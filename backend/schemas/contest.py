from schemas.schema import ma
from schemas.submission import SubmissionSchema
from marshmallow  import fields
from models.contest import Contest
class ContestSchema(ma.Schema):
    model=Contest
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
    submissions = fields.Nested(SubmissionSchema,many=True,required=True)



contest_schema = ContestSchema()
contests_schema = ContestSchema(many=True)
