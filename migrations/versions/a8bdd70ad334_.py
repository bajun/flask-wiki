"""empty message

Revision ID: a8bdd70ad334
Revises: 
Create Date: 2018-12-22 02:05:52.466965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8bdd70ad334'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('content',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('revision_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['revision_id'], ['revision.id'], name='revision_fk', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('page',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('revision_latest', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_page_title'), 'page', ['title'], unique=True)
    op.create_table('revision',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('page_id', sa.Integer(), nullable=True),
    sa.Column('content_id', sa.Integer(), nullable=True),
    sa.Column('actual', sa.Boolean(), nullable=True),
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['content.id'], name='content_fk', use_alter=True),
    sa.ForeignKeyConstraint(['page_id'], ['page.id'], name='page_fk', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revision')
    op.drop_index(op.f('ix_page_title'), table_name='page')
    op.drop_table('page')
    op.drop_table('content')
    # ### end Alembic commands ###
