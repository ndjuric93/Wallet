from schematics import Model
from schematics.types import StringType


class LoginRequest(Model):
    username = StringType(required=True)
    password = StringType(required=True)
