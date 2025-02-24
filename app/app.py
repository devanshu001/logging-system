from datetime import datetime
from fastapi import FastAPI, Request, Response, Query, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError
from app.models import LogLevel
from app.models.error import NotFoundException
from app.models.requests import AddLogRequest
from app.services import QueryService
from app.services.ingestion_service import IngestionService


def create_app() -> FastAPI:
    app = FastAPI(swagger_ui_parameters={'tryItOutEnabled': True})

    @app.post('/logs')
    async def add_log(log: AddLogRequest):
        try:
            IngestionService.add_log(log)
            return {"status": "Log queued successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error queuing log: {str(e)}")

    @app.get("/logs")
    async def query_logs(start_time: datetime = Query(None),
                         end_time: datetime = Query(None),
                         service: str = Query(None),
                         level: LogLevel = Query(None),
                         search: str = Query(None)):
        try:
            return QueryService.get_logs(start_time, end_time, service, level, search)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

    @app.get("/logs/aggregations")
    async def aggregate_logs():
        try:
            result = QueryService.get_aggregations()
            return [{"service": r[0], "level": r[1], "count": r[2]} for r in result]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Aggregation error: {str(e)}")

    @app.get("/healthz")
    def health_check():
        return {"status": "ok"}

    @app.exception_handler(NotFoundException)
    async def not_found(request: Request, exc: NotFoundException):
        return Response(status_code=404)

    @app.get('/', include_in_schema=False)
    def root():
        return RedirectResponse('/docs')

    return app


app = create_app()
