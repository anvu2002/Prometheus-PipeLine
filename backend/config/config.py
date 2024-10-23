import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

GPU_MAP = {
    "cf6c958c-ef27-8968-00a7-48f5112fe134":"GPU_0", 
    "da348d25-c816-68b6-b96f-ca942600529c":"GPU_1",
    "b0d81ee0-78c7-6d6d-a72f-85b95652e0b8":"GPU_2", 
    "92920a10-5401-2969-c105-cf7acb294699":"GPU_3" 
}
