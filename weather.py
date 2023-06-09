import requests
import json
from datetime import datetime
import csv

FILENAME = "settings.csv"

def get_city(guild):
    # read the city from the settings file for the guild
    with open('settings.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == str(guild.id):
                return row[1]

def main(guild, WEATHER_API_KEY):
    # read the city from the settings file for the guild
    city = get_city(guild)
    # get the coordinates of the city
    lat, lon = get_coordinates(city, WEATHER_API_KEY)
    # get the weather data
    data = get_weather(lat, lon, WEATHER_API_KEY)
    # get the current weather
    current = current_weather(data)
    weather_response = f"Here is the weather for {city}:\n{current}"
    return weather_response

# Function to fetch weather data from the API
def get_coordinates(city, WEATHER_API_KEY):
    # Get city coordinates
    geocoding = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&appid={WEATHER_API_KEY}"
    response = requests.get(geocoding)
    data = json.loads(response.text)
    # If no city found, return
    if len(data) == 0:
        return None, None
    # extract coordinates
    lat = data[0]['lat']
    lon = data[0]['lon']
    return lat, lon

def get_weather(lat, lon, WEATHER_API_KEY):
    # Get weather data    
    weather = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(weather)
    data = json.loads(response.text)
    return data

def info_weather(data):
    # get lat, lon, timezone, timezone_offset
    lat = data["lat"]
    lon = data["lon"]
    timezone = data["timezone"]
    timezone_offset = data["timezone_offset"]
    return f"Latitude: {lat}\nLongitude: {lon}\nTimezone: {timezone}\nTimezone Offset: {timezone_offset}"
    
def current_weather(data):
    # get all current datapoints
    current_data = data["current"]
    sunrise = current_data["sunrise"]
    sunset = current_data["sunset"]
    temp = current_data["temp"]
    feels_like = current_data["feels_like"]
    pressure = current_data["pressure"]
    humidity = current_data["humidity"]
    dew_point = current_data["dew_point"]
    uvi = current_data["uvi"]
    clouds = current_data["clouds"]
    visibility = current_data["visibility"]
    wind_speed = current_data["wind_speed"]
    wind_deg = current_data["wind_deg"]
    weather = current_data["weather"][0]["description"]
    
    # format sunrise and sunset
    sunrise = datetime.fromtimestamp(sunrise).strftime("%#I:%M %p")
    sunset = datetime.fromtimestamp(sunset).strftime("%#I:%M %p")

    return f"\nSunrise: {sunrise}\nSunset: {sunset}\nTemperature: {temp}°C\nFeels Like: {feels_like}°C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nDew Point: {dew_point}°C\nUV Index: {uvi}\nClouds: {clouds}%\nVisibility: {visibility} meters\nWind Speed: {wind_speed} m/s\nWind Direction: {wind_deg}°\nWeather: {weather}"
    
def hour_weather(data, hour):
    reply = ""
    
    hours_from_now = data["hourly"][hour]
    temp = hours_from_now["temp"]
    feels_like = hours_from_now["feels_like"]
    pressure = hours_from_now["pressure"]
    humidity = hours_from_now["humidity"]
    dew_point = hours_from_now["dew_point"]
    uvi = hours_from_now["uvi"]
    clouds = hours_from_now["clouds"]
    visibility = hours_from_now["visibility"]
    wind_speed = hours_from_now["wind_speed"]
    wind_deg = hours_from_now["wind_deg"]
    wind_gust = hours_from_now["wind_gust"]
    weather = hours_from_now["weather"][0]["description"]

    reply += f"\nTemperature: {temp}°C\nFeels Like: {feels_like}°C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nDew Point: {dew_point}°C\nUV Index: {uvi}\nClouds: {clouds}%\nVisibility: {visibility} meters\nWind Speed: {wind_speed} m/s\nWind Direction: {wind_deg}°\nWind Gust: {wind_gust} m/s\nWeather: {weather}\n\n"
    
    return reply
        
    
def day_weather(data, day):
    reply = ""
    
    days_from_now = data["daily"][day]
    sunrise = days_from_now["sunrise"]
    sunset = days_from_now["sunset"]
    moonrise = days_from_now["moonrise"]
    moonset = days_from_now["moonset"]
    moon_phase = days_from_now["moon_phase"]
    summary = days_from_now["summary"]
    temp = days_from_now["temp"]
    day_temp = temp["day"]
    min_temp = temp["min"]
    max_temp = temp["max"]
    night_temp = temp["night"]
    eve_temp = temp["eve"]
    morn_temp = temp["morn"]
    feels_like = days_from_now["feels_like"]
    day_feels_like = feels_like["day"]
    night_feels_like = feels_like["night"]
    eve_feels_like = feels_like["eve"]
    morn_feels_like = feels_like["morn"]
    pressure = days_from_now["pressure"]
    humidity = days_from_now["humidity"]
    dew_point = days_from_now["dew_point"]
    wind_speed = days_from_now["wind_speed"]
    wind_deg = days_from_now["wind_deg"]
    wind_gust = days_from_now["wind_gust"]
    weather = days_from_now["weather"][0]["description"]
    clouds = days_from_now["clouds"]
    pop = days_from_now["pop"]
    uvi = days_from_now["uvi"]
    
    # format sunrise, sunset, moonrise, moonset
    sunrise = datetime.fromtimestamp(sunrise).strftime("%#I:%M %p")
    sunset = datetime.fromtimestamp(sunset).strftime("%#I:%M %p")
    moonrise = datetime.fromtimestamp(moonrise).strftime("%#I:%M %p")
    moonset = datetime.fromtimestamp(moonset).strftime("%#I:%M %p")
    
    reply += f"\nSunrise: {sunrise}\nSunset: {sunset}\nMoonrise: {moonrise}\nMoonset: {moonset}\nMoon Phase: {moon_phase}\nSummary: {summary}\nDay Temperature: {day_temp}°C\n Min Temperature: {min_temp}°C\n Max Temperature: {max_temp}°C\n Night Temperature: {night_temp}°C\n Evening Temperature: {eve_temp}°C\n Morning Temperature: {morn_temp}°C\n Day Feels Like: {day_feels_like}°C\n Night Feels Like: {night_feels_like}°C\n Evening Feels Like: {eve_feels_like}°C\n Morning Feels Like: {morn_feels_like}°C\n Pressure: {pressure} hPa\n Humidity: {humidity}%\n Dew Point: {dew_point}°C\n Wind Speed: {wind_speed} m/s\n Wind Direction: {wind_deg}°\n Wind Gust: {wind_gust} m/s\n Weather: {weather}\n Clouds: {clouds}%\n Precipitation Probability: {pop}%\n UV Index: {uvi}\n\n"
    
    return reply