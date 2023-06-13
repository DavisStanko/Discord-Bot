import asyncio
import datetime
import discord
from dotenv import load_dotenv
import os
import random

# Import custom modules
from commands import dice, media, messages, news, points, settings, trivia, weather

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')

STARTING_POINTS = 1000
LEADERBOARD_SIZE = 10

NOUNS = "nouns.txt"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

points.create_table()

# Help commands
message_commands = {
    "help": messages.get_help,
    "media": messages.get_media,
    "games": messages.get_game,
    "schedule": messages.get_schedule,
    "info": messages.get_info,
}

# Admin commands
admin_commands = {
    "admin": messages.get_admin,
    "setlocation": settings.set_location,
    "setnewschannel": settings.set_news_channel
}

# Account commands
account_commands = ["points", "income", "trivia", "wordscramble", "roulette", "slots"]

@client.event
async def on_ready():
    # List connected servers
    guilds = client.guilds

    # Print guild names with IDs
    print(f"{client.user} is connected to:")
    for guild in guilds:
        print(f"{guild.name} ({guild.id})")

    # Control weather and news updates
    while True:
        # Sleep until the next trigger point
        current_time = int(datetime.datetime.now().timestamp())
        next_trigger = current_time + (21600 - (current_time % 21600))
        time_to_sleep = next_trigger - current_time
        await asyncio.sleep(time_to_sleep)

        # For each guild
        for guild in client.guilds:
            news_channel = settings.get_news_channel(guild.id)

            if news_channel is not None:
                # Get the weather and news data
                weather_data = weather.main(guild.id, WEATHER_API_KEY)
                news_data = news.main(guild.id, NEWS_API_KEY)
                # Convert the news channel ID to an object
                news_channel_obj = client.get_channel(int(news_channel))
                # Send the weather and news data to the news channel
                await news_channel_obj.send(weather_data)
                await news_channel_obj.send(news_data)

@client.event
async def on_message(message):
    # Check if the bot has permissions to send messages, that the message is not from the bot, and that the message is a command
    if not message.channel.permissions_for(message.guild.me).send_messages or message.author == client.user or not message.content.startswith('!'):
        return

    # Format the request
    request = message.content[1:].lower()
    command = request.split(" ")[0]    

    # Help commands
    if command in message_commands:
        command = message_commands[request]
        await message.channel.send(command())
    
    # Admin commands
    elif command in admin_commands:
        # Check if the user is an admin
        if not message.author.guild_permissions.administrator:
            await message.channel.send(f"{message.author.mention} You do not have permission to use that command!")
            return

        if command == "admin":
            await message.channel.send(admin_commands[command]())
        elif command == "setnewschannel":
            admin_commands[command](message.guild.id, message.channel.id)
            await message.channel.send(f"{message.author.mention} News channel set to {message.channel.mention}!")
        elif command == "setlocation":
            # Split the request into the command and the location
            request = request.split(" ")

            # Check if the request is valid
            if len(request) != 3:
                await message.channel.send(f"{message.author.mention} Invalid command! Please use the format `!setlocation [city] [country]`")
                return

            # Get the city and country
            city = request[1]
            country = request[2]

            # Set the location
            admin_commands[command](message.guild.id, city, country)
            await message.channel.send(f"{message.author.mention} Location set to {city}, {country}!")

    # Media commands
    elif command in media.get_commands():
        post, subreddit = await media.get_post(request, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)

        # Check for errors
        response = (f"{message.author.mention} Unable to access r/{subreddit}. Subreddit may be private.") if post is None else post
        await message.channel.send(response)

    # Create an account
    elif command == "start":
        new_account = points.add_user(message.author.id, STARTING_POINTS)

        # Check if the account was created
        response = f"{message.author.mention} You already have an account!" if not new_account else f"{message.author.mention} Account created! You have {STARTING_POINTS} points."
        await message.channel.send(response)

    # Leaderboard
    elif command == "leaderboard":
        leaderboard = await points.get_top_users(client, LEADERBOARD_SIZE)
        await message.channel.send(leaderboard)
        
    # Account commands
    elif command in account_commands:
        # Check if the user has an account
        user_has_account = points.has_account(message.author.id)

        if not user_has_account:
            await message.channel.send(f"{message.author.mention} You need to create an account first! Use `!start`")
        else:
            # Points
            if command == "points":
                user_points = points.get_points(message.author.id)
                await message.channel.send(f"{message.author.mention} You have {user_points} points.")

            # Income
            elif command == "income":
                current_time = int(datetime.datetime.now().timestamp())
                last_income = points.get_last_income(message.author.id)
                
                # If it hasn't been 30 minutes since last income
                if current_time - last_income < 1800:
                    # get time left until next income
                    time_left = 1800 - (current_time - last_income)
                    # convert to minutes and seconds
                    minutes, seconds = divmod(time_left, 60)
                    await message.channel.send(f"{message.author.mention} You can't collect income yet! Try again in {minutes} minutes and {seconds} seconds.")
                else:
                    # Add 100 points and set the last income time
                    points.add_points(message.author.id, 100)
                    points.set_last_income(message.author.id, current_time)
                    await message.channel.send(f"{message.author.mention} You've received 100 points!")

            # Trivia
            elif command == "trivia":
                # Get trivia question and answers
                answers, correct_answer, reply = trivia.get_random_question()

                # Send the question and ping the user
                await message.channel.send(f"{message.author.mention}\n{reply}")
                
                # Check if a message is a valid answer and sent from the asker
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
                    else:
                        await message.channel.send(f"Wrong answer! The correct answer is: {correct_answer}")
                except asyncio.TimeoutError:
                    await message.channel.send(f"Time's up! The correct answer is: {correct_answer}")
            
            # Word Scramble
            elif command == "wordscramble":
                # Open get all nouns
                with open(NOUNS, "r") as f:
                    words = f.read().splitlines()
                
                # Get a random word
                word = random.choice(words).strip().lower()

                # Get length of word
                word_length = len(word)

                # randomize the positions of the letters
                prompt = "".join(random.sample(word, word_length))

                # Send the word and ping the user
                await message.channel.send(f"{message.author.mention}\nUnscramble the word in 30 seconds: {prompt}")

                # Check if the message is a valid answer and sent from the asker
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
                    else:
                        await message.channel.send(f"Wrong answer! The correct answer is: {word}")
                except asyncio.TimeoutError:
                    await message.channel.send(f"Time's up! The correct answer is: {word}")
            
            # Roulette
            elif command == "roulette":
                # Extract wager and user choice
                _, wager, user_choice = request.split()
                
                # Check that the wager is an integer
                if not wager.isdigit():
                    await message.channel.send(f"{message.author.mention} Invalid wager.")
                else:
                    wager = int(wager)
                    user_points = points.get_points(message.author.id)

                    # Check that the user has enough points
                    if wager > user_points:
                        await message.channel.send(f"{message.author.mention} You don't have enough points!")
                    else:
                        # Define roulette options
                        options = ["red", "black", "green"]

                        # Check if the user's choice is valid
                        if user_choice not in options:
                            await message.channel.send(f"{message.author.mention} Invalid choice.")
                        else:
                            # Spin the wheel
                            wheel = random.choices(options, weights=[18, 18, 2], k=1)[0]

                            # Check if the user won
                            if user_choice == wheel:
                                # Calculate winnings and add to user's points
                                winnings = wager * 14 if wheel == "green" else wager
                                points.add_points(message.author.id, winnings)
                                await message.channel.send(f"{message.author.mention} You won {winnings} points!")
                            else:
                                points.add_points(message.author.id, -wager)
                                await message.channel.send(f"{message.author.mention} You lost {wager} points!")

            # Slots
            elif command == "slots":
                # Extract wager
                _, wager = request.split()

                # Check that the wager is an integer
                if not wager.isdigit():
                    await message.channel.send(f"{message.author.mention} Invalid wager.")
                else:                
                    wager = int(wager)
                    user_points = points.get_points(message.author.id)

                    # Check that the user has enough points
                    if wager > user_points:
                        await message.channel.send(f"{message.author.mention} You don't have enough points!")
                    else:
                        # Define slot symbols
                        symbols = ["1", "2", "3", "4", "5"]

                        # Spin the wheel
                        wheel = random.choices(symbols, weights=[1, 1, 1, 1, 1], k=3)

                        # Check if the user won
                        if wheel[0] == wheel[1] == wheel[2]:
                            points.add_points(message.author.id, int(wager) * 20)
                            await message.channel.send(f"{message.author.mention} You win! The wheel landed on | {wheel[0]} {wheel[1]} {wheel[2]} |")
                        else:
                            points.add_points(message.author.id, -int(wager))
                            await message.channel.send(f"{message.author.mention} You lose! The wheel landed on | {wheel[0]} {wheel[1]} {wheel[2]} |")
    
    # Dice
    elif dice.is_valid_dice_format(command):
        # Roll the dice
        N, M, roll_history, roll = dice.roll_dice(command)
        # Format the reply
        reply = f"You rolled {N}d{M} and got {roll} ({roll_history})"
        await message.channel.send(reply)


client.run(TOKEN)