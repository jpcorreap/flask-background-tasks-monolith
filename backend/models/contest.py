from models.model import db


class Contest(db.Model):
    __tablename__ = "contest"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    banner = db.Column(db.String(128), unique=True, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    submissions = db.relationship(
        "Submission", backref="submission", cascade="all, delete-orphan"
    )
    prize = db.Column(db.Float, nullable=False)
    script = db.Column(db.String(256), nullable=False)
    advices = db.Column(db.String(256), nullable=False)
    admin = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)
    db.CheckConstraint("end_date > start_date", name="date_constraint")
