"""kaikang

Revision ID: ab14776f8ce1
Revises: 
Create Date: 2021-03-06 14:07:26.115510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab14776f8ce1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('auditor', sa.String(length=64), nullable=False),
    sa.Column('tenant', sa.String(length=64), nullable=False),
    sa.Column('part1_score', sa.Integer(), nullable=True),
    sa.Column('part2_score', sa.Integer(), nullable=True),
    sa.Column('part3_score', sa.Integer(), nullable=True),
    sa.Column('part4_score', sa.Integer(), nullable=True),
    sa.Column('part5_score', sa.Integer(), nullable=True),
    sa.Column('total_score', sa.Integer(), nullable=True),
    sa.Column('remarks', sa.String(length=64), nullable=False),
    sa.Column('rectification', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_timestamp'), 'audit', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_audit_timestamp'), table_name='audit')
    op.drop_table('audit')
    # ### end Alembic commands ###