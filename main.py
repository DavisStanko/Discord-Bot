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
    # Get the request
    request = message.content.lower()

    # If message is from the bot, ignore
    if message.author == client.user:
        return

    # If message is a command
    elif request.startswith('!'):
        # Remove the '!' from the request
        request = request[1:]

        if request == "help":
            reply = "I can help you with the following commands:\n" \
                    "`!help` - Displays this help message.\n" \
                    "`!content` - Lists content commands.\n" \
                    "`!game` - Lists game commands.\n" \
                    "`!utility` - Lists utility commands."
            await message.channel.send(reply)
            return

        if request == "utility":
            reply = f"I react to the following utility commands:\n" \
                    "`!info` - Links to my GitHub page.\n" \
                    "`!weather [location] [info|now|hour|day (0-47)|day (0-7)]` - Displays the weather info in the specified location and time.\n" \
                    "`!NdM` - Rolls N M-sided dice where N and M are positive integers.\n"
            await message.channel.send(reply)
            return

        if request == "content":
            reply = f"I react to the following content commands by sending a random media file from the specified directory:\n{content.get_commands()}"
            await message.channel.send(reply)
            return

        if request == "game":
            reply = f"I react to the following game commands:\n" \
                    "`!trivia` - Starts a game of trivia.\n" \
                    "`!heads` or `!tails` - Flips a coin and tells you the result.\n" \
                    "`!rock`, `!paper`, or `!scissors` - Plays a game of rock paper scissors.\n"
            await message.channel.send(reply)
            return

        if request == "info":
            reply = f"https://github.com/DavisStanko/Discord-Bot"
            await message.channel.send(reply)
            return

        # Trivia
        if request == "trivia":            
            answers, correct_answer, reply = trivia.get_random_question()

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
        
        # Coinflip
        if request == "heads" or request == "tails":
            # Get heads or tails
            coin = random.randint(0, 1)
            if coin == 0:
                coin = "heads"
            else:
                coin = "tails"
            # Check if the user guessed correctly
            if request == coin:
                await message.channel.send(f"{message.author.mention} You guessed correctly! It's {coin}!")
            else:
                await message.channel.send(f"{message.author.mention} You guessed incorrectly! It's {coin}!")
        
        # Rock Paper Scissors
        if request == "rock" or request == "paper" or request == "scissors":
            # Get the bot's choice
            bot = random.randint(0, 2)
            if bot == 0:
                bot = "rock"
            elif bot == 1:
                bot = "paper"
            else:
                bot = "scissors"
            # Check if the user won
            if request == "rock" and bot == "scissors":
                await message.channel.send(f"{message.author.mention} You win! I chose {bot}!")
            elif request == "paper" and bot == "rock":
                await message.channel.send(f"{message.author.mention} You win! I chose {bot}!")
            elif request == "scissors" and bot == "paper":
                await message.channel.send(f"{message.author.mention} You win! I chose {bot}!")
            # Check if the bot won
            elif request == "rock" and bot == "paper":
                await message.channel.send(f"{message.author.mention} I win! I chose {bot}!")
            elif request == "paper" and bot == "scissors":
                await message.channel.send(f"{message.author.mention} I win! I chose {bot}!")
            elif request == "scissors" and bot == "rock":
                await message.channel.send(f"{message.author.mention} I win! I chose {bot}!")
            # Check if it's a tie
            else:
                await message.channel.send(f"{message.author.mention} It's a tie! I chose {bot}!")
        
        # Weather command
        if request.startswith("weather"):
            # Split the request into words
            words = request.split()
    
            # Check if the request is valid and parse it
            try:
                city, info, time = weather.parse_weather(words)
            except Exception as e:
                await message.channel.send(e)
                return
            
            # Get the coordinates of the city
            lat, lon = weather.get_coordinates(city, WEATHER_API_KEY)
            # If the city is not found
            if lat is None or lon is None:
                await message.channel.send("City not found.")
                return
            
            # Get the weather data
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
        if request in content.get_commands():
            reply = content.get_file(request)
                        
            await message.channel.send(f"Here is your {request}!", file=discord.File(reply))
            return

        # Check if the request is a valid dice roll
        if dice.is_valid_dice_format(request):
            # Roll the dice
            N, M, roll_history, roll = dice.roll_dice(request)
            # Format the reply
            reply = f"You rolled {N}d{M} and got {roll} ({roll_history})"
            await message.channel.send(reply)
            return

client.run(TOKEN)
