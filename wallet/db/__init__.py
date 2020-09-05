from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"autoflush": False})

from wallet.db.user import User
from wallet.db.balance import Balance
from wallet.db.transaction import Transaction
