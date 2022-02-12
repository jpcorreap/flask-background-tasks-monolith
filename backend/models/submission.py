from enum import Enum

from app import db


class SubmissionStatus(str, Enum):
    processing = "processing"
    converted = "converted"


class Submission(db.Model):
    __tablename__ = "submission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    observations = db.Column(db.String(512), nullable=False)
    status = db.Column(db.Enum(SubmissionStatus), nullable=False)
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
