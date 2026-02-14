from os import getenv
from dotenv import load_dotenv
import requests

load_dotenv()


url = getenv("URL")

headers = {
    "Authorization": getenv("BEARER"),
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

json_data = response.json()

values = [
    item["value"]
    for group in json_data["data"]
    if group["groupValue"] == "TrailerType"
    for item in group["groupData"]
]

with open("scrapped_data.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(values))

print("done")