from expense_tracker.extensions import ma
from marshmallow import post_load, pre_load

from .models import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name", "is_admin")
        load_only = ("password", )
        # fields = ("id", "username", "password", "email", "first_name", "last_name", "is_admin")

    # @post_load
    # def make_user(self, data, **kwargs):
    #     return User(**data)


user_schema = UserSchema()