# Dummy .env file, only for initial alembic configuration

from alembic import context

# Dummy metadata (empty)
target_metadata = None

def run_migrations_offline():
    """Run migrations in offline mode (does nothing)."""
    context.configure(url="sqlite:///./dummy.db", literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in online mode (does nothing)."""
    # Create a dummy connection object
    from sqlalchemy import create_engine
    connectable = create_engine("sqlite:///./dummy.db")
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()