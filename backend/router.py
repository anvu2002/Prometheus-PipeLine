from fastapi import Request, APIRouter, HTTPException
from loguru import logger
import json
from prometheus_client import get_gpu_memory_usage
from slack_notifier import send_slack_alert
from models import GPUUsage, UserAction, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from config.config import GPU_MAP

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/metrics/gpu")
async def fetch_gpu_metrics(request: Request):
    """
    Fetch and store GPU metrics, as well as user actions.
    Expected request body:
    {
        "target_gpu_id": "gpu_uuid", Targeted GPU
        "user_id": "<optional_user_id>",
        "action": "<optional_user_action>"
    }
    """
    try:
        gpu_metrics = dict()
        data = await request.json()
        if "target_gpu_id" not in data:
            raise HTTPException(status_code=400, detail="Missing required parameter 'target_gpu_id'")

        target_gpu_id: str = data["target_gpu_id"]

        metrics : list[list] = get_gpu_memory_usage()
        
        logger.debug(f"metrics = {metrics}")
        if not metrics:
            raise HTTPException(status_code=404, detail=f"No GPU Metrics was found!")

        # Initialize database session
        db: Session = SessionLocal()
        
        for metric in metrics:
            gpu_uuid = metric[0]['metric']['uuid']
            try:
                memory_used = round(float(metric[0]['value'][1]) * 100, 1)
            except ValueError:
                logger.error(f"Invalid memory value for GPU {gpu_uuid}: {metric[0]['value'][1]}")
                raise HTTPException(status_code=500, detail="Invalid memory value from Prometheus")
            
            gpu_metrics.update({gpu_uuid:memory_used})
            # Store GPU memory usage in the database
            gpu_usage = GPUUsage(gpu_id=gpu_uuid, memory_used=memory_used)
            db.add(gpu_usage)

        db.commit()

        logger.debug(f"gpu_metrics = {gpu_metrics}")

        # Alerting!
        if gpu_metrics[target_gpu_id] > 80:
            send_slack_alert(GPU_MAP[target_gpu_id], gpu_metrics)


    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        logger.error(f"Internal server error: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        if 'db' in locals():
            db.close()

    return {"status": "success", "metrics": metrics}

async def fetch_user_metrics(request: Request):
# Slack -- Interactive Messages -- Response Payload
    try:
        data = await request.json()
        if "user_id" in data and "action" in data:
            user_id = data["user_id"]
            action = data["action"]
            response_time = data.get("response_time", None)  # Optional response time

            # Store user action in the database
            user_action = UserAction(
                user_id=user_id,
                action=action,
                response_time=response_time if response_time else None,
                timestamp=datetime.utcnow()
            )
            # db.add(user_action)
    except Exception as e:
        logger.error(f"[User Metrics] eror: {e}")