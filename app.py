from flask import Flask, render_template, request
import requests
from datetime import datetime
import pycountry

__version__ = "0.2.0"

app = Flask(__name__)

# Your OpenWeatherMap API Key
API_KEY = "4a0d54e3d5e62026af5d5e51844ef022"


def get_country_name(code):
    country = pycountry.countries.get(alpha_2=code)
    return country.name if country else code


def get_weather(city=None, lat=None, lon=None):
    params = {"appid": API_KEY, "units": "metric"}
    url = "https://api.openweathermap.org/data/2.5/weather"

    if city:
        params["q"] = city
    else:
        params["lat"] = lat
        params["lon"] = lon

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code != 200:
            return None

        # Extracting data
        main = data["main"]
        weather_info = data["weather"][0]

        # HTTPS Fix for the 'black dot' error + High Resolution Icons
        icon_code = weather_info["icon"]

        return {
            "city": data["name"],
            "country": get_country_name(data["sys"]["country"]),
            "temp": round(main["temp"]),
            "feels": round(main["feels_like"]),
            "min": round(main["temp_min"]),
            "max": round(main["temp_max"]),
            "humidity": main["humidity"],
            "description": weather_info["description"].title(),
            "wind": round(data["wind"]["speed"], 1),
            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime(
                "%I:%M %p"
            ),
            "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime(
                "%I:%M %p"
            ),
            "icon_url": f"https://openweathermap.org/img/wn/{icon_code}@4x.png",
            "coord": data.get("coord"),
        }
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_nearby_cities(lat, lon, cnt=5):
    url = "https://api.openweathermap.org/data/2.5/find"
    params = {"lat": lat, "lon": lon, "cnt": cnt, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return []

        nearby = []
        for city in response.json().get("list", []):
            nearby.append(
                {
                    "city": city["name"],
                    "temp": round(city["main"]["temp"]),
                    "description": city["weather"][0]["description"].title(),
                    "icon_url": f"https://openweathermap.org/img/wn/{city['weather'][0]['icon']}@2x.png",
                }
            )
        return nearby
    except:
        return []


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    nearby = []
    output = ""
    temp_class = "normal"  # Default background

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather = get_weather(city)
            if not weather:
                output = f"City '{city}' not found. Please try again."
            else:
                # TEMPERATURE LOGIC: Determine background color
                current_temp = weather["temp"]
                if current_temp >= 30:
                    temp_class = "hot"
                elif current_temp <= 10:
                    temp_class = "cold"
                else:
                    temp_class = "pleasant"

                # Nearby Cities Logic
                lat, lon = weather["coord"]["lat"], weather["coord"]["lon"]
                raw_list = get_nearby_cities(lat, lon)
                nearby = [c for c in raw_list if c["city"].lower() != city.lower()][:2]

    return render_template(
        "index.html",
        weather=weather,
        nearby=nearby,
        output=output,
        temp_class=temp_class,
    )


@app.route("/")
def index():
    return render_template("index.html", version=__version__)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
