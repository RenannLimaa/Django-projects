import datetime
from collections import defaultdict

import requests
from django.shortcuts import render
from django.template.defaulttags import register


def index(request):
    API_KEY = (
        open("/home/renan/programming/Django/weather_project/API_KEY", "r")
        .read()
        .strip()
    )
    current_weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}"
    )
    forecast_url = (
        "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&appid={}"
    )

    if request.method == "POST":
        city = request.POST.get("city")

        weather_data, daily_forecasts = fetch_weather(city, API_KEY, current_weather_url, forecast_url)
        print(daily_forecasts)
        context = {
            "weather_data": weather_data,
            "daily_forecast": daily_forecasts
        }

        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")


def fetch_weather(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response["coord"]["lat"], response["coord"]["lon"]

    weather_data = {
        "city": city,
        "temperature": round(response["main"]["temp"], 2),
        "description": response["weather"][0]["description"],
        "icon": response["weather"][0]["icon"],
    }

    forecast_response = requests.get(
        forecast_url.format(lat, lon, api_key)).json()
    
    forecast_data = {}

    for daily_data in forecast_response["list"][:40]:
        dt_timestamp = datetime.datetime.fromtimestamp(daily_data["dt"])
        day_of_week = dt_timestamp.strftime("%A")

        if day_of_week not in forecast_data:
            forecast_data[day_of_week] = []

        forecast_data[day_of_week].append(
            {
                "date": dt_timestamp.date(),
                "day": day_of_week,
                "time": dt_timestamp.strftime("%H:%M"),
                "min_temp": round(daily_data["main"]["temp_min"], 2),
                "max_temp": round(daily_data["main"]["temp_max"], 2),
                "description": daily_data["weather"][0]["description"],
                "icon": daily_data["weather"][0]["icon"],
            }
        )

    return weather_data, forecast_data
