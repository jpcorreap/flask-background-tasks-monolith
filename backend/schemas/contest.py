from schemas.schema import ma


class ContestSchema(ma.Schema):
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
