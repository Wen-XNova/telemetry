from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class MetricIngestRequest(BaseModel):
    device_id: str = Field(..., min_length=3, max_length=64, description="Unique device identifier")
    metric_type: str = Field(..., min_length=2, max_length=32, description="Type of metricrecorded")
    value: float = Field(..., description="Numeric value of the metric reading")
    timestamp: Optional[datetime] = Field(
        default=None,
        description="Event timestamp. Defaults to current server UTC time if omitted."
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional auxiliary payload context"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "device_id": "sensor-node-01",
                "metric_type": "temperature",
                "value": 23.8,
                "metadata": {"location": "rack-2b"}
            }
        }
    )