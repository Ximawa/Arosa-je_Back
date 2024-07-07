from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import registry

# Example using pymysql
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3308/arosaje"

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
