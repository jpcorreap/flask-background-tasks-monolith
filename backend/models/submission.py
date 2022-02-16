from enum import Enum
import uuid

from models.model import db


class SubmissionStatus(str, Enum):
    processing = "processing"
    converted = "converted"


class SubmissionFileType(str, Enum):
    mp3 = "mp3"
    wav = "wav"
    m4a = "m4a"
    mpc = "mpc"
    wma = "wma"


class Submission(db.Model):
    __tablename__ = "submission"
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    observations = db.Column(db.String(512), nullable=False)
    status = db.Column(db.Enum(SubmissionStatus), nullable=False)
    contest_id = db.Column(db.UUID, db.ForeignKey("contest.id"), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    file_type = db.Column(db.Enum(SubmissionFileType), nullable=False)
