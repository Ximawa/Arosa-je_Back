from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy.exc import OperationalError

# Connection details without specifying the database
SQLALCHEMY_DATABASE_SERVER_URL = "mysql+pymysql://root:@localhost:3308/"
DATABASE_NAME = "arosaje"

# Attempt to connect to the server and create the database if it doesn't exist
engine_server = create_engine(SQLALCHEMY_DATABASE_SERVER_URL)
with engine_server.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"))
    conn.commit()

# Now, connect to the newly ensured database
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:@localhost:3308/{
    DATABASE_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

mapper_registry = registry()
Base = mapper_registry.generate_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
