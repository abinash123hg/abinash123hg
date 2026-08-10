import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

USERNAME = "abinash123hg"

url = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    level = cell.get("data-level")

    if date and level is not None:
        days.append({
            "date": date,
            "level": int(level)
        })

if not days:
    raise RuntimeError("No contribution data found.")

os.makedirs("data", exist_ok=True)

output = {
    "username": USERNAME,
    "updated": datetime.now().isoformat(),
    "days": days
}

with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Saved {len(days)} contribution days.")