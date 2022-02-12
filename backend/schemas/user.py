from app import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "names","last_names","email","submissions")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
