from datetime import datetime
import json
import os
import uuid

from constants.extensions import MAPPER_IMAGE_FILE
from constants.format import DATE_FORMAT
from flask import Response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models.contest import Contest
from models.submission import Submission
from settings import config
from utils.extensions import allowed_file
from utils.s3fs_utils import save_file
from utils.validators import validate_url


class ResourceContest(Resource):
    @jwt_required()
    def get(self):
        page = request.args.get("page", 1, type=int)
        contests = Contest.admin_index.query(int(get_jwt_identity()))
        ans = [json.loads(contest.to_json()) for contest in contests]
        # ORDER BY
        return ans

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
                    file_id = str(uuid.uuid4())
                    file_type = file.filename.split(".")[-1]
                    filename = f"{file_id}.{file_type}"
                    if not validate_url(request.form["url"]):
                        return ("Wrong URL", 400)
                    start_date = datetime.strptime(
                        request.form["start_date"], DATE_FORMAT
                    )
                    end_date = datetime.strptime(request.form["end_date"], DATE_FORMAT)
                    if start_date > end_date:
                        return "End date should be greater than start date", 400
                    new_contest = Contest(
                        file_id,
                        url=request.form["url"],
                        name=request.form["name"],
                        image_type=file_type,
                        start_date=start_date,
                        end_date=end_date,
                        prize=request.form["prize"],
                        script=request.form["script"],
                        advices=request.form["advices"],
                        admin=int(get_jwt_identity()),
                    )
                    new_contest.save()
                    save_file(file, config.BANNER_FOLDER_PATH, filename)
                    return json.loads(new_contest.to_json())
                return ("Not allowed file type", 400)
            return ("Not file was sent", 400)
        except Exception as e:
            error = str(e)
            return error, 422


class ResourceContestDetail(Resource):
    @jwt_required(optional=True)
    def get(self, contest_url):
        page = request.args.get("page", 1, type=int)
        contest = [_ for _ in Contest.url_index.query(contest_url)][0]
        contest_id = contest.id
        if not get_jwt_identity():
            submissions = Submission.contest_id_index.query(
                contest_id, filter_condition=Submission.status == "converted"
            )
        else:
            submissions = Submission.contest_id_index.query(contest_id)
        submissions = [json.loads(submission.to_json()) for submission in submissions]
        ans = json.loads(contest.to_json())
        ans["submissions"] = submissions
        return ans

    @jwt_required()
    def put(self, contest_url):
        try:
            contest = [
                _
                for _ in Contest.admin_index.query(
                    int(get_jwt_identity()),
                    filter_condition=(Contest.url == contest_url),
                )
            ][0]
            file = request.files.get("file")
            if file:
                if file.filename == "":
                    return ("no file found in request", 400)
                if allowed_file(file.filename, "image"):
                    file_type = file.filename.split(".")[-1]
                    filename = f"{contest.id}.{file_type}"
                    contest.image_type = file_type
                    file.save(os.path.join(config.BANNER_FOLDER_PATH, filename))
                    file.close()
            if not validate_url(request.form["url"]):
                return ("Wrong URL", 400)
            contest.url = request.form["url"]
            contest.name = request.form["name"]
            start_date = datetime.strptime(request.form["start_date"], DATE_FORMAT)
            contest.start_date = start_date
            end_date = datetime.strptime(request.form["end_date"], DATE_FORMAT)
            contest.end_date = end_date
            if start_date > end_date:
                return "End date should be greater than start date", 400
            contest.prize = request.form["prize"]
            contest.script = request.form["script"]
            contest.advices = request.form["advices"]
            contest.save()
            return json.loads(contest.to_json())
        except Exception as e:
            error = str(e)
            return error, 422

    @jwt_required()
    def delete(self, contest_url):
        contest = [
            _
            for _ in Contest.admin_index.query(
                int(get_jwt_identity()), filter_condition=(Contest.url == contest_url)
            )
        ][0]
        contest.delete()
        return "", 204

    @jwt_required()
    def patch(self, contest_url):
        try:
            contest = [
                _
                for _ in Contest.admin_index.query(
                    int(get_jwt_identity()),
                    filter_condition=(Contest.url == contest_url),
                )
            ][0]
            if url := request.form.get("url"):
                if not validate_url(url):
                    return ("Wrong URL", 400)
                contest.url = url
            if name := request.form.get("name"):
                contest.name = name
            if file := request.files.get("file"):
                if file.filename != "" and allowed_file(file.filename, "image"):
                    file_type = file.filename.split(".")[-1]
                    filename = f"{contest.id}.{file_type}"
                    contest.image_type = file_type
                    file.save(os.path.join(config.BANNER_FOLDER_PATH, filename))
                    file.close()
                else:
                    return ("invalid file found in request", 400)
            if prize := request.form.get("prize"):
                contest.prize = prize
            if script := request.form.get("script"):
                contest.script = script
            if advices := request.form.get("advices"):
                contest.advices = advices
            if start_date := request.form.get("start_date"):
                contest.start_date = datetime.strptime(start_date, DATE_FORMAT)
            if end_date := request.form.get("end_date"):
                contest.end_date = datetime.strptime(end_date, DATE_FORMAT)
            if start_date and end_date and start_date > end_date:
                return "End date should be greater than start date", 400
            contest.save()
            return json.loads(contest.to_json())
        except Exception as e:
            error = str(e)
            return error, 422


class ResourceBannerImageContest(Resource):
    def get(self, url_contest):
        contest = [_ for _ in Contest.url_index.query(url_contest)][0]
        route = os.path.join(
            config.BANNER_FOLDER_PATH, f"{contest.id}.{contest.image_type}"
        )

        def generate():
            with open(route, "rb") as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)

        return Response(generate(), mimetype=MAPPER_IMAGE_FILE[contest.image_type])
