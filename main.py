# modularize more
# move reutnrs down with the help of else blocks

import asyncio
import asyncpraw
from asyncprawcore.exceptions import Forbidden
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
ADMIN = os.getenv('DISCORD_ADMIN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')

STARTING_POINTS = 1000

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
        # Sleep until the next trigger point
        current_time = int(datetime.datetime.now().timestamp())
        next_trigger = current_time + (21600 - (current_time % 21600))
        time_to_sleep = next_trigger - current_time
        await asyncio.sleep(time_to_sleep)

        # For each guild
        for guild in client.guilds:
            news_channel = settings.get_news_channel(guild.id)

            if news_channel is not None:
                # Get the weather data
                weather_data = weather.main(guild.id, WEATHER_API_KEY)
                # Get the news data
                news_data = news.main(guild.id, NEWS_API_KEY)
                # Convert the news channel ID to an object
                news_channel_obj = client.get_channel(int(news_channel))
                # Send the weather and news data to the news channel
                await news_channel_obj.send(weather_data)
                await news_channel_obj.send(news_data)

@client.event
async def on_message(message):
    # If message is from the bot, ignore 
    if message.author == client.user:
        return

    # If message is a command
    if message.content.startswith('!'):        
        # Remove the '!' from the request and make it case insensitive
        request = message.content[1:].lower()

        # Map help commands
        message_commands = {
            "help": messages.get_help(),
            "admin": messages.get_admin(),
            "utility": messages.get_utility(),
            "content": messages.get_content(),
            "games": messages.get_game(),
            "schedule": messages.get_schedule(),
            "info": messages.get_info(),
        }

        # Send the help message if sufficient permissions are met
        if request == "admin" and message.author.id != ADMIN:
            await message.channel.send(f"{message.author.mention} You do not have permission to use this command.")
            return
        elif request in message_commands:
            await message.channel.send(message_commands[request])
            return
        
        # Reddit
        if request in media.get_commands():
            # Get the subreddits associated with the command
            subreddits = media.get_commands()[request]

            # Create a reddit instance
            reddit = asyncpraw.Reddit(
                client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent="Discord Bot"
            )

            try:
                # Get a random subreddit and post
                subreddit = await reddit.subreddit(random.choice(subreddits))
                post = await subreddit.random()

                # Send the post
                reply = f"{post.title}\n{post.url}"
                await message.channel.send(reply)

            # If the subreddit is private
            except Forbidden:
                await message.channel.send(f"{message.author.mention} Unable to access r/{subreddit}. Subreddit may be private.")


        # Trivia
        if request == "trivia":
            # Check if user has an account
            if not points.has_account(message.author.id):
                await message.channel.send(f"{message.author.mention} You need to create an account first! Use !start")
                return
            
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
            
            # Open nouns file and get a random word
            with open(NOUNS, "r") as f:
                word = random.choice(f).strip()

            # Get length of word
            word_length = len(word)

            # randomize the positions of the letters
            prompt = "".join(random.sample(word, len(word)))

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
                    return
                else:
                    await message.channel.send(f"Wrong answer! The correct answer is: {word}")
                    return
            except asyncio.TimeoutError:
                await message.channel.send(f"Time's up! The correct answer is: {word}")
                return

        # Start gambling
        if request == "start":
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

            # Get current and last income timestamp
            current_time = int(datetime.datetime.now().timestamp())
            last_income = points.get_last_income(message.author.id)
            
            # If it hasn't been 30 minutes since last income
            if current_time - last_income < 1800:
                # get time left until 30 minutes is up
                time_left = 1800 - (current_time - last_income)
                # convert to minutes and seconds
                minutes = time_left // 60
                seconds = time_left % 60
                await message.channel.send(f"{message.author.mention} You can't collect income yet! Try again in {minutes} minutes and {seconds} seconds.")
                return

            # Add 100 points
            points.add_points(message.author.id, 100)
            # Update last income timestamp
            points.set_last_income(message.author.id, current_time)
            await message.channel.send(f"{message.author.mention} You've received 100 points!")
            return

        # Roulette
        if request.startswith("roulette"):
            # Check if user has an account
            if not points.has_account(message.author.id):
                await message.channel.send(f"{message.author.mention} You need to create an account first! Use !start")
                return

            # Extract wager and user choice
            _, wager, user_choice = request.split()
            
            # Check that the wager is an integer
            if not wager.isdigit():
                await message.channel.send(f"{message.author.mention} Invalid wager.")
                return
            
            wager = int(wager)
            user_points = points.get_points(message.author.id)

            # Check that the user has enough points
            if wager > user_points:
                await message.channel.send(f"{message.author.mention} You don't have enough points!")
                return
            
            # Define roulette options
            options = ["red", "black", "green"]

            # Check if the user's choice is valid
            if user_choice not in options:
                await message.channel.send(f"{message.author.mention} Invalid choice.")
                return
            
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
        if request.startswith("slots"):
            # Check if user has an account
            if not points.has_account(message.author.id):
                await message.channel.send(f"{message.author.mention} You need to create an account first! Use !start")
                return
            
            # Extract wager
            _, wager = request.split()

            # Check that the wager is an integer
            if not wager.isdigit():
                await message.channel.send(f"{message.author.mention} Invalid wager.")
                return
            
            wager = int(wager)
            user_points = points.get_points(message.author.id)

            # Check that the user has enough points
            if wager > user_points:
                await message.channel.send(f"{message.author.mention} You don't have enough points!")
                return
            
            # Define slot symbols
            symbols = ["1", "2", "3", "4", "5"]

            # Spin the wheel
            wheel = random.choices(symbols, weights=[1, 1, 1, 1, 1], k=3)

            # Check if the user won
            if wheel[0] == wheel[1] == wheel[2]:
                points.add_points(message.author.id, int(wager) * 20)
                await message.channel.send(f"{message.author.mention} You win! The wheel landed on | {wheel[0]} {wheel[1]} {wheel[2]} |")
                return
            else:
                points.add_points(message.author.id, -int(wager))
                await message.channel.send(f"{message.author.mention} You lose! The wheel landed on | {wheel[0]} {wheel[1]} {wheel[2]} |")
                return
        
        # Leaderboard
        if request == "leaderboard":
            # Get top 10 users
            top_users, top_points = points.get_top_users(10)

            # Convert user IDs to discord users
            for i, user in enumerate(top_users):
                discord_user = await client.fetch_user(user)
                if discord_user:
                    top_users[i] = discord_user.name
                else:
                    top_users[i] = "Unknown User"

            # Combine users and points
            top_users = [f"{top_users[i]} - {top_points[i]} points" for i in range(len(top_users))]

            await message.channel.send(f"```{chr(10).join(top_users)}```")
            return

        # Admin commands
        admin_commands = ["setcity", "setcountry", "setnewschannel"]

        for command in admin_commands:
            if request.startswith(command):
                # Check if user is admin
                if not message.author.guild_permissions.administrator:
                    await message.channel.send(f"{message.author.mention} You don't have permission to do that.")
                    return

                # get argument
                argument = request.split(" ")[1]

                # set city
                if command == "setcity":
                    settings.set_city(message.guild.id, argument)
                    await message.channel.send(f"{message.author.mention} City set to {argument}")
                    return
                
                # set country
                if command == "setcountry":
                    settings.set_country(message.guild.id, argument)
                    await message.channel.send(f"{message.author.mention} Country set to {argument}")
                    return
                
                # set news channel
                if command == "setnewschannel":
                    settings.set_news_channel(message.guild.id, argument)
                    await message.channel.send(f"{message.author.mention} News channel set to {argument}")
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
