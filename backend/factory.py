from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from celery_utils import init_celery
from models.model import db
from schemas.schema import ma
from settings import config
from views.contest import (
    ResourceBannerImageContest,
    ResourceContest,
    ResourceContestDetail,
)
from views.submission import (
    ResourceAudioSubmission,
    ResourceAudioSubmissionRaw,
    ResourceSubmission,
    ResourceSubmissionDetail,
)
from views.user import SignIn, SignUp, UserDetail

def create_app(**kwargs):
    flask_app = Flask(__name__, static_folder="../front/build", static_url_path="/")
    flask_app.config.from_object(config)

    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()
    ma.init_app(flask_app)
    api = Api(flask_app)
    bcrypt = Bcrypt(flask_app)
    jwt = JWTManager(flask_app)
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), flask_app)
    CORS(flask_app)

    api.add_resource(ResourceContest, "/api/contests")
    api.add_resource(ResourceContestDetail, "/api/contests/<string:contest_url>")
    api.add_resource(SignUp, "/api/signup")
    api.add_resource(SignIn, "/api/signin")
    api.add_resource(ResourceSubmission, "/api/contests/<string:contest_url>/submissions")
    api.add_resource(
        ResourceSubmissionDetail,
        "/api/contests/<string:contest_url>/submissions/<string:id_submission>",
    )
    api.add_resource(ResourceAudioSubmission, "/api/submissions/<string:id>")
    api.add_resource(ResourceAudioSubmissionRaw, "/api/submissions/raw/<string:id>")
    api.add_resource(
        ResourceBannerImageContest, "/api/contests/banner/<string:url_contest>"
    )
    api.add_resource(UserDetail, "/api/users/<int:user_id>")


    @flask_app.route("/")
    @flask_app.route("/contests")
    @flask_app.route("/login")
    @flask_app.route("/signup")
    def serve():
        return flask_app.send_static_file("index.html")

    @flask_app.route("/contests/<string:x>")
    def serve1(x):
        return flask_app.send_static_file("index.html")

    @flask_app.route("/contests/<string:x>/submit")
    @flask_app.route("/contests/<string:x>/edit")
    def serve2(x):
        return flask_app.send_static_file("index.html")
    return flask_app