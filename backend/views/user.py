from datetime import timedelta

from flask import request
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from models.model import db
from models.user import User

from backend.models.admin import Admin


class SignIn(Resource):
    def post(self):
        user = User.query.filter_by(email=request.json["email"]).first()
        admin = Admin.query.filter_by(id=user.id).first()
        if check_password_hash(
            admin.password, request.json["password"].encode("utf-8")
        ):
            access_token = create_access_token(
                identity=str(user.id), expires_delta=timedelta(hours=2)
            )
            return {"access_token": access_token}, 200
        else:
            return "Wrong email or password", 401


class SignUp(Resource):
    def post(self):
        new_user = User(
            email=request.json["email"],
            names=request.json["names"],
            last_names=request.json["last_names"],
        )
        db.session.add(new_user)
        db.session.flush()
        new_admin = Admin(
            id=new_user.id,
            company_name=request.json["company_name"],
            password=generate_password_hash(
                request.json["password"].encode("utf-8")
            ).decode("utf-8"),
        )
        db.session.add(new_admin)
        db.session.commit()
        return "", 204
