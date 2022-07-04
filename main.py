import os, os.path
import random 
import discord
from dotenv import load_dotenv # Loads the .env file
import smtplib, ssl

from requests import request # for email

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') 
SERVER = os.getenv('DISCORD_SERVER') # Server ID
ADMIN = os.getenv('DISCORD_ADMIN') # Admin ID
# spotify
SPOTIFY_PROFILE = os.getenv('SPOTIFY_PROFILE')
CHILL = os.getenv('CHILL')
COUNTRY = os.getenv('COUNTRY')
HEAVY = os.getenv('HEAVY')
LIGHT = os.getenv('LIGHT')
POP = os.getenv('POP')
SIGMA = os.getenv('SIGMA')
# for a friend
PROFILE_NAME_1 = os.getenv('DISCORD_PROFILE_NAME_1') # Name of my freinds profile
HIDDEN_MESSAGE = os.getenv('HIDDEN_MESSAGE') # Easter egg
# Email authentication
MAIL_USER = os.getenv('GMAIL_USERNAME')
MAIL_PASS = os.getenv('GMAIL_APP_PASSWORD') 

# Number of reactions needed to trigger a command
votes = 2

# List of commands for !help
# Space in front of first command is intentional for consistent indentaion
commandlist = [" !help", "!info", "!song", "!meme", "!object", "!animal", "!feels", "!literallyme"]
commandlist = ", ".join(commandlist).replace(',', '\n').replace(' ','') # Join commands into one string and format it
helpmessage = (f"I react to the following commands:\n{commandlist}\nYou can add \"amount\" to the end of most commands to get the total number of possible outputs.\nDislike a file attachment? If a message from me gets the 👎 reaction {votes} times, the attachment will automatically be deleted from my server.")

gitrepo = "https://github.com/DavisStanko/Discord-Bot"

# List of playlists for !song
# Space in front of first playlists is intentional for consistent indentaion
playlists = [" chill", "country", "heavy", "light", "pop", "sigma"]
numberofplaylsits = len(playlists)
playlists = ", ".join(playlists).replace(',', '\n') # Join playlists into one string and format it
songhelpmessage = (f"Add a playlist to the end of the !song command to get a random song from that playlist.\nPlaylists include:\n{playlists}\nAdd \"amount\" after a playlist to get the total number of possible songs. You can find these playlists on my spotify profile: {SPOTIFY_PROFILE}")

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
    
    # # Command no longer relevent but may be in the future.
    # # No return, so it will continue to the next command even if this is activated.
    # if message.author.name == PROFILE_NAME_1:
    #     chance = random.randint(1,100)
    #     if chance == 1:
    #         await message.channel.send(content=HIDDEN_MESSAGE)
    #     else:
    #         await message.channel.send(content="Go Leafs Go!")

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
        if request.endswith("country"):
            await message.channel.send(content=COUNTRY)
            return
        if request.endswith("heavy"):
            await message.channel.send(content=HEAVY)
            return
        if request.endswith("light"):
            await message.channel.send(content=LIGHT)
            return
        if request.endswith("pop"):
            await message.channel.send(content=POP)
            return
        if request.endswith("sigma"):
            await message.channel.send(content=SIGMA)
            return

# Deprecated: I'm too lazy to consistently update the text files nessesary to make this work
    # if request.startswith("!song"):
    #     if request.endswith("amount"):
    #         if request == "!songamount":  # If no playlist is specified
    #             await message.channel.send(f"There are {numberofplaylsits} playlists.")  # Number of playlists.
    #             return
    #         else:
    #             request = request.replace("!song", "").replace("amount", "")  # Get playlist name
    #             answer = len(open(f'song/{request}.txt').read().splitlines())  # Get number of lines in file
    #             await message.channel.send(content= f"There are {answer} songs in the {request} playlist")  # Number of songs in playlist
    #             return

    #     # Get random song from playlist
    #     else:
    #         request = request.replace("!song", "")  # Get playlist name
    #         await message.channel.send(content=random.choice(open(f'song/{request}.txt').read().splitlines()))  # Get random song from playlist
    #         return

    # NEEDS ERROR HANDLING ASAP
    if request.startswith("!d"):
        sides = request.replace("!d", "")
        roll = random.randint(1, int(sides))
        await message.channel.send(content=f"You rolled a {roll}")

    # Return ammount of files in directory
    if request.endswith("amount"):
        directory = request.replace("!","").replace("amount", "") # Get directory name
        answer = os.listdir(directory) # Get list of files in directory
        if directory.endswith("s"):
            plural = ""
        else:
            plural = "s"
        await message.channel.send(content=f"There are {len(answer)} {directory}{plural}") # Number of files
        return

    # Final command since trigger message is so broad
    #  Return random file in directory
    if request.startswith("!"):
        try:
            directory = request.replace("!", "") # Get directory name
            attachment = random.choice(os.listdir(directory)) # Get random file in directory
            path = f"{directory}/{attachment}" # Get path to file
            final = discord.File(path) # Create file object
            await message.channel.send(content=f"Here is your {directory}!", file=final) # Send file
            return
        except FileNotFoundError: # If directory doesn't exist
            pass

@client.event # React to reaction
async def on_reaction_add(reaction, user): 
    if str(reaction.emoji) == "👎":
        if reaction.count == votes:
            try:
                directory = reaction.message.content.replace("Here is your ","").replace("!","") # Get directory name
                attachment = reaction.message.attachments[0].filename # Get file name
                path = f"{directory}/{attachment}" # Get path to file
                os.remove(path) # Delete file
                
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
                    server.login(MAIL_USER, MAIL_PASS)
                    server.sendmail(MAIL_USER, MAIL_USER, f"{path} was deleted")
                return
            except IndexError: # If no file is attached
                pass

client.run(TOKEN)
