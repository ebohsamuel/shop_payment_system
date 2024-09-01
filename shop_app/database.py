from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base


# "postgresql://postgres:PG/eng1102493@localhost:5432/shop_application.db" for local server"
DATABASE_URL = "sqlite:///./shop_application.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
