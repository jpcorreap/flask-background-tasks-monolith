from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from models.model import db
from schemas.schema import ma
from settings import config
from views.contest import ResourceBannerImageContest, ResourceContest, ResourceContestDetail
from views.submission import ResourceAudioSubmission, ResourceSubmission, ResourceSubmissionDetail
from views.user import SignIn, SignUp

# app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
with app.app_context():
    db.create_all()
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
api.add_resource(ResourceBannerImageContest,"/api/contests/banner/<string:url_contest>")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")
