from logging.config import fileConfig
import os
from sqlalchemy import create_engine
from alembic import context

from database import Base
from models import User, Product, Order


config = context.config
fileConfig(config.config_file_name)

# импорт Base из вашего приложения
target_metadata = Base.metadata

url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@postgres:5432/myapp")

def run_migrations_offline():
  
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    
    connectable = create_engine(url)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
