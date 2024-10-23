#Query the Prometheus server to fetch the current GPU VRAM usage metric
import requests

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

def get_gpu_memory_usage():
    metric = 'nvidia_smi_memory_used_bytes'
    response = requests.get(f"{PROMETHEUS_URL}?query={metric}")
    result = response.json()

    if result['status'] == 'success':
        return result['data']['result']
    else:
        raise Exception("Failed to fetch data from Prometheus")
