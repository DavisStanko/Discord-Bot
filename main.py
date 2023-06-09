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

NOUNS = "nouns.txt"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

points.create_table()


@client.event
async def on_ready():
    # List connected servers
    guilds = client.guilds

    # Print guild names with IDs
    for guild in guilds:
        print(f"{guild.name} ({guild.id})")

    # Control weather and news updates
    while True:
        # Get current unix timestamp
        current_time = int(datetime.datetime.now().timestamp())

        # Get the unix timestamp of the next trigger point 12am 6am 12pm 6pm
        next_trigger = current_time + (3600 - (current_time % 3600))

        # Get the time to sleep
        time_to_sleep = next_trigger - current_time

        # Sleep until the next trigger point
        print(f"Sleeping for {time_to_sleep} seconds")
        await asyncio.sleep(time_to_sleep)

        # For each guild
        for guild in client.guilds:
            # Get the news channel
            news_channel = settings.get_news_channel(guild)

            if news_channel is not None:
                # Get the weather data
                weather_data = weather.main(guild, WEATHER_API_KEY)
                # Get the news data
                news_data = news.main(guild, NEWS_API_KEY)
                # send to news channel
                await news_channel.send(weather_data)
                await news_channel.send(news_data)

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

        if request == "schedule":
            await message.channel.send(messages.get_schedule())
            return

        if request == "info":
            await message.channel.send(messages.get_info())
            return

        # Trivia
        if request == "trivia":
            # Check if user has an account
            if not points.has_account(message.author.id):
                await message.channel.send(f"{message.author.mention} You need to create an account first! Use !start")
                return
            
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
                    # Add 10 points
                    points.add_points(message.author.id, 10)
                    await message.channel.send("Correct answer! You get 10 points!")
                    return
                else:
                    await message.channel.send(f"Wrong answer! The correct answer is: {correct_answer}")
                    return
            except asyncio.TimeoutError:
                await message.channel.send(f"Time's up! The correct answer is: {correct_answer}")
                return
        
        # Word Scramble
        if request == "wordscramble":
            # check if user has an account
            if not points.has_account(message.author.id):
                await message.channel.send(f"{message.author.mention} You need to create an account first! Use !start")
                return
            
            # Open nouns
            with open(NOUNS, "r") as f:
                nouns = f.readlines()
                random_line = random.randint(0, len(nouns) - 1)
                word = nouns[random_line].strip()

            # Get length of word
            word_length = len(word)

            # randomize the positions of the letters
            prompt = list(word)
            random.shuffle(prompt)
            prompt = "".join(prompt)

            # Send the word and ping the user
            await message.channel.send(f"{message.author.mention}\nUnscramble the word in 30 seconds: {prompt}")

            # Check if the answer is correct
            def check_answer(m):
                return (
                    m.author == message.author
                    and m.channel == message.channel
                )
            
            try:
                user_response = await client.wait_for("message", check=check_answer, timeout=30.0)
                user_answer = user_response.content.strip().lower()

                if user_answer == word:
                    # Add 10 points
                    points.add_points(message.author.id, 10 * word_length)
                    await message.channel.send(f"Correct answer! You get {10 * word_length} points!")
                    return
                else:
                    await message.channel.send(f"Wrong answer! The correct answer is: {word}")
                    return
            except asyncio.TimeoutError:
                await message.channel.send(f"Time's up! The correct answer is: {word}")
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
            # Check if user has an account
            if not points.has_account(message.author.id):
                await message.channel.send(f"{message.author.mention} You need to create an account first! Use !start")
                return

            user_points = points.get_points(message.author.id)
            await message.channel.send(f"{message.author.mention} You have {user_points} points.")
            return

        # Income
        if request == "income":
            # Check if user has an account
            if not points.has_account(message.author.id):
                await message.channel.send(f"{message.author.mention} You need to create an account first! Use !start")
                return

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
            # Check if user has an account
            if not points.has_account(message.author.id):
                await message.channel.send(f"{message.author.mention} You need to create an account first! Use !start")
                return

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
            # Check if user has an account
            if not points.has_account(message.author.id):
                await message.channel.send(f"{message.author.mention} You need to create an account first! Use !start")
                return
            
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
