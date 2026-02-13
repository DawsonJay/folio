"""Initial analytics_events table

Revision ID: 001
Revises: 
Create Date: 2026-02-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'analytics_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('session_id', sa.String(), nullable=True),
        sa.Column('question_text', sa.Text(), nullable=True),
        sa.Column('answer_text', sa.Text(), nullable=True),
        sa.Column('confidence', sa.String(), nullable=True),
        sa.Column('top_score', sa.Float(), nullable=True),
        sa.Column('response_time_ms', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('event_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analytics_events_id'), 'analytics_events', ['id'], unique=False)
    op.create_index(op.f('ix_analytics_events_event_type'), 'analytics_events', ['event_type'], unique=False)
    op.create_index(op.f('ix_analytics_events_timestamp'), 'analytics_events', ['timestamp'], unique=False)
    op.create_index(op.f('ix_analytics_events_session_id'), 'analytics_events', ['session_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_analytics_events_session_id'), table_name='analytics_events')
    op.drop_index(op.f('ix_analytics_events_timestamp'), table_name='analytics_events')
    op.drop_index(op.f('ix_analytics_events_event_type'), table_name='analytics_events')
    op.drop_index(op.f('ix_analytics_events_id'), table_name='analytics_events')
    op.drop_table('analytics_events')

