from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class IngestReceiptResponse(BaseModel):
    status: str = Field(default="accepted", description="Processing status of the payload")
    device_id: str = Field(..., description="Acknowledged device identifier")
    queued_at: datetime = Field(..., description="UTC timestamp when the event was received")

class MetricResponse(BaseModel):
    id: int
    device_id: str
    metric_type: str
    value: float
    timestamp: datetime
    created_at: datetime

    # Allow Pydantic to read data directly from SQLAlchemy ORM models
    model_config = ConfigDict(from_attributes=True)