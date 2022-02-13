from schemas.schema import ma


class ContestSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "url",
            "name",
            "banner",
            "start_date",
            "end_date",
            "submissions",
            "prize",
            "script",
            "advices",
            "admin",
        )


contest_schema = ContestSchema()
contests_schema = ContestSchema(many=True)
