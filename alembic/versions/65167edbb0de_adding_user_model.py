"""
Adding user model.

Revision ID: 65167edbb0de
Revises: 
Create Date: 2023-05-02 18:12:30.947031

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '65167edbb0de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade the schema to this version."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade the schema to this version."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###