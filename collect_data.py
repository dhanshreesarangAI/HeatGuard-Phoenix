import requests
import time
import pandas as pd
from datetime import datetime

API_KEY = "2430d857a786cd426c695f1df0639939"

AREAS = {
    "Downtown Phoenix": [-112.0850, 33.4400, -112.0700, 33.4550],
    "Scottsdale": [-111.9300, 33.4900, -111.9150, 33.5050],
    "Tempe": [-111.9450, 33.4150, -111.9300, 33.4300],
    "Mesa": [-111.8350, 33.4100, -111.8200, 33.4250],
    "Glendale": [-112.1950, 33.5350, -112.1800, 33.5500]
}

def submit_request(area_name, coords):
    url = "https://api.fortyguard.com/v1/heatmap"
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    
    min_lon, min_lat, max_lon, max_lat = coords
    
    payload = {
        "polygon_aoi": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [min_lon, min_lat],
                        [max_lon, min_lat],
                        [max_lon, max_lat],
                        [min_lon, max_lat],
                        [min_lon, min_lat]
                    ]]
                }
            }]
        },
        "date_time": {
            "start_date": "2025-07-15",
            "start_time": "14:00",
            "filter_type": 1
        },
        "granularity": 100
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["data"]["activity_id"]
    else:
        print(f"Error submitting {area_name}: {response.text}")
        return None

def check_status(area_name, activity_id):
    url = f"https://api.fortyguard.com/v1/status/{activity_id}"
    headers = {"api-key": API_KEY}
    
    for _ in range(30):
        response = requests.get(url, headers=headers)
        data = response.json()["data"]
        status = data["status"].lower()
        
        if status in ("completed", "succeeded"):
            result = data.get("result", {})
            
            print(f"  DEBUG - result top-level keys: {list(result.keys())}")
            if "stats_data" in result:
                print(f"  DEBUG - stats_data keys: {list(result['stats_data'].keys())}")
            
            stats = None
            
            # Method 1: Direct path
            try:
                stats = result["stats_data"]["temperature_stats"]
            except (KeyError, TypeError):
                pass
            
            # Method 2: Calculate from map_data (guaranteed fallback)
            if stats is None and "map_data" in result:
                try:
                    temps = [f["properties"]["average_temperature"] 
                             for f in result["map_data"]["features"]]
                    if temps:
                        stats = {
                            "mean": sum(temps) / len(temps),
                            "minimum": min(temps),
                            "maximum": max(temps)
                        }
                        print(f"  ℹ️ Calculated stats from map_data ({len(temps)} tiles)")
                except (KeyError, TypeError) as e:
                    print(f"  Error calculating from map_data: {e}")
            
            if stats is None:
                print(f"  ⚠️ Could not extract stats for {area_name}")
                print(f"  Full result: {result}")
                return None
            
            return stats
            
        elif status in ("failed", "error"):
            print(f"  ❌ Task failed for {area_name}")
            return None
        time.sleep(5)
    
    print(f"  ⏱️ Timeout waiting for {area_name}")
    return None

# Main collection loop
results = []

for area_name, coords in AREAS.items():
    print(f"Fetching data for {area_name}...")
    activity_id = submit_request(area_name, coords)
    
    if activity_id:
        stats = check_status(area_name, activity_id)
        if stats:
            results.append({
                "area": area_name,
                "avg_temp": stats["mean"],
                "min_temp": stats["minimum"],
                "max_temp": stats["maximum"],
                "date": "2026-08-27",
                "time": "14:00"
            })
            print(f"  ✅ {area_name}: {stats['mean']:.2f}°C")
        else:
            print(f"  ❌ Failed to get data for {area_name}")
    
    time.sleep(2)

# Save to CSV
if results:
    df = pd.DataFrame(results)
    df.to_csv("phoenix_heat_data.csv", index=False)
    print("\n✅ Data saved to phoenix_heat_data.csv")
    print(df)
else:
    print("\n❌ No data collected. Check errors above.")