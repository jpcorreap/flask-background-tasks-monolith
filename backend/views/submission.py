from datetime import datetime

from flask import request
from flask_restful import Resource
from models.model import db
from models.submission import Submission
from schemas.submission import submission_schema, submissions_schema

from backend.models.contest import Contest
from backend.models.user import User


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
        contest = Contest.query.filter_by(url=contest_url).first_or_404()
        user = User.query.filter_by(email=request.json["email"]).first()
        if not user:
            new_user = User(
                email=request.json["email"],
                names=request.json["names"],
                last_names=request.json["last_names"],
            )
            db.session.add(new_user)
            db.session.flush()
        new_submission = Submission(
            user_id=user.id,
            observations=request.json["observations"],
            status="processing",
            contest_id=contest.id,
            upload_date=datetime.now(),
        )
        db.session.add(new_submission)
        db.session.commit()
        return submission_schema.dump(new_submission)


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
