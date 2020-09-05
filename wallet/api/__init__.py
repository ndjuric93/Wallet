from flask import Blueprint

api: Blueprint = Blueprint('api', __name__)

from wallet.api.status import get_status
from wallet.api.user import login
from wallet.api.balance import get_balance
from wallet.api.transaction import get_transactions, create_transaction
