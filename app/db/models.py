import enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

Base = declarative_base()


class EpicStatus(enum.Enum):
    OPEN = "open"
    DONE = "done"

class TaskStatus(enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


class Epic(Base):
    __tablename__ = "epics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, unique=True)
    owner_email = Column(String, nullable=False)
    status = Column(Enum(EpicStatus), default=EpicStatus.OPEN)

    tasks = relationship("Task", back_populates="epic", cascade="all, delete")



class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    epic_id = Column(UUID(as_uuid=True), ForeignKey("epics.id"), nullable=False)

    hours_estimate = Column(Integer, nullable=False)
    hours_spent = Column(Integer, nullable=False, default=0)

    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)

    epic = relationship("Epic", back_populates="tasks")
