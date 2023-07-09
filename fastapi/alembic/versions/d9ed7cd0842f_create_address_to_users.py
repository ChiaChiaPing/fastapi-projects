"""create address to users

Revision ID: d9ed7cd0842f
Revises: dbe8f0cd4e26
Create Date: 2023-06-22 20:46:54.637377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9ed7cd0842f'
down_revision = 'dbe8f0cd4e26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users",sa.Column("address_id",sa.Integer(),nullable=True))
    op.create_foreign_key("address_user_FK","users","address",["address_id"],["id"], ondelete="CASCADE")
    


def downgrade() -> None:
    op.drop_constraint("address_user_FK","users")
    op.drop_column("users","address_id")  
