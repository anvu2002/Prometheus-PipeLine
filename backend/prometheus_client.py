# prometheus_client.py
import requests

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

def get_gpu_memory_usage():
    query = 'nvidia_smi_memory_used_bytes'
    response = requests.get(f"{PROMETHEUS_URL}?query={query}")
    result = response.json()

    if result['status'] == 'success':
        return result['data']['result']
    else:
        raise Exception("Failed to fetch data from Prometheus")
