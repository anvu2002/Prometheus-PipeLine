# slack_notifier.py
import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/your/webhook/url"

def send_slack_alert(gpu_id, memory_used):
    message = f"⚠️ GPU {gpu_id} is using {memory_used} MB of memory. Please check your usage!"
    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=payload)
