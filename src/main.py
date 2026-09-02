from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from src.api.v1.endpoints.ingestion import router as ingestion_router
from src.db.session import engine
from src.models.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(
    title="Telemetry Ingestion Engine",
    description="Asynchronous data pipeline and monitoring dashboard",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ingestion_router, prefix="/api/v1")

templates = Jinja2Templates(directory="src/templates")

@app.get("/", include_in_schema=False)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )