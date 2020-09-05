"""creates users

Revision ID: 1975ea83b712
Revises: 2afffe73f809

"""

# revision identifiers, used by Alembic.
revision = '1975ea83b712'
down_revision = 'b01ef8e186b7'
branch_labels = None

import uuid

from alembic import op
from sqlalchemy import orm
from werkzeug.security import generate_password_hash
from wallet.db.user import User
from wallet.db.balance import Balance

def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    data = [
        {
            'username': 'UserOne',
            'password': generate_password_hash('Test123')
        },
        {
            'username': 'UserTwo',
            'password': generate_password_hash('Test456')
        }
    ]
    for user in data:
        db_user = User(id=str(uuid.uuid4()), username=user['username'], password=user['password'])
        balance = Balance(id=str(uuid.uuid4()), user_id=str(db_user.id), amount=1000)
        session.add(db_user)
        session.add(balance)
    session.commit()


def downgrade():
    pass
