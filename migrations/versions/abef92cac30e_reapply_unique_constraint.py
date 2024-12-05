"""Reapply unique constraint

Revision ID: abef92cac30e
Revises: 52a52138bf12
Create Date: 2024-11-25 12:39:20.585442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abef92cac30e'
down_revision = '52a52138bf12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_competitor_races')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('_alembic_tmp_competitor_races',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('race_id', sa.INTEGER(), nullable=False),
    sa.Column('result', sa.VARCHAR(), nullable=True),
    sa.Column('competitor_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['competitor_id'], ['competitor.id'], name='fk_competitor_race'),
    sa.ForeignKeyConstraint(['race_id'], ['race.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('race_id', 'competitor_id', name='uq_race_competitor')
    )
    # ### end Alembic commands ###
