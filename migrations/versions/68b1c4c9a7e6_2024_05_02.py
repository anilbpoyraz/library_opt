"""2024-05-02

Revision ID: 68b1c4c9a7e6
Revises: None
Create Date: 2024-05-02 17:12:30.705386

"""

# revision identifiers, used by Alembic.
revision = '68b1c4c9a7e6'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import context


def upgrade():
    context.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    """schema upgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('author', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('placement', sa.String(), nullable=False),
    sa.Column('is_available', sa.Boolean(), server_default='t', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_author'), 'books', ['author'], unique=False)
    op.create_index(op.f('ix_books_category'), 'books', ['category'], unique=False)
    op.create_index(op.f('ix_books_created_at'), 'books', ['created_at'], unique=False)
    op.create_index(op.f('ix_books_is_available'), 'books', ['is_available'], unique=False)
    op.create_index(op.f('ix_books_placement'), 'books', ['placement'], unique=False)
    op.create_index(op.f('ix_books_title'), 'books', ['title'], unique=False)
    op.create_table('patrons',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('overdue_count', sa.Integer(), server_default='0', nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='t', nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_patrons_created_at'), 'patrons', ['created_at'], unique=False)
    op.create_index(op.f('ix_patrons_email'), 'patrons', ['email'], unique=False)
    op.create_index(op.f('ix_patrons_first_name'), 'patrons', ['first_name'], unique=False)
    op.create_index(op.f('ix_patrons_is_active'), 'patrons', ['is_active'], unique=False)
    op.create_index(op.f('ix_patrons_last_name'), 'patrons', ['last_name'], unique=False)
    op.create_index(op.f('ix_patrons_password'), 'patrons', ['password'], unique=False)
    op.create_table('tokens',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='t', nullable=False),
    sa.Column('patron_id', postgresql.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['patron_id'], ['patrons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_is_active'), 'tokens', ['is_active'], unique=False)
    op.create_index(op.f('ix_tokens_patron_id'), 'tokens', ['patron_id'], unique=False)
    op.create_index(op.f('ix_tokens_token'), 'tokens', ['token'], unique=False)
    op.create_table('transactions',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('book_id', postgresql.UUID(), nullable=True),
    sa.Column('patron_id', postgresql.UUID(), nullable=True),
    sa.Column('checkout_date', sa.DateTime(), nullable=True),
    sa.Column('return_date', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='t', nullable=False),
    sa.Column('user_return_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['patron_id'], ['patrons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_is_active'), 'transactions', ['is_active'], unique=False)
    op.create_table('checked_out_books',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('transaction_id', postgresql.UUID(), nullable=True),
    sa.Column('is_return_on_time', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('transaction_id')
    )
    op.create_index(op.f('ix_checked_out_books_is_return_on_time'), 'checked_out_books', ['is_return_on_time'], unique=False)
    op.create_table('overdue_books',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('transaction_id', postgresql.UUID(), nullable=True),
    sa.Column('overdue_days', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('transaction_id')
    )
    op.create_index(op.f('ix_overdue_books_overdue_days'), 'overdue_books', ['overdue_days'], unique=False)
    # ### end Alembic commands ###


def schema_downgrades():
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_overdue_books_overdue_days'), table_name='overdue_books')
    op.drop_table('overdue_books')
    op.drop_index(op.f('ix_checked_out_books_is_return_on_time'), table_name='checked_out_books')
    op.drop_table('checked_out_books')
    op.drop_index(op.f('ix_transactions_is_active'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_tokens_token'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_patron_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_is_active'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_patrons_password'), table_name='patrons')
    op.drop_index(op.f('ix_patrons_last_name'), table_name='patrons')
    op.drop_index(op.f('ix_patrons_is_active'), table_name='patrons')
    op.drop_index(op.f('ix_patrons_first_name'), table_name='patrons')
    op.drop_index(op.f('ix_patrons_email'), table_name='patrons')
    op.drop_index(op.f('ix_patrons_created_at'), table_name='patrons')
    op.drop_table('patrons')
    op.drop_index(op.f('ix_books_title'), table_name='books')
    op.drop_index(op.f('ix_books_placement'), table_name='books')
    op.drop_index(op.f('ix_books_is_available'), table_name='books')
    op.drop_index(op.f('ix_books_created_at'), table_name='books')
    op.drop_index(op.f('ix_books_category'), table_name='books')
    op.drop_index(op.f('ix_books_author'), table_name='books')
    op.drop_table('books')
    # ### end Alembic commands ###


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    try:
        from os import walk
        path = 'migrations/seeds/'
        files = []
        for dirpath, dirnames, filenames in walk(path):
            files.extend(filenames)
            break
        for file in files:
            with open(path + file) as json_file:
                context.execute(json_file.read())
    except Exception as e:
        print(e)


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass