from datetime import datetime
import os

from constants.format import DATE_FORMAT
from flask import config, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models.contest import Contest
from models.model import db
from schemas.contest import contest_schema, contests_schema
from sqlalchemy.exc import SQLAlchemyError

from backend.utils.extensions import allowed_file


class ResourceContest(Resource):
    @jwt_required()
    def get(self):
        contests = (
            Contest.query.filter_by(admin=get_jwt_identity())
            .order_by(Contest.id.desc())
            .all()
        )
        return contests_schema.dump(contests)

    @jwt_required()
    def post(self):
        try:
            if "file" not in request.files:
                return ("not file in request", 400)
            file = request.files.get("file")
            if file:
                if file.filename == "":
                    return ("no file found in request", 400)
                if allowed_file(file.filename, "image"):
                    new_contest = Contest(
                        url=request.form["url"],
                        name=request.form["name"],
                        banner=file.filename,
                        start_date=datetime.strptime(
                            request.form["start_date"], DATE_FORMAT
                        ),
                        end_date=datetime.strptime(
                            request.form["end_date"], DATE_FORMAT
                        ),
                        prize=request.form["prize"],
                        script=request.form["script"],
                        advices=request.form["advices"],
                        admin=get_jwt_identity(),
                    )
                    db.session.add(new_contest)
                    db.session.commit()
                    file.save(os.path.join(config["BANNER_FOLDER_PATH"], file.filename))
                    return contest_schema.dump(new_contest)
                return ("Not allowed file type", 400)
            return ("Not file was sent", 400)
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return error, 422


class ResourceContestDetail(Resource):
    def get(self, contest_url):
        contest = Contest.query.filter_by(url=contest_url).first_or_404()
        return contest_schema.dump(contest)

    @jwt_required()
    def put(self, contest_url):
        try:
            contest = Contest.query.filter_by(
                url=contest_url, admin=get_jwt_identity()
            ).first_or_404()
            file = request.files.get("file")
            if file:
                if file.filename == "":
                    return ("no file found in request", 400)
                if allowed_file(file.filename, "image"):
                    contest.banner = file.filename
                    file.save(os.path.join(config["BANNER_FOLDER_PATH"], file.filename))
            contest.url = request.form["url"]
            contest.name = request.form["name"]
            contest.start_date = datetime.strptime(
                request.form["start_date"], DATE_FORMAT
            )
            contest.end_date = datetime.strptime(request.form["end_date"], DATE_FORMAT)
            contest.prize = request.form["prize"]
            contest.script = request.form["script"]
            contest.advices = request.form["advices"]
            db.session.commit()
            return contest_schema.dump(contest)
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return error, 422

    @jwt_required()
    def delete(self, contest_url):
        contest = Contest.query.filter_by(
            url=contest_url, admin=get_jwt_identity()
        ).first_or_404()
        db.session.delete(contest)
        db.session.commit()
        return "", 204

    @jwt_required()
    def patch(self, contest_url):
        try:
            contest = Contest.query.filter_by(
                url=contest_url, admin=get_jwt_identity()
            ).first_or_404()
            if url := request.form.get("url"):
                contest.url = url
            if name := request.form.get("name"):
                contest.name = name
            if file := request.files.get("file"):
                if file.filename != "" and allowed_file(file.filename, "image"):
                    contest.banner = file.filename
                    file.save(os.path.join(config["BANNER_FOLDER_PATH"], file.filename))
                else:
                    return ("invalid file found in request", 400)
            if prize := request.form.get("prize"):
                contest.prize = prize
            if script := request.form.get("script"):
                contest.script = script
            if advices := request.form.get("advices"):
                contest.advices = advices
            if start_date := request.form.get("start_date"):
                contest.start_date = start_date
            if end_date := request.form.get("end_date"):
                contest.end_date = end_date
            db.session.commit()
            return contest_schema.dump(contest)
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return error, 422
