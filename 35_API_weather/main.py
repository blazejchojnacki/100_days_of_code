import requests
import json
import datetime

LATITUDE = "52.29"
LONGITUDE = "21.11"
API_KEY = "3bc81e0f4956687592dcec745f9b7c7c"
URL = "https://api.openweathermap.org/data/2.5/forecast"
parameters = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": API_KEY,
    "cnt": 4,
    "units": "metric"
}
date_now = datetime.datetime.now()
now_hour_str = f""

results = requests.get(URL, params=parameters)
results.raise_for_status()
json_result = json.loads(results.text)
print(json_result['list'][1])
