from models.model import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    names = db.Column(db.String(128), nullable=False)
    last_names = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False, primary_key=True)
    submissions = db.relationship("Submission", cascade="all, delete-orphan")
    admin = db.relationship("Admin", backref="admin", uselist=False)
