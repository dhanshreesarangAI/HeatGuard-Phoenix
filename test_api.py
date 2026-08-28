import requests

# Your FortyGuard API Key
API_KEY = "2430d857a786cd426c695f1df0639939"

url = "https://api.fortyguard.com/v1/heatmap"

headers = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

# Downtown Phoenix ka small area (test ke liye)
payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-112.0850, 33.4400],
                        [-112.0700, 33.4400],
                        [-112.0700, 33.4550],
                        [-112.0850, 33.4550],
                        [-112.0850, 33.4400]
                    ]]
                }
            }
        ]
    },
    "date_time": {
        "start_date": "2026-08-23",
        "start_time": "14:00",
        "filter_type": 1
    },
    "granularity": 100
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print("SUCCESS!")
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")