"""create apt_num on address table

Revision ID: d620899a4069
Revises: d9ed7cd0842f
Create Date: 2023-06-22 21:44:23.445290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd620899a4069'
down_revision = 'd9ed7cd0842f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address",sa.Column("apt_num",sa.String(),nullable=True))



def downgrade() -> None:
    op.drop_column("address","apt_num")
