from datetime import datetime

from constants.format import DATE_FORMAT
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models.contest import Contest
from models.model import db
from schemas.contest import contest_schema, contests_schema


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
        new_contest = Contest(
            url=request.json["url"],
            name=request.json["name"],
            banner=request.json["banner"],
            start_date=datetime.strptime(request.json["start_date"], DATE_FORMAT),
            end_date=datetime.strptime(request.json["end_date"], DATE_FORMAT),
            prize=request.json["prize"],
            script=request.json["script"],
            advices=request.json["advices"],
            admin=get_jwt_identity(),
        )
        db.session.add(new_contest)
        db.session.commit()
        return contest_schema.dump(new_contest)


class ResourceContestDetail(Resource):
    def get(self, contest_url):
        contest = Contest.query.filter_by(url=contest_url).first_or_404()
        return contest_schema.dump(contest)

    @jwt_required()
    def put(self, contest_url):
        contest = Contest.query.filter_by(
            url=contest_url, admin=get_jwt_identity()
        ).first_or_404()
        contest.url = request.json["url"]
        contest.name = request.json["name"]
        contest.banner = request.json["banner"]
        contest.start_date = datetime.strptime(request.json["start_date"], DATE_FORMAT)
        contest.end_date = datetime.strptime(request.json["end_date"], DATE_FORMAT)
        contest.prize = request.json["prize"]
        contest.script = request.json["script"]
        contest.advices = request.json["advices"]
        db.session.commit()
        return contest_schema.dump(contest)

    @jwt_required()
    def delete(self, contest_url):
        contest = Contest.query.filter_by(
            url=contest_url, admin=get_jwt_identity()
        ).first_or_404()
        db.session.delete(contest)
        db.session.commit()
        return "", 204

    @jwt_required
    def patch(self, contest_url):
        contest = Contest.query.filter_by(
            url=contest_url, admin=get_jwt_identity()
        ).first_or_404()
        if url := request.json.get("url"):
            contest.url = url
        if name := request.json.get("name"):
            contest.name = name
        if banner := request.json.get("banner"):
            contest.banner = banner
        if prize := request.json.get("prize"):
            contest.prize = prize
        if script := request.json.get("script"):
            contest.script = script
        if advices := request.json.get("advices"):
            contest.advices = advices
        if start_date := request.json.get("start_date"):
            contest.start_date = start_date
        if end_date := request.json.get("end_date"):
            contest.end_date = end_date
        db.session.commit()
        return contest_schema.dump(contest)
