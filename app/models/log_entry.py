from enum import Enum
from sqlalchemy import Column, String, DateTime, Enum as SAEnum, Integer, Index, literal_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func

from app.database.db import engine


# Enum for log levels
class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


class Base(DeclarativeBase):
    pass


# Log model
class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    level = Column(SAEnum(LogLevel), nullable=False)
    message = Column(String, nullable=False)
    service = Column(String, nullable=False)

    __table_args__ = (
    Index('message_search_idx', func.to_tsvector(literal_column("'english'"), message), postgresql_using='gin'),)


# Create tables
Base.metadata.create_all(bind=engine)
