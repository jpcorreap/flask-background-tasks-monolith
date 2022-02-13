from datetime import datetime
import json
import os
import uuid

from flask import config, request
from flask_restful import Resource
from models.model import db
from models.submission import Submission
from schemas.submission import submission_schema, submissions_schema
from werkzeug.utils import secure_filename

from backend.models.contest import Contest
from backend.models.user import User

ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a", "mpc", "wma"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class ResourceSubmission(Resource):
    def get(self, contest_url):
        contest = Contest.query.filter_by(url=contest_url).first_or_404()
        submissions = (
            Submission.query.filter_by(contest_id=contest.id)
            .order_by(Submission.upload_date.desc())
            .get_or_404()
        )
        return submissions_schema.dump(submissions)

    def post(self, contest_url):
        res = None
        if "file" not in request.files:
            res = ("not file in request", 400)

        if "data" not in request.files:
            res = ("not user data in request", 400)

        file = request.files["file"]

        if file.filename == "":
            res = ("no file founded in request", 400)

        json_data = json.load(request.files["data"])
        contest = Contest.query.filter_by(url=contest_url).first_or_404()
        user = User.query.filter_by(email=json_data["email"]).first()

        if not user:
            new_user = User(
                email=json_data["email"],
                names=json_data["names"],
                last_names=json_data["last_names"],
            )
            db.session.add(new_user)
            db.session.flush()

        new_submission: Submission

        if file and allowed_file(file.filename):
            file_id = uuid.uuid4()
            file_type = secure_filename(file.filename).split(".")[1]
            final_name = f"{file_id}.{file_type}"
            file.save(os.path.join(config["UPLOAD_FOLDER"], final_name))
            new_submission = Submission(
                id=file_id,
                user_id=user.id,
                observations=json_data["observations"],
                status="processing",
                contest_id=contest.id,
                upload_date=datetime.now(),
                file_type=file_type,
            )
            db.session.add(new_submission)
            db.session.commit()
            res = submission_schema.dump(new_submission)

        return res


class ResourceSubmissionDetail(Resource):
    def get(self, contest_url, id_submission):
        contest = Contest.query.filter_by(url=contest_url).first_or_404()
        submission = Submission.query.filter_by(
            id=id_submission, contest_id=contest.id
        ).first_or_404()
        return submission_schema.dump(submission)

    def patch(self, id_submission):
        submission = Submission.query.filter_by(id=id_submission).first_or_404()
        submission.status = request.json["status"]
        db.session.commit()
        return submission_schema.dump(submission)
