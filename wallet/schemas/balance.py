from schematics import Model
from schematics.types import DecimalType


class Balance(Model):
    """
    Balance schema
    """
    amount = DecimalType()
