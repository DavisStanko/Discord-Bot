import os
import random
import discord
from dotenv import load_dotenv
import asyncio

# Import custom modules
import content
import dice
import trivia
import weather

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
ADMIN = os.getenv('DISCORD_ADMIN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


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
                    "`!weather [location] [info|now|hour (0-47)|day (0-7)]` - Displays the weather info in the specified location and time.\n" \
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
            question_data = trivia.get_random_question()
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
            
            lat, lon = weather.get_coordinates(city, WEATHER_API_KEY)
            # If the city is not found
            if lat is None or lon is None:
                await message.channel.send("City not found.")
                return
            weather_data = weather.get_weather(lat, lon, WEATHER_API_KEY)
            # run function based on info
            if info == "info":
                reply = weather.info_weather(weather_data)
                reply = f"{city}'s info is:\n{reply}"
            elif info == "current":
                reply = weather.current_weather(weather_data)
                reply = f"The current weather in {city} is:\n{reply}"
            elif info == "hour":
                reply = weather.hour_weather(weather_data, time)
                reply = f"In {time} hours the weather in {city} will be:\n{reply}"
            elif info == "day":
                reply = weather.day_weather(weather_data, time)
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
        if request in content.content_commands:
            # Get the path to the folder
            folder_path = os.path.join(content.content_path, request)
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
        if dice.is_valid_dice_format(request):
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
