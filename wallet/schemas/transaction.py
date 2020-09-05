from schematics import Model
from schematics.types import StringType, DecimalType, ListType, ModelType


class Transaction(Model):
    amount = DecimalType(required=True)
    receiver = StringType(required=True)


class SentTransaction(Model):
    amount = DecimalType(required=True)
    receiver = StringType(required=True)


class ReceivedTransaction(Model):
    amount = DecimalType(required=True)
    sender = StringType(required=True)


class TransactionList(Model):
    sent = ListType(ModelType(SentTransaction), default=[])
    received = ListType(ModelType(ReceivedTransaction), default=[])
