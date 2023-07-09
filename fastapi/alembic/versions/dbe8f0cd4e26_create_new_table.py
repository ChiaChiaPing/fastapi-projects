"""create new table

Revision ID: dbe8f0cd4e26
Revises: 48bdd6e7057d
Create Date: 2023-06-22 20:40:22.214239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbe8f0cd4e26'
down_revision = '48bdd6e7057d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("address",
                    sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                    sa.Column("address1",sa.String(),nullable=False),
                    sa.Column("address2",sa.String(),nullable=False),
                    sa.Column("city",sa.String(),nullable=False),
                    sa.Column("state",sa.String(),nullable=False),
                    sa.Column("country",sa.String(),nullable=False),
                    sa.Column("postalcode",sa.String(),nullable=False)
                    )


def downgrade() -> None:
    op.drop_table("address")
