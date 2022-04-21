from models.model import db


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    company_name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
