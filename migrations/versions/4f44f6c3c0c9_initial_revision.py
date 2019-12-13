"""initial revision

Revision ID: 4f44f6c3c0c9
Revises: 
Create Date: 2019-12-13 07:34:55.556039

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4f44f6c3c0c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('candidate_stage',
                    sa.Column('time', sa.DateTime(), nullable=False),
                    sa.Column('applicant_id', sa.Integer(), nullable=False),
                    sa.Column('stage',
                              sa.Enum('APPLIED', 'SCREENED', 'REJECTED_1', 'INTERVIEWED', 'REJECTED_2',
                                      'GIVEN_OFFER',
                                      'DECLINED', 'HIRED', name='pipelinestage'), nullable=False),
                    sa.PrimaryKeyConstraint('applicant_id', 'stage')
                    )
    op.create_index('candidate_stage_time_idx', 'candidate_stage', ['time'])


def downgrade():
    op.drop_table('candidate_stage')
