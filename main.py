import os
import random
import discord
from dotenv import load_dotenv  # Loads the .env file
import smtplib
import ssl

from requests import request  # for email

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')  # Server ID
ADMIN = os.getenv('DISCORD_ADMIN')  # Admin ID
# spotify
SPOTIFY_PROFILE = os.getenv('SPOTIFY_PROFILE')
CHILL = os.getenv('CHILL')
HEAVY = os.getenv('HEAVY')
ROCK = os.getenv('ROCK')
LIGHT = os.getenv('LIGHT')
RAP = os.getenv('RAP')
POP = os.getenv('POP')
HYPERPOP = os.getenv('HYPERPOP')
NOISE = os.getenv('NOISE')
COUNTRY = os.getenv('COUNTRY')
SIGMA = os.getenv('SIGMA')
BOOMER = os.getenv('BOOMER')
# Email authentication
MAIL_USER = os.getenv('GMAIL_USERNAME')
MAIL_PASS = os.getenv('GMAIL_APP_PASSWORD')

# Number of reactions needed to trigger a command
votes = 2

# List of commands for !help
# Space in front of first command is intentional for consistent indentaion
commandlist = [" !help", "!info", "!song", "!meme", "!object", "!animal", "!feels", "!literallyme", "!motivation"]
commandlist = ", ".join(commandlist).replace(',', '\n').replace(' ', '')  # Join commands into one string and format it
helpmessage = (f"I react to the following commands:\n{commandlist}\nI can also roll dice of any size! Try typing !d20\nYou can add \"amount\" to the end of most commands to get the total number of possible outputs.\nDislike a file attachment? If a message from me gets the 👎 reaction {votes} times, the attachment will automatically be deleted from my server.")

gitrepo = "https://github.com/DavisStanko/Discord-Bot"

# List of playlists for !song
# Space in front of first playlists is intentional for consistent indentaion
playlists = [" chill", "heavy", "rock", "light", "rap", "pop", "hyperpop", "noise", "country", "sigma", "boomer"]
numberofplaylsits = len(playlists)
playlists = ", ".join(playlists).replace(',', '\n')  # Join playlists into one string and format it
songhelpmessage = (f"Add a playlist name to the end of the !song command to recieve that playlist's url.\nPlaylists include:\n{playlists}\n You can also find these playlists on my spotify profile: {SPOTIFY_PROFILE}")

client = discord.Client()


@client.event  # Connect to discord
async def on_ready():
    # connects to servers from .env
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    # Prints out infor for debugging
    print(f'{client.user} is connected to the following servers:\n{SERVER}')


@client.event  # Send message reply
async def on_message(message):
    request = message.content.lower().replace(' ', '')

    # If message is from bot, ignore
    if message.author == client.user:
        return

    # Send help message
    if request == "!help":
        await message.channel.send(content=helpmessage)
        return

    # Send info message
    if request == "!info":
        await message.channel.send(content=gitrepo)
        return

    # Send song help message
    if request == "!song":
        await message.channel.send(content=songhelpmessage)
        return

    # All other song commands
    if request.startswith("!song"):
        if request.endswith("chill"):
            await message.channel.send(content=CHILL)
            return
        elif request.endswith("heavy"):
            await message.channel.send(content=HEAVY)
            return
        elif request.endswith("rock"):
            await message.channel.send(content=ROCK)
            return
        elif request.endswith("light"):
            await message.channel.send(content=LIGHT)
            return
        elif request.endswith("rap"):
            await message.channel.send(content=RAP)
            return
        elif request.endswith("hyperpop"):
            await message.channel.send(content=HYPERPOP)
            return
        elif request.endswith("pop"):
            await message.channel.send(content=POP)
            return
        elif request.endswith("noise"):
            await message.channel.send(content=NOISE)
            return
        elif request.endswith("country"):
            await message.channel.send(content=COUNTRY)
            return
        elif request.endswith("sigma"):
            await message.channel.send(content=SIGMA)
        elif request.endswith("boomer"):
            await message.channel.send(content=BOOMER)
            return

    # Dice roll
    if request.startswith("!d"):
        sides = request.replace("!d", "")
        # Try to conver to int
        try:
            sides = int(sides)
        except TypeError:
            pass
        # Check if negative integer
        if sides < 1:
            await message.channel.send(content=f"Please enter a positive number.")
        roll = random.randint(1, sides)
        await message.channel.send(content=f"You rolled a {roll}")

    # Return ammount of files in directory
    if request.endswith("amount"):
        directory = request.replace("!", "").replace("amount", "")  # Get directory name
        answer = os.listdir(directory)  # Get list of files in directory
        if directory.endswith("s"):
            plural = ""
        else:
            plural = "s"
        await message.channel.send(content=f"There are {len(answer)} {directory}{plural}")  # Number of files
        return

    #  Return random file in directory
    if request.startswith("!"):
        try:
            directory = request.replace("!", "")  # Get directory name
            attachment = random.choice(os.listdir(directory))  # Get random file in directory
            path = f"{directory}/{attachment}"  # Get path to file
            final = discord.File(path)  # Create file object
            await message.channel.send(content=f"Here is your {directory}!", file=final)  # Send file
            return
        except FileNotFoundError:  # If directory doesn't exist
            pass


@client.event  # React to reaction
async def on_reaction_add(reaction, user):
    if str(reaction.emoji) == "👎":
        if reaction.count == votes:
            try:
                directory = reaction.message.content.replace("Here is your ", "").replace("!", "")  # Get directory name
                attachment = reaction.message.attachments[0].filename  # Get file name
                path = f"{directory}/{attachment}"  # Get path to file
                os.remove(path)  # Delete file

                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
                    server.login(MAIL_USER, MAIL_PASS)
                    server.sendmail(MAIL_USER, MAIL_USER, f"{path} was deleted")
                return
            except IndexError:  # If no file is attached
                pass

client.run(TOKEN)
