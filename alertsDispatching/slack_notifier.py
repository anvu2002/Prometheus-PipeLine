# slack_notifier.py
import requests
from loguru import logger
from datetime import datetime
from prometheus_client import get_gpu_memory_usage



from config.config import SLACK_WEBHOOK_URL, GPU_MAP


def send_slack_alert(target_gpu_name, details:str, gpus_metrics:dict):
    formatted_metrics = "\n".join(
        f"{GPU_MAP[gpu_uuid]}: {usage}%" 
        for gpu_uuid, usage in gpus_metrics.items()
        if GPU_MAP[gpu_uuid] != target_gpu_name
    )

    try:
        payload ={
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"[ALERT] {target_gpu_name} Memory Threshold Reached",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Type:*\nEXHAUSTED_RESOURCE"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Created by:*\n<mailto:anvu6028@gmail.com|Advanced Observability Team>"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Details:*\n{details}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Available GPUs:*\n{formatted_metrics}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*When:*\n{datetime.now()}"
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Acknowledge"
                            },
                            "style": "primary",
                            "value": "click_me_123"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Report Issue"
                            },
                            "style": "danger",
                            "value": "click_me_123"
                        }
                    ]
                }
            ]
        }
        requests.post(SLACK_WEBHOOK_URL, json=payload)
    except Exception as e:
        logger.error(f"[Slack] Error sending message: {e}")


def send_slack_resolved(target_gpu_name, details, gpus_metrics: dict):
    formatted_metrics = "\n".join(
        f"{GPU_MAP[gpu_uuid]}: {usage}%" 
        for gpu_uuid, usage in gpus_metrics.items()
        # if GPU_MAP[gpu_uuid] != target_gpu_name
    )

    try:
        payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"[RESOLVED] {target_gpu_name} Memory Usage Back to Normal",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Type:*\nRESOURCE_OK"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Resolved by:*\n<mailto:anvu6028@gmail.com|Advanced Observability Team>"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Available GPUs:*\n{formatted_metrics}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*When:*\n{datetime.now()}"
                        }
                    ]
                }
            ]
        }
        requests.post(SLACK_WEBHOOK_URL, json=payload)
    except Exception as e:
        logger.error(f"[Slack] Error sending resolved message: {e}")
