import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# ? Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))