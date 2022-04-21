from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from models.contest import Contest
from models.model import db
from models.submission import Submission
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

app = Flask(__name__, static_folder="../front/build", static_url_path="/")
app.config.from_object(config)

db.init_app(app)
with app.app_context():
    db.create_all()
    if not Submission.exists():
        Submission.create_table(
            wait=True, read_capacity_units=1, write_capacity_units=1
        )
    if not Contest.exists():
        Contest.create_table(wait=True, read_capacity_units=1, write_capacity_units=1)

ma.init_app(app)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

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


@app.route("/")
@app.route("/contests")
@app.route("/login")
@app.route("/signup")
def serve():
    return app.send_static_file("index.html")


@app.route("/contests/<string:x>")
def serve1(x):
    return app.send_static_file("index.html")


@app.route("/contests/<string:x>/submit")
@app.route("/contests/<string:x>/edit")
def serve2(x):
    return app.send_static_file("index.html")
