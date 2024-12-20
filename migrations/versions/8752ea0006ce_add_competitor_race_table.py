"""Add competitor_race table

Revision ID: 8752ea0006ce
Revises: 86f1939b5fd1
Create Date: 2024-11-24 19:30:47.053139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8752ea0006ce'
down_revision = '86f1939b5fd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('competitor_races', schema=None) as batch_op:
        batch_op.add_column(sa.Column('competitor_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_competitor_race', 'competitor', ['competitor_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('competitor_races', schema=None) as batch_op:
        batch_op.drop_constraint('fk_competitor_race', type_='foreignkey')
        batch_op.drop_column('competitor_id')

    # ### end Alembic commands ###
