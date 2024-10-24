#Query the Prometheus server to fetch the current GPU VRAM usage metric
import requests

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

def get_gpu_memory_usage():
    res = []
    gpu_uuid = ['92920a10-5401-2969-c105-cf7acb294699','b0d81ee0-78c7-6d6d-a72f-85b95652e0b8', 'cf6c958c-ef27-8968-00a7-48f5112fe134','da348d25-c816-68b6-b96f-ca942600529c']

    for id in gpu_uuid:
        query = f'nvidia_smi_memory_used_bytes{{uuid="{id}"}} / nvidia_smi_memory_total_bytes{{uuid="{id}"}}'
        response = requests.get(f"{PROMETHEUS_URL}?query={query}")
        result = response.json()
        
        if result['status'] == 'success':
            res.append(result['data']['result'])
        else:
            raise Exception("Failed to fetch data from Prometheus")
    return res
