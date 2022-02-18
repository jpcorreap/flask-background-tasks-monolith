from datetime import timedelta

from flask import request
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from models.admin import Admin
from models.model import db
from models.user import User
from schemas.user import user_schema


class SignIn(Resource):
    def post(self):
        ans = "Wrong email or password", 401
        user = User.query.filter_by(email=request.json["email"]).first()
        if user:
            admin = Admin.query.filter_by(id=user.id).first()
            if check_password_hash(
                admin.password, request.json["password"].encode("utf-8")
            ):
                access_token = create_access_token(
                    identity=str(user.id),
                    expires_delta=timedelta(hours=2),
                    additional_claims={"email": request.json["email"]},
                )
                ans = {"access_token": access_token}, 200
        return ans


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
        access_token = create_access_token(
            identity=str(new_user.id),
            expires_delta=timedelta(hours=2),
            additional_claims={"email": request.json["email"]},
        )
        return {"access_token": access_token}, 200


class UserDetail(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first_or_404()
        return user_schema.dump(user)
