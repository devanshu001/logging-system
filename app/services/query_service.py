
from app.database.db import SessionLocal
from app.models.log_entry import Log
from typing import List
from sqlalchemy import func


class QueryService:

    @staticmethod
    def get_logs( start_time, end_time, service, level, search) -> List[Log]:
        session: SessionLocal = SessionLocal()
        query = session.query(Log)
        if start_time:
            query = query.filter(Log.timestamp >= start_time)
        if end_time:
            query = query.filter(Log.timestamp <= end_time)
        if service:
            query = query.filter(Log.service == service)
        if level:
            query = query.filter(Log.level == level)
        if search:
            query = query.filter(Log.message.match(search))
        logs = query.all()
        session.close()
        return logs

    @staticmethod
    def get_aggregations():
        session: SessionLocal = SessionLocal()
        result = session.query(Log.service, Log.level, func.count(Log.id)).group_by(Log.service, Log.level).all()
        session.close()
        return result
