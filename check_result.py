import requests
import time

API_KEY = "2430d857a786cd426c695f1df0639939"
activity_id = "d02998b9-8668-4cd7-b373-e74b5bc42928"

status_url = f"https://api.fortyguard.com/v1/status/{activity_id}"
headers = {"api-key": API_KEY}

response = requests.get(status_url, headers=headers)
print("Full response:")
print(response.json())