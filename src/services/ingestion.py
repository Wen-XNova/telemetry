import asyncio
from typing import List

from src.schemas.requests import MetricIngestRequest
from src.db.session import AsyncSessionLocal
from src.db.repository import MetricRepository


class IngestionService:
    @staticmethod
    async def process_payload_background(payload: MetricIngestRequest):
        await asyncio.sleep(1)

        async with AsyncSessionLocal() as session:
            repo = MetricRepository(session)
            db_record = await repo.create_metric(payload)
            print(f"[INFO] Persisted {db_record.metric_type} (ID: {db_record.id})")

    @staticmethod
    async def process_batch_background(payloads: List[MetricIngestRequest]):
        async with AsyncSessionLocal() as session:
            repo = MetricRepository(session)

            for payload in payloads:
                await repo.create_metric(payload)

            print(f"[INFO] Batch processed {len(payloads)} records.")