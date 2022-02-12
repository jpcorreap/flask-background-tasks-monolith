from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from models.model import db
from schemas.schema import ma

from backend.views.user import SignIn, SignUp

# app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
app = Flask(__name__)
app.config.from_object("settings")

db.init_app(app)
with app.app_context():
    db.create_all()
ma.init_app(app)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# api.add_resource(ResourceEvent, "/api/events")
# api.add_resource(ResourceEventDetail, "/api/events/<int:id_event>")
api.add_resource(SignUp, "/api/signup")
api.add_resource(SignIn, "/api/signin")


@app.route("/")
def serve():
    return app.send_static_file("index.html")
