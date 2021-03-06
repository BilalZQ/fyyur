"""empty message

Revision ID: 9cedd721d165
Revises: a5f9ae20f9fa
Create Date: 2021-07-04 17:12:35.229249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cedd721d165'
down_revision = 'a5f9ae20f9fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('artist_id', sa.Integer(), nullable=True),
                    sa.Column('venue_id', sa.Integer(), nullable=True),
                    sa.Column('start_time', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
                    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('show')
    # ### end Alembic commands ###
