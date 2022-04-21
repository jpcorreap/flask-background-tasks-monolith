from datetime import datetime
import json
import os
import uuid
from utils.s3fs_utils import upload_file

from constants.extensions import MAPPER_AUDIO_FILE
from flask import Response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models.contest import Contest
from models.model import db
from models.submission import Submission, SubmissionStatus
from models.user import User
from settings import config
from tasks import celery_app
from utils.extensions import allowed_file
from werkzeug.utils import secure_filename


class ResourceSubmission(Resource):
    def post(self, contest_url):
        if "file" not in request.files:
            return ("not file in request", 400)
        file = request.files.get("file")
        if file and file.filename == "":
            return ("no file found in request", 400)
        contest = [_ for _ in Contest.url_index.query(contest_url)][0]
        user = User.query.filter_by(email=request.form["email"]).first()
        if not user:
            user = User(
                email=request.form["email"],
                names=request.form["names"],
                last_names=request.form["last_names"],
            )
            db.session.add(user)
            db.session.flush()
        new_submission: Submission
        if file and allowed_file(file.filename, "audio"):
            file_id = str(uuid.uuid4())
            file_type = secure_filename(file.filename).split(".")[-1]
            final_name = f"{file_id}.{file_type}"
            new_submission = Submission(
                file_id,
                user_id=user.id,
                observations=request.form["observations"],
                status="processing",
                contest_id=contest.id,
                upload_date=datetime.now(),
                file_type=file_type,
                user_name=f"{user.names} {user.last_names}",
                user_email=user.email,
            )

            new_submission.save()
            db.session.commit()
            # Esto era de los modelos A, B y C
            # file.save(os.path.join(config.UPLOAD_FOLDER, final_name))
            # file.close()

            # Cambio al modelo D
            successfully_uploaded = upload_file(file, config.PROCESSING_FOLDER_PATH, final_name)

            if successfully_uploaded:
                # TODO modificar esta logica para enviar a SQS en lugar de Celery
                celery_app.send_task(
                    "tasks.process_audio_files", 
                    kwargs={
                        "sub_id": file_id,
                        "file_type": file_type,
                        "user_email": user.email
                    }
                )

            return json.loads(new_submission.to_json())
        return ("Not allowed file type", 400)


class ResourceSubmissionDetail(Resource):
    def patch(self, id_submission):
        submission = Submission.get(id_submission)
        submission.status = request.json["status"]
        submission.save()
        return json.loads(submission.to_json())


class ResourceAudioSubmission(Resource):
    @jwt_required(optional=True)
    def get(self, id):
        submission = Submission.query(id)
        if submission.status == SubmissionStatus.processing and not get_jwt_identity():
            return Response(status=401)
        route = (
            os.path.join(config.PROCESSED_FOLDER_PATH, f"{submission.id}.mp3")
            if submission.status == SubmissionStatus.converted
            else os.path.join(
                config.PROCESSING_FOLDER_PATH, f"{submission.id}.{submission.file_type}"
            )
        )

        def generate():
            with open(route, "rb") as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)

        return Response(
            generate(),
            mimetype=MAPPER_AUDIO_FILE["mp3"]
            if submission.status == SubmissionStatus.converted
            else MAPPER_AUDIO_FILE[submission.file_type],
        )


class ResourceAudioSubmissionRaw(Resource):
    def get(self, id):
        submission = Submission.query(id)
        route = os.path.join(
            config.PROCESSING_FOLDER_PATH, f"{submission.id}.{submission.file_type}"
        )

        def generate():
            with open(route, "rb") as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)

        return Response(
            generate(),
            mimetype=MAPPER_AUDIO_FILE[submission.file_type],
        )
