from marshmallow import fields
from models.contest import Contest
from schemas.schema import ma
from schemas.submission import SubmissionSchema


class ContestSchema(ma.Schema):
    model = Contest
    submissions = (fields.List(fields.Nested(SubmissionSchema, required=True)),)

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


contest_schema = ContestSchema()
contests_schema = ContestSchema(many=True)
