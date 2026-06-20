from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:1609@localhost/helper"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)