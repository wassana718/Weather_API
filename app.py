from flask import Flask, render_template, request
import requests
from datetime import datetime
import pycountry

# request.form.get("username")

# name = request.form["username"]

app = Flask(__name__)

# add your OpenWeatherMap API key here
#create from openweathermap.org

API_KEY = "4a0d54e3d5e62026af5d5e51844ef022"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_country_name(code):
    country = pycountry.countries.get(alpha_2=code)
    return country.name if country else code


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]
        sys = data["sys"]

        return {
            "city": city,
            "country": get_country_name(sys["country"]),
            "temp": main["temp"],
            "feels": main["feels_like"],
            "min": main["temp_min"],
            "max": main["temp_max"],
            "humidity": main["humidity"],
            "pressure": main["pressure"],
            "description": weather["description"],
            "wind": wind["speed"],
            "sunrise": datetime.fromtimestamp(sys["sunrise"]).strftime('%I:%M %p'),
            "sunset": datetime.fromtimestamp(sys["sunset"]).strftime('%I:%M %p')
        }

    return None


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    output = ""

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            weather = get_weather(city)
            if not weather:
                output = f"City not found. Please try again. {city}"

    return render_template("index.html", output=output, weather=weather)


if __name__ == "__main__":
    app.run(debug=True)
