"""Create phone number for user sql

Revision ID: 48bdd6e7057d
Revises: 
Create Date: 2023-06-22 20:15:49.145795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48bdd6e7057d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users",sa.Column("phone_number",sa.String,nullable=True))



def downgrade() -> None:
    op.drop_column("users","phone_number")
