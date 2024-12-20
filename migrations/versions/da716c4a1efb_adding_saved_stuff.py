"""adding saved stuff

Revision ID: da716c4a1efb
Revises: abef92cac30e
Create Date: 2024-11-25 13:12:49.439029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da716c4a1efb'
down_revision = 'abef92cac30e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_competitor',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('competitor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['competitor_id'], ['competitor.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'competitor_id')
    )
    op.create_table('user_race',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('race_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['race_id'], ['race.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'race_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_race')
    op.drop_table('user_competitor')
    # ### end Alembic commands ###
