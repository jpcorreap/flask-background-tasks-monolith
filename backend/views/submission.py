from datetime import datetime
import os
import uuid

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models.contest import Contest
from models.model import db
from models.submission import Submission
from models.user import User
from schemas.submission import submission_schema, submissions_schema
from settings import config
from utils.extensions import allowed_file
from werkzeug.utils import secure_filename


class ResourceSubmission(Resource):
    @jwt_required(optional=True)
    def get(self, contest_url):
        contest = Contest.query.filter_by(url=contest_url).first_or_404()
        if get_jwt_identity():
            submissions = (
                Submission.query.filter_by(contest_id=contest.id)
                .order_by(Submission.upload_date.desc())
                .get_or_404()
            )
        else:
            submissions = (
                Submission.query.filter_by(contest_id=contest.id, status="converted")
                .order_by(Submission.upload_date.desc())
                .get_or_404()
            )
        return submissions_schema.dump(submissions)

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
            file.save(os.path.join(config.UPLOAD_FOLDER, final_name))
            return submission_schema.dump(new_submission)
        return ("Not allowed file type", 400)


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
