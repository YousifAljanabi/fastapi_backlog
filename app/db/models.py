from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
