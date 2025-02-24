from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.database.db import queue, SessionLocal
from app.models import Log
from app.models.requests import AddLogRequest


class IngestionService:

    @staticmethod
    def save_log_to_db(timestamp, level, message, service):
        session = SessionLocal()
        try:
            log_entry = Log(timestamp=timestamp, level=level, message=message, service=service)
            session.add(log_entry)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def add_log(log: AddLogRequest):
        queue.enqueue(IngestionService.save_log_to_db, log.timestamp, log.level, log.message, log.service)
