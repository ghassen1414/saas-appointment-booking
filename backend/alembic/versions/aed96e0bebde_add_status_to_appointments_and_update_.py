"""add status to appointments and update constraints

Revision ID: aed96e0bebde
Revises: a89da62d6efe
Create Date: 2025-05-29 17:10:50.740950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aed96e0bebde'
down_revision: Union[str, None] = 'a89da62d6efe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###

    # --- Handle service_name alteration with index ---
    # 1. Drop the existing index on service_name
    op.drop_index('ix_appointments_service_name', table_name='appointments')

    # 2. Alter the service_name column
    op.alter_column('appointments', 'service_name',
               existing_type=sa.VARCHAR(length=255, collation='SQL_Latin1_General_CP1_CI_AS'), # Ensure collation matches if it was explicitly set
               nullable=False)

    # 3. Recreate the index on service_name
    op.create_index('ix_appointments_service_name', 'appointments', ['service_name'], unique=False)
    # --- End service_name handling ---

    # Alter owner_id (assuming no problematic index here, but if there was, similar drop/recreate needed)
    op.alter_column('appointments', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # Add the status column
    op.add_column('appointments', sa.Column('status', sa.Enum('PENDING_CONFIRMATION', 'CONFIRMED', 'CANCELLED_BY_USER', 'CANCELLED_BY_ADMIN', 'COMPLETED', 'NO_SHOW', name='appointmentstatus'),
                                          nullable=False,
                                          server_default='PENDING_CONFIRMATION'))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('appointments', 'status') # This will also drop the enum type if it was created by alembic

    op.alter_column('appointments', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=True) # Revert to nullable=True

    # --- Handle service_name downgrade with index ---
    # 1. Drop the index
    op.drop_index('ix_appointments_service_name', table_name='appointments')

    # 2. Alter the column back to nullable=True
    op.alter_column('appointments', 'service_name',
               existing_type=sa.VARCHAR(length=255, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True) # Revert to nullable=True

    # 3. Recreate the index
    op.create_index('ix_appointments_service_name', 'appointments', ['service_name'], unique=False)
    # --- End service_name handling ---

    # ### end Alembic commands ###