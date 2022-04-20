from datetime import datetime
import os
import uuid
from backend.utils.s3fs_utils import upload_file

from constants.extensions import MAPPER_AUDIO_FILE
from constants.limit import ROWS_PER_PAGE
from flask import Response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models.contest import Contest
from models.model import db
from models.submission import Submission, SubmissionStatus
from models.user import User
from schemas.submission import submission_schema, submissions_schema
from settings import config
from tasks import celery_app
from utils.extensions import allowed_file
from werkzeug.utils import secure_filename


class ResourceSubmission(Resource):
    @jwt_required(optional=True)
    def get(self, contest_url):
        page = request.args.get("page", 1, type=int)
        contest = Contest.query.filter_by(url=contest_url).first_or_404()
        if get_jwt_identity():
            submissions = Submission.query.filter_by(contest_id=contest.id).order_by(
                Submission.upload_date.desc()
            )
        else:
            submissions = Submission.query.filter_by(
                contest_id=contest.id, status="converted"
            ).order_by(Submission.upload_date.desc())
        return submissions_schema.dump(
            submissions.paginate(page=page, per_page=ROWS_PER_PAGE).items
        )

    def post(self, contest_url):
        if "file" not in request.files:
            return ("not file in request", 400)
        file = request.files.get("file")
        if file and file.filename == "":
            return ("no file found in request", 400)
        contest = Contest.query.filter_by(url=contest_url).first_or_404()
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
            file_id = uuid.uuid4()
            file_type = secure_filename(file.filename).split(".")[-1]
            final_name = f"{file_id}.{file_type}"
            new_submission = Submission(
                id=file_id,
                user_id=user.id,
                observations=request.form["observations"],
                status="processing",
                contest_id=contest.id,
                upload_date=datetime.now(),
                file_type=file_type,
            )

            db.session.add(new_submission)
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

            return submission_schema.dump(new_submission)
        return ("Not allowed file type", 400)


class ResourceSubmissionDetail(Resource):
    @jwt_required(optional=True)
    def get(self, contest_url, id_submission):
        contest = Contest.query.filter_by(url=contest_url).first_or_404()
        if get_jwt_identity():
            submission = Submission.query.filter_by(
                id=id_submission, contest_id=contest.id
            ).first_or_404()
        else:
            submission = Submission.query.filter_by(
                id=id_submission, contest_id=contest.id, status="converted"
            ).first_or_404()
        return submission_schema.dump(submission)

    def patch(self, id_submission):
        submission = Submission.query.filter_by(id=id_submission).first_or_404()
        submission.status = request.json["status"]
        db.session.commit()
        return submission_schema.dump(submission)


class ResourceAudioSubmission(Resource):
    @jwt_required(optional=True)
    def get(self, id):
        submission = Submission.query.filter_by(id=id).first_or_404()
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
        submission = Submission.query.filter_by(id=id).first_or_404()
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
