# Import Libraries
import requests
from datetime import datetime
import pycountry

# API_KEY and BASE_URL link
API_KEY = "4a0d54e3d5e62026af5d5e51844ef022"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Full country name Function()
def get_country_name(code):
    "Convert country code to full country name"
    country = pycountry.countries.get(alpha_2=code)
    return country.name if country else code 

# city weather Function()
def get_weather(city):#  API Request Parameters
    params = {        
        "q": city,
        "appid": API_KEY,
        "units": 'metric'
   
    }

    try: # Send Request to API
        response = requests.get(BASE_URL, params=params)
        data = response.json() # Convert Response to JSON

        if response.status_code == 200: # 200 mean success

            main = data["main"]
            weather = data["weather"][0]
            wind = data["wind"]
            sys = data["sys"]

            temperature = main["temp"]
            feels_like = main["feels_like"]
            temp_min = main["temp_min"]
            temp_max = main["temp_max"]
            pressure = main["pressure"]
            humidity = main["humidity"]

        # Weather Description
            description = weather["description"]
            wind_speed = wind["speed"]

        # Sunrise and sunset
            sunrise = datetime.fromtimestamp(sys["sunrise"])
            sunset = datetime.fromtimestamp(sys["sunset"])

        # Convert Country Code
            country_code = sys["country"]
            country = get_country_name(country_code)


            print("\n Weather Report")
            print("-------------------------")
            print(f"city: {city}, {country}")
            print(f"condition: {description}")
            print(f"Temperature: {temperature} °C")
            print(f"Fells like: {feels_like} °C")
            print(f"min Temp: {temp_min} °C")
            print(f"max Temp: {temp_max} °C")
            print(f"Humidity: {humidity}%")
            print(f"Pressure: {pressure} hpa")
            print(f"wind Speed: {wind_speed} m/s")
            print(f"Sunrise: {sunrise.strftime('%I:%M:%S %p')}")
            print(f"Sunset: {sunset.strftime('%I:%M:%S %p')}")
            print("----------------------------")

        else:
            print("Error:", data.get("message", "City not found"))
        
    # Error Handling
    except requests.exceptions.RequestException:
        print("Network error: Please check your internet connection.")
\
# Main Function()
def main():
    city_name = input("Enter city name: ").strip()
    get_weather(city_name)

# Program Start 
if __name__ == "__main__":
    main()





