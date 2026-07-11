import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Parse connection arguments safely. 
# Hosted Supabase database URLs often require SSL mode.
connect_args = {}
db_url = settings.DATABASE_URL

if "supabase" in db_url or "pooler.supabase" in db_url or "aws-" in db_url:
    connect_args["sslmode"] = "require"

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
