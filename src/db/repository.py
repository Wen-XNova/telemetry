from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.metrics import Metric
from src.schemas.requests import MetricIngestRequest


class MetricRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_metric(self, payload: MetricIngestRequest) -> Metric:
        # exclude_unset prevents overwriting default values (like timestamps) with None
        new_metric = Metric(**payload.model_dump(exclude_unset=True))

        self.session.add(new_metric)
        await self.session.commit()
        await self.session.refresh(new_metric)

        return new_metric

    async def get_recent_metrics(self, limit: int = 50):
        query = select(Metric).order_by(Metric.timestamp.desc()).limit(limit)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def update_metric(self, metric_id: int, payload: MetricIngestRequest) -> Metric | None:
        metric = await self.session.get(Metric, metric_id)
        if not metric:
            return None

        # Update the core fields
        metric.device_id = payload.device_id
        metric.metric_type = payload.metric_type
        metric.value = payload.value

        if payload.timestamp:
            metric.timestamp = payload.timestamp

        await self.session.commit()
        await self.session.refresh(metric)

        return metric

    async def delete_metric(self, metric_id: int) -> bool:
        metric = await self.session.get(Metric, metric_id)
        if not metric:
            return False

        await self.session.delete(metric)
        await self.session.commit()

        return True