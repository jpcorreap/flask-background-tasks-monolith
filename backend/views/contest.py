from datetime import datetime

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
            start_date=datetime.strptime(
                request.json["start_date"], "%Y-%m-%d %-H:%-M"
            ),
            end_date=datetime.strptime(request.json["end_date"], "%Y-%m-%d %-H:%-M"),
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
    def put(self, id_contest):
        contest = Contest.query.filter_by(
            id=id_contest, admin=get_jwt_identity()
        ).first_or_404()
        contest.url = (request.json["url"],)
        contest.name = (request.json["name"],)
        contest.banner = (request.json["banner"],)
        contest.start_date = (
            datetime.strptime(request.json["start_date"], "%Y-%m-%d %-H:%-M"),
        )
        contest.end_date = (
            datetime.strptime(request.json["end_date"], "%Y-%m-%d %-H:%-M"),
        )
        contest.prize = (request.json["prize"],)
        contest.script = (request.json["script"],)
        contest.advices = (request.json["advices"],)
        db.session.commit()
        return contest_schema.dump(contest)

    @jwt_required()
    def delete(self, id_contest):
        contest = Contest.query.filter_by(
            id=id_contest, admin=get_jwt_identity()
        ).first_or_404()
        db.session.delete(contest)
        db.session.commit()
        return "", 204
