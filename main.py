import os
import random
import discord
from dotenv import load_dotenv
import asyncio
import datetime

# Import custom modules
import messages
import content
import dice
import trivia
import points
import weather
import news
import settings

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
ADMIN = os.getenv('DISCORD_ADMIN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

points.create_table()

@client.event
async def on_ready():
    # List connected servers
    guilds = client.guilds

    # Get guild names
    guild_names = [guild.name for guild in guilds]

    # Print out information for debugging
    print(f'{client.user} is connected to the following servers:\n {guild_names}')

    # Control weather and news updates
    while True:
        # if 0 6 12 18 EST
        if datetime.datetime.now().hour % 6 == 0:
            # For each guild
            for guild in client.guilds:
                # Get the news channel
                news_channel = settings.get_news_channel(guild)

                if news_channel != None:
                    # Get the weather data
                    weather_data = weather.main(guild, WEATHER_API_KEY)
                    # Get the news data
                    news_data = news.main(guild, NEWS_API_KEY)
                    # send to news channel
                    await news_channel.send(weather_data)
                    await news_channel.send(news_data)
                
        # Sleep for 1 minute
        await asyncio.sleep(60)

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
            await message.channel.send(messages.get_help())
            return

        if request == "utility":
            await message.channel.send(messages.get_utility())
            return

        if request == "content":
            await message.channel.send(messages.get_content())
            return

        if request == "game":
            await message.channel.send(messages.get_game())
            return

        if request == "gamble":
            await message.channel.send(messages.get_gamble())
            return

        if request == "info":
            await message.channel.send(messages.get_info())
            return

        # Trivia
        if request == "trivia":            
            answers, correct_answer, reply = trivia.get_random_question()

            # Send the question and ping the user
            await message.channel.send(f"{message.author.mention}\n{reply}")
            
            # Check if the answer is correct
            def check_answer(m):
                return (
                    m.author == message.author
                    and m.channel == message.channel
                    and m.content.strip() in ["1", "2", "3", "4"]
                )

            try:
                user_response = await client.wait_for("message", check=check_answer, timeout=10.0)
                user_answer = int(user_response.content.strip())
                selected_answer = answers[user_answer - 1]

                if selected_answer.endswith(correct_answer):
                    await message.channel.send("Correct answer!")
                    return
                else:
                    await message.channel.send(f"Wrong answer! The correct answer is: {correct_answer}")
                    return
            except asyncio.TimeoutError:
                await message.channel.send(f"Time's up! The correct answer is: {correct_answer}")
                return
        
        # Start gambling
        if request == "start":
            STARTING_POINTS = 1000
            new_account = points.add_user(message.author.id, STARTING_POINTS)
            # Check if the account was created
            if not new_account:
                await message.channel.send(f"{message.author.mention} You already have an account!")
                return
            else:
                await message.channel.send(f"{message.author.mention} Your account has been created!")
                return
        
        # Check points
        if request == "points":
            user_points = points.get_points(message.author.id)
            await message.channel.send(f"{message.author.mention} You have {user_points} points.")
            return

        # Income
        if request == "income":
            # Get current unix timestamp
            current_time = current_timestamp = int(datetime.datetime.now().timestamp())
            
            # Compare to last income timestamp
            last_income = points.get_last_income(message.author.id)
            
            # If it's been 30 minutes since last income
            if current_time - last_income >= 1800:
                # Add 100 points
                points.add_points(message.author.id, 100)
                # Update last income timestamp
                points.set_last_income(message.author.id, current_time)
                await message.channel.send(f"{message.author.mention} You've received 100 points!")
                return
            else:
                # get time left until 30 minutes is up
                time_left = 1800 - (current_time - last_income)
                # convert to minutes and seconds
                minutes = time_left // 60
                seconds = time_left % 60
                await message.channel.send(f"{message.author.mention} You can't collect income yet! Try again in {minutes} minutes and {seconds} seconds.")
                return

        # Roulette
        if request.startswith("roulette"):
            # Get wager
            wager = request.split(" ")[1]
            # Check that it's a positive integer
            if not wager.isdigit():
                await message.channel.send(f"{message.author.mention} Invalid wager.")
                return
            # Check that the user has enough points
            user_points = points.get_points(message.author.id)
            if int(wager) > user_points:
                await message.channel.send(f"{message.author.mention} You don't have enough points.")
                return
            # Play the game
            options = ["red", "black", "green"]
            # Check user's choice
            user_choice = request.split(" ")[2]
            if user_choice not in options:
                await message.channel.send(f"{message.author.mention} Invalid choice.")
                return
            # Spin the wheel
            wheel = random.choices(options, weights=[18, 18, 2], k=1)[0]
            # Check if the user won
            if user_choice == wheel:
                if user_choice == "green":
                    points.add_points(message.author.id, int(wager) * 14)
                else:
                    points.add_points(message.author.id, int(wager))
                await message.channel.send(f"{message.author.mention} You win! The wheel landed on {wheel}!")
                return
            # Check if the bot won
            else:
                points.add_points(message.author.id, -int(wager))
                await message.channel.send(f"{message.author.mention} You lose! The wheel landed on {wheel}!")
                return
        
        # Slots
        if request.startswith("slots"):
            # Get wager
            wager = request.split(" ")[1]
            # Check that it's a positive integer
            if not wager.isdigit():
                await message.channel.send(f"{message.author.mention} Invalid wager.")
                return
            # Check that the user has enough points
            user_points = points.get_points(message.author.id)
            if int(wager) > user_points:
                await message.channel.send(f"{message.author.mention} You don't have enough points.")
                return
            # Play the game
            options = ["1", "2", "3", "4", "5"]
            # Spin the wheel
            wheel = random.choices(options, weights=[1, 1, 1, 1, 1], k=3)
            # Check if the user won
            if wheel[0] == wheel[1] == wheel[2]:
                points.add_points(message.author.id, int(wager) * 20)
                await message.channel.send(f"{message.author.mention} You win! The wheel landed on | {wheel[0]} {wheel[1]} {wheel[2]} |")
                return
            # Check if the bot won
            else:
                points.add_points(message.author.id, -int(wager))
                await message.channel.send(f"{message.author.mention} You lose! The wheel landed on | {wheel[0]} {wheel[1]} {wheel[2]} |")
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
