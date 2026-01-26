import requests
import pandas as pd

TARGET_DATE = "2026-01-30"

url = "https://api.nasdaq.com/api/calendar/dividends"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Origin": "https://www.nasdaq.com",
    "Referer": "https://www.nasdaq.com/",
}

r = requests.get(url, params={"date": TARGET_DATE}, headers=headers)
rows = r.json()["data"]["calendar"]["rows"]

df = pd.DataFrame(rows)
df.to_csv(f"dividends_{TARGET_DATE}.csv", index=False)
