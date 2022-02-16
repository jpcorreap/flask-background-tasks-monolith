from marshmallow import fields
from models.contest import Contest
from schemas.schema import ma
from schemas.submission import SubmissionSchema


class ContestSchema(ma.Schema):
    model = Contest

    class Meta:
        fields = (
            "id",
            "url",
            "name",
            "image_type",
            "start_date",
            "end_date",
            "prize",
            "script",
            "advices",
            "admin",
        )

    submissions = fields.List(fields.Nested(SubmissionSchema, required=True))


contest_schema = ContestSchema()
contests_schema = ContestSchema(many=True)
