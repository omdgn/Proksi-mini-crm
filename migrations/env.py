# migrations/env.py
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ---- Proje kökünü PYTHONPATH'e ekle ----
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ---- Artık app.* import edebiliriz ----
from app.config.settings import settings
from app.config.db import Base
# Modeller metadata'ya eklensin diye importla (autogenerate bunları görsün)
from app.models import user_model, note_model  # noqa: F401

# Alembic config objesi
config = context.config

# .ini içindeki sqlalchemy.url boş; burada .env'den gelen URL'yi veriyoruz:
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Hedef metadata
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,      # kolon tipi değişikliklerini de algıla
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
