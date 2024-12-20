"""Add competitor_race table

Revision ID: 86f1939b5fd1
Revises: 565d46c0186d
Create Date: 2024-11-24 19:29:00.801340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86f1939b5fd1'
down_revision = '565d46c0186d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('competitor_races',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('competitor_id', sa.Integer(), nullable=False),
    sa.Column('race_id', sa.Integer(), nullable=False),
    sa.Column('result', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['competitor_id'], ['competitor.id'], name='fk_competitor_race'),
    sa.ForeignKeyConstraint(['race_id'], ['race.id'], name='fk_competitor_race'),
    sa.PrimaryKeyConstraint('id', name='pk_competitor_race')
    )
    op.drop_table('competitor_race')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('competitor_race',
    sa.Column('competitor_id', sa.INTEGER(), nullable=False),
    sa.Column('race_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['competitor_id'], ['competitor.id'], name='fk_competitor_race' ),
    sa.ForeignKeyConstraint(['race_id'], ['race.id'], name='fk_race_competitor'),
    sa.PrimaryKeyConstraint('competitor_id', 'race_id', name='pk_competitor_race')
    )
    op.drop_table('competitor_races')
    # ### end Alembic commands ###
