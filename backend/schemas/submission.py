from app import ma


class SubmissionSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "observations", "status", "contest_id")


submission_schema = SubmissionSchema()
submissions_schema = SubmissionSchema(many=True)
