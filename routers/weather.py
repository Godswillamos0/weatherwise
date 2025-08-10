from fastapi import APIRouter, Query
import httpx
import os
from dotenv import load_dotenv
from typing import Dict, List, Any

load_dotenv()

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)
API_KEY = os.getenv("WEATHER_API_KEY") or "75c90856662def9a21913a79ed25f920"


async def fetch_days(city: str) -> Dict[str, List[Dict[str, Any]]]:
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        return {}

    data = response.json()
    forecast_by_day: Dict[str, List[Dict[str, Any]]] = {}

    for entry in data["list"]:
        dt_txt = entry["dt_txt"]
        date = dt_txt.split(" ")[0]
        weather_desc = entry["weather"][0]["description"]
        main = entry["main"]

        forecast_by_day.setdefault(date, []).append({
            "time": dt_txt,
            "description": weather_desc,
            "temp": main["temp"],
            "humidity": main["humidity"],
            "pressure": main["pressure"]
        })
    #print(f"Fetched weather data for {city}: {forecast_by_day}")
    return forecast_by_day


# -----------------------------
# ✅ API endpoint: Filter suitable election days
# -----------------------------
@router.get("/ideal-election-days")
async def get_ideal_election_days(
    city: str = Query("Akure,NG", description="City name (default is Akure, Nigeria)")
):
    def is_ideal_weather(description: str) -> bool:
        description = description.lower()
        bad_keywords = ["rain", "shower", "thunderstorm", "drizzle"]
        return not any(bad in description for bad in bad_keywords)

    forecast_by_day = await fetch_days(city)

    if not forecast_by_day:
        return {"error": "Could not fetch weather data. Check city name or API key."}

    ideal_days_summary = []

    for day, intervals in forecast_by_day.items():
        # Filter only intervals with good weather
        good_intervals = [
            i for i in intervals if is_ideal_weather(i["description"])
        ]

        if len(good_intervals) >= 4:
            avg_temp = round(sum(i["temp"] for i in good_intervals) / len(good_intervals), 1)
            avg_humidity = round(sum(i["humidity"] for i in good_intervals) / len(good_intervals), 1)
            avg_pressure = round(sum(i["pressure"] for i in good_intervals) / len(good_intervals), 1)
            descriptions = list({i["description"] for i in good_intervals})

            ideal_days_summary.append({
                "date": day,
                "average_temperature": avg_temp,
                "average_humidity": avg_humidity,
                "average_pressure": avg_pressure,
                "weather_conditions": descriptions
            })

    return {
        "city": city,
        "ideal_election_days": ideal_days_summary or []
    }
