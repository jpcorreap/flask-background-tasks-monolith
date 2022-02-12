from app import ma


class AdminSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "company_name",
            "contests",
        )


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)
