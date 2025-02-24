from pydantic import BaseModel
from datetime import datetime

from app.models import LogLevel


class AddLogRequest(BaseModel):
    timestamp: datetime
    level: LogLevel
    message: str
    service: str