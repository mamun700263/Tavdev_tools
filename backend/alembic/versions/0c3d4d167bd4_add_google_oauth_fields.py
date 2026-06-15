"""add google oauth fields

Revision ID: 0c3d4d167bd4
Revises: 9716076540e3
Create Date: 2026-06-15 12:20:06.427660

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c3d4d167bd4'
down_revision: Union[str, Sequence[str], None] = '9716076540e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

auth_provider_enum = sa.Enum(
    "LOCAL",
    "GOOGLE",
    name="auth_provider_enum"
)


def upgrade() -> None:
    # 1. CREATE ENUM TYPE FIRST
    auth_provider_enum.create(op.get_bind(), checkfirst=True)

    # 2. ADD COLUMN using existing enum
    op.add_column(
        'accounts',
        sa.Column(
            'auth_provider',
            auth_provider_enum,
            nullable=False,
            server_default='LOCAL'
        )
    )

    # 3. GOOGLE SUB COLUMN
    op.add_column(
        'accounts',
        sa.Column('google_sub', sa.String(length=255), nullable=True)
    )

    # 4. INDEXES
    op.create_index(
        op.f('ix_accounts_auth_provider'),
        'accounts',
        ['auth_provider'],
        unique=False
    )

    op.create_index(
        op.f('ix_accounts_google_sub'),
        'accounts',
        ['google_sub'],
        unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_accounts_google_sub'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_auth_provider'), table_name='accounts')

    op.drop_column('accounts', 'google_sub')
    op.drop_column('accounts', 'auth_provider')

    auth_provider_enum.drop(op.get_bind(), checkfirst=True)