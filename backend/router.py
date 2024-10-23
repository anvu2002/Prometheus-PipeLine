from fastapi import Request, APIRouter
from loguru import logger
import json
from prometheus_client import get_gpu_memory_usage
from slack_notifier import send_slack_alert
from models import GPUUsage, SessionLocal

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/metrics/gpu")
def fetch_gpu_metrics():
    metrics = get_gpu_memory_usage()
    db = SessionLocal()
    for metric in metrics:
        gpu_id = metric['metric']['gpu']
        memory_used = float(metric['value'][1])

        # Store in database
        gpu_usage = GPUUsage(gpu_id=gpu_id, memory_used=memory_used)
        db.add(gpu_usage)

        # Send alert if memory usage exceeds 80%
        if memory_used > 8000:  # Example threshold
            send_slack_alert(gpu_id, memory_used)

    db.commit()
    db.close()
    return {"status": "success", "metrics": metrics}