import os
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    )
from sqlalchemy.sql import func
from databases import Database


DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

urls = Table(
    'urls',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('origin', String(250)),
    Column('shorten', String(250)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

database = Database(DATABASE_URI)
