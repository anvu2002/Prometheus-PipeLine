from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token="SLACK_TOKEN")

channel_id = "gpu-monitoring"

bot_name = "GPU-bot"

message = "sup brooooo"

try:
    response = client.chat_postMessage(channel=channel_id, text=message,username=bot_name)
    print("Message sent successfully!")
except SlackApiError as e:
    print(f"Error sending message: {e}")