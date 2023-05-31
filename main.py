import os
import random
import discord
from dotenv import load_dotenv
import re
import requests
import json
import html
import asyncio
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
ADMIN = os.getenv('DISCORD_ADMIN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Get a list of all the folders in a directory
def get_child_folders(path):
    return [entry for entry in os.listdir(path) if os.path.isdir(os.path.join(path, entry))]

# Get the media paths
main_dir = os.path.dirname(os.path.realpath(__file__))
content_path = os.path.join(main_dir, "internet")

# Get the command lists
content_commands = sorted(["!" + command for command in get_child_folders(content_path)])

# Format the command lists
content_commands = "\n".join([f"`{command}`" for command in content_commands])

# Check if a string is in NdM format
def is_valid_dice_format(string):
    pattern = r"\d+d\d+"
    match = re.fullmatch(pattern, string)
    return match is not None

# Get a random trivia question
def get_random_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    data = json.loads(response.text)

    question = data['results'][0]
    question_text = html.unescape(question['question'])
    correct_answer = html.unescape(question['correct_answer'])
    incorrect_answers = [html.unescape(answer) for answer in question['incorrect_answers']]
    answers = incorrect_answers + [correct_answer]
    random.shuffle(answers)

    question_data = {
        'question': question_text,
        'answers': answers,
        'correct_answer': correct_answer
    }

    return question_data

# Function to fetch weather data from the API
def get_coordinates(city):
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

def get_weather(lat, lon):
    # Get weather data    
    weather = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(weather)
    data = json.loads(response.text)
    return data

# Format weather data into a string
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
    
    reply += f"\nSunrise: {sunrise}\nSunset: {sunset}\nMoonrise: {moonrise}\nMoonset: {moonset}\nMoon Phase: {moon_phase}\nSummary: {summary}\nTemperature: {temp}°C\nFeels Like: {feels_like}°C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nDew Point: {dew_point}°C\nWind Speed: {wind_speed} m/s\nWind Direction: {wind_deg}°\nWind Gust: {wind_gust} m/s\nWeather: {weather}\nClouds: {clouds}%\nProbability of Precipitation: {pop}%\nUV Index: {uvi}\n\n"
    
    return reply


@client.event
async def on_ready():
    # Connects to servers from .env
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    # Print out information for debugging
    print(f'{client.user} is connected to the following servers:\n{SERVER}')


@client.event
async def on_message(message):
    request = message.content.lower()

    # If message is from the bot, ignore
    if message.author == client.user:
        return

    # If message is a command
    elif request.startswith('!'):
        # Remove the '!' from the request
        request = request[1:]
        # .lower the request
        request = request.lower()

        if request == "help":
            reply = "I can help you with the following commands:\n" \
                    "`!help` - Displays this help message.\n" \
                    "`!content` - Lists content commands.\n" \
                    "`!games` - Lists game commands.\n" \
                    "`!utility` - Lists utility commands."
            await message.channel.send(reply)
            return

        if request == "utility":
            reply = f"I react to the following utility commands:\n" \
                    "`!info` - Links to my GitHub page.\n" \
                    "`!weather [location] [info|now|hour X|day X]` - Displays the weather info in the specified location and time where X is an integer.\n" \
                    "`!NdM` - Rolls N M-sided dice where N and M are positive integers.\n"
            await message.channel.send(reply)
            return

        if request == "content":
            reply = f"I react to the following content commands by sending a random media file from the specified directory:\n{content_commands}"
            await message.channel.send(reply)
            return

        if request == "games":
            reply = f"I react to the following game commands:\n" \
                    "`!trivia` - Starts a game of trivia."
            await message.channel.send(reply)
            return

        if request == "info":
            reply = f"https://github.com/DavisStanko/Discord-Bot"
            await message.channel.send(reply)
            return

        # Trivia
        if request == "trivia":            
            question_data = get_random_question()
            question = question_data['question']
            answers = question_data['answers']
            correct_answer = question_data['correct_answer']

            # Prompt to answer via number
            prompt = "Please answer by sending the number of the correct answer within 10 seconds."
            # Replace &quot; with "
            question = question.replace("&quot;", "\"")
            # Format the question
            question = f"**{question}**\n"
            # Format the answers
            answers = [f"{i+1}. {answer}" for i, answer in enumerate(answers)]
            # Combine the prompt, question, and answers
            reply = question + "\n".join(answers) + "\n" + prompt

            # Send the question and ping the user
            await message.channel.send(f"{message.author.mention}\n{reply}")
            
            # Check if the answer is correct
            def check_answer(m):
                return m.author == message.author and m.channel == message.channel and m.content.strip() in ["1", "2", "3", "4"]

            try:
                user_response = await client.wait_for('message', check=check_answer, timeout=10.0)
                user_answer = user_response.content.strip()
                if user_answer.isdigit():
                    user_answer = int(user_answer)
                    if 1 <= user_answer <= len(answers):
                        selected_answer = answers[user_answer - 1]
                        if selected_answer.endswith(correct_answer):
                            await message.channel.send("Correct answer!")
                        else:
                            await message.channel.send("Wrong answer! The correct answer is: " + correct_answer)
                        return
                await message.channel.send("Invalid answer. The correct answer is: " + correct_answer)
            except asyncio.TimeoutError:
                await message.channel.send("Time's up! The correct answer is: " + correct_answer)
            return
        
        # Weather command
        if request.startswith("weather"):
            words = request.split()

            try:
                city = words[1] # Extract the location from the message
            # If no location is specified
            except IndexError:
                await message.channel.send("Please specify a location.")
                return
            
            try:
                info = words[2]  # Extract the info from the message
                # check if info is valid
                if info not in ["info", "current", "minutely", "hour", "day"]:
                    await message.channel.send("Please specify a valid info type (info, current, hourly, daily).")
                    return
            except IndexError:
                info = "current"
            
            # if hour or day is specified check if 0-47 or 0-7
            if info in ["hour", "day"]:
                try:
                    time = int(words[3])
                    if info == "hour" and (time < 0 or time > 47):
                        await message.channel.send("Please specify a valid hour (0-47).")
                        return
                    elif info == "day" and (time < 0 or time > 7):
                        await message.channel.send("Please specify a valid day (0-7).")
                        return
                except IndexError:
                    await message.channel.send("Please specify a valid hour (0-47) or day (0-7).")
                    return
                except ValueError:
                    await message.channel.send("Please specify a valid hour (0-47) or day (0-7).")
                    return
            
            lat, lon = get_coordinates(city)
            # If the city is not found
            if lat is None or lon is None:
                await message.channel.send("City not found.")
                return
            weather = get_weather(lat, lon)
            # run function based on info
            if info == "info":
                reply = info_weather(weather)
                reply = f"{city}'s info is:\n{reply}"
            elif info == "current":
                reply = current_weather(weather)
                reply = f"The current weather in {city} is:\n{reply}"
            elif info == "hour":
                reply = hour_weather(weather, time)
                reply = f"In {time} hours the weather in {city} will be:\n{reply}"
            elif info == "day":
                reply = day_weather(weather, time)
                reply = f"In {time} days the weather in {city} will be:\n{reply}"
            # check if over 2000 characters
            if len(reply) > 2000:
                # check how many times 2000 goes into the length
                num = len(reply) // 2000
                # split the reply into num parts
                replies = [reply[i:i+2000] for i in range(0, len(reply), 2000)]
                # send each part
                for i in range(num):
                    await message.channel.send(replies[i])
                return
            await message.channel.send(reply)
            return

        # Content
        if request in content_commands:
            # Get the path to the folder
            folder_path = os.path.join(content_path, request)
            # Get a list of all the files in the folder
            files = os.listdir(folder_path)
            # Get a random file from the list
            file = random.choice(files)
            # Get the path to the file
            file_path = os.path.join(folder_path, file)
            # Send the file
            await message.channel.send(f"Here is your {request}!", file=discord.File(file_path))
            return

        # Utility
        # If request is in NdM format
        if is_valid_dice_format(request):
            # Split the string into N and M
            N, M = request.split("d")
            # Convert N and M to integers
            N = int(N)
            M = int(M)
            # Roll the dice
            rolls = [random.randint(1, M) for i in range(N)]
            # Format the reply
            reply = f"You rolled {N}d{M} and got {sum(rolls)} ({rolls})"
            await message.channel.send(reply)
            return

client.run(TOKEN)
