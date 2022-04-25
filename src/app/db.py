import os

from databases import Database
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    ForeignKey,
    create_engine
)
from sqlalchemy.sql import func


DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Notes table in db
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# Regions table in db
regions = Table(
    "regions",
    metadata,
    Column("id", Integer, unique=True, primary_key=True),
    Column("title", String(70), unique=True, nullable=False),
)

# Dialects table in db
dialects = Table(
    "dialects",
    metadata,
    Column("id", Integer, unique=True, primary_key=True),
    Column("title", String(50), unique=True, nullable=False),
    Column("description", String(200), nullable=False),
)

# Dialects table in db
relationships = Table(
    "relationships",
    metadata,
    Column("region_id", Integer, ForeignKey("regions.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("dialect_id", Integer, ForeignKey("dialects.id", ondelete="CASCADE"), nullable=False, index=True),
)

# Databases query builder
database = Database(DATABASE_URL)
