import csv
import io
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.requests import MetricIngestRequest
from src.schemas.responses import IngestReceiptResponse, MetricResponse
from src.services.ingestion import IngestionService
from src.db.session import get_db
from src.db.repository import MetricRepository

router = APIRouter()


@router.post("/ingest", response_model=IngestReceiptResponse, status_code=202)
async def ingest_metric(
        payload: MetricIngestRequest,
        background_tasks: BackgroundTasks
):
    # Fire & forget - let the background worker handle the DB write
    background_tasks.add_task(IngestionService.process_payload_background, payload)

    return IngestReceiptResponse(
        status="accepted",
        device_id=payload.device_id,
        queued_at=datetime.now(timezone.utc)
    )


@router.post("/ingest/batch", status_code=202)
async def ingest_batch(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Please upload a valid CSV file.")

    raw_data = await file.read()
    decoded_csv = raw_data.decode('utf-8')

    reader = csv.DictReader(io.StringIO(decoded_csv))
    batch = []

    try:
        for row in reader:
            # Let Pydantic handle the type casting & validation
            batch.append(MetricIngestRequest(
                device_id=row['device_id'],
                metric_type=row['metric_type'],
                value=float(row['value'])
            ))
    except KeyError as err:
        raise HTTPException(status_code=400, detail=f"Your CSV is missing a required column: {err}")
    except ValueError:
        raise HTTPException(status_code=400, detail="Found invalid data types in the CSV. Check your value column.")

    background_tasks.add_task(IngestionService.process_batch_background, batch)

    return {
        "status": "accepted",
        "message": f"Queued {len(batch)} records for background processing."
    }


@router.get("/metrics", response_model=List[MetricResponse])
async def get_metrics(
        limit: int = 50,
        session: AsyncSession = Depends(get_db)
):
    repo = MetricRepository(session)
    return await repo.get_recent_metrics(limit=limit)


@router.put("/metrics/{metric_id}", response_model=MetricResponse)
async def update_metric(
        metric_id: int,
        payload: MetricIngestRequest,
        session: AsyncSession = Depends(get_db)
):
    repo = MetricRepository(session)
    updated = await repo.update_metric(metric_id, payload)

    if not updated:
        raise HTTPException(status_code=404, detail="Metric not found.")

    return updated


@router.delete("/metrics/{metric_id}", status_code=204)
async def delete_metric(
        metric_id: int,
        session: AsyncSession = Depends(get_db)
):
    repo = MetricRepository(session)

    if not await repo.delete_metric(metric_id):
        raise HTTPException(status_code=404, detail="Metric not found.")

    return None