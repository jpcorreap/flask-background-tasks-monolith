from models.model import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    names = db.Column(db.String(128), unique=True, nullable=False)
    last_names = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False, primary_key=True)
    submissions2 = db.relationship(
        "Submission", backref="submission", cascade="all, delete-orphan"
    )
    admin = db.relationship("Admin", backref="admin", uselist=False)
