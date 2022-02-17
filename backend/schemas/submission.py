from models.submission import Submission
from schemas.schema import ma


class SubmissionSchema(ma.Schema):
    class Meta:
        model = Submission
        fields = (
            "id",
            "user_id",
            "observations",
            "status",
            "contest_id",
            "file_type",
            "upload_date",
        )


submission_schema = SubmissionSchema()
submissions_schema = SubmissionSchema(many=True)
