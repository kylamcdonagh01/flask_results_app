"""initial migration

Revision ID: f250a62dbaeb
Revises: 
Create Date: 2024-11-24 16:57:41.596724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f250a62dbaeb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('competitor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=15), nullable=True),
    sa.Column('last_name', sa.String(length=25), nullable=True),
    sa.Column('club', sa.String(length=100), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_competitor_races')
    )
    with op.batch_alter_table('competitor', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_competitor_first_name'), ['first_name'], unique=True)
        batch_op.create_index(batch_op.f('ix_competitor_last_name'), ['last_name'], unique=True)

    op.create_table('race',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('race_date', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id',name='pk_races_competitors')
    )
    op.create_table('user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_users'),
    sa.UniqueConstraint('username', name='uq_user')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('race')
    with op.batch_alter_table('competitor', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_competitor_last_name'))
        batch_op.drop_index(batch_op.f('ix_competitor_first_name'))

    op.drop_table('competitor')
    # ### end Alembic commands ###
