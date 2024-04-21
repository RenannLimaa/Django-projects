from django.shortcuts import render
import requests


def index(request):
    API_KEY = open("/home/renan/programming/Django/weather_project/API_KEY", "r").read().strip()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}"

    if request.method == "POST":
        city = request.POST.get("city")

        weather_data = fetch_weather(city, API_KEY, current_weather_url)

        context = {
            "weather_data": weather_data
        }

        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")


def fetch_weather(city, api_key, current_weather_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()

    print(response)

    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'], 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    return weather_data
