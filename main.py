import os
import os.path
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
ADMIN = os.getenv('DISCORD_ADMIN')
SPOTIFY_PROFILE = os.getenv('SPOTIFY_PROFILE')

client = discord.Client()

gitrepo = "https://github.com/DavisStanko/Discord-Bot"

# List of playlistss
# Space in front of first playlists is intentional
playlists = [" chill", "country", "heavy", "light", "pop", "rap"]
playlists = ", ".join(playlists).replace(',', '\n') # Join playlists into one string and format it
songhelpmessage = (f"Add a playlist to the end of the !song command to get a random song from that playlist.\nPlaylists include:\n{playlists}\nAdd \"amount\" after a playlist to get the total number of possible songs. You can find these playlists on my spotify profile: {SPOTIFY_PROFILE}")

# List of commands
# Space in front of first command is intentional
# **!command** means bold
commandlist = [" !help", "!info", "!song", "**!meme**", "**!object**", "**!frog**", "**!shrigma**", "**!chill**"]
commandlist = ", ".join(commandlist).replace(',', '\n') # Join commands into one string and format it
helpmessage = (f"I react to the following commands:\n{commandlist}\nAdd \"amount\" to the end of bold commands to get the total number of possible files.")


@client.event  # Connect to discord
async def on_ready():
    # connects to servers from .env
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    print(f'{client.user} is connected to the following servers:\n{SERVER}')


@client.event  # Send message reply
async def on_message(message):
    request = message.content.lower().replace(' ', '')

    # If message is from bot, ignore
    if message.author == client.user:
        return

    # Deletes a file if admin and !delete is used
    elif message.author.id == ADMIN and request.startswith("!delete"):
        try:
            path = request.replace("!delete", "")
            os.remove(path) # Delete file
            await message.channel.send(content=f"Deleted {path}") # Send confirmation
        except:
            await message.channel.send(content=f"Could not delete {path}. Format is: !delete directory/file.extension") # Send error

    # Send help message
    elif request == "!help":
        await message.channel.send(content=helpmessage)

    # Send info message
    elif request == "!info":
        await message.channel.send(content=gitrepo)

    # Send song help message
    elif request == "!song":
        await message.channel.send(content=songhelpmessage)

    # All other song commands
    elif request.startswith("!song"):
        if request.endswith("amount"):
            if request == "!songamount":  # If no playlist is specified
                await message.channel.send("There are 6 playlists.")  # Number of playlists, hardcoded.
            else:
                request = request.replace("!song", "").replace("amount", "")  # Get playlisr name
                await message.channel.send(content=len(open(f'song/{request}.txt').read().splitlines()))  # Number of songs in playlist

        # Get random song from playlist
        else:
            request = request.replace("!song", "")  # Get playlist name
            await message.channel.send(content=random.choice(open(f'song/{request}.txt').read().splitlines()))  # Get random song from playlist

    # Return ammount of files in directory
    elif request.endswith("amount"):
        directory = request.replace("amount", "") # Get directory name
        answer = os.listdir(directory) # Get list of files in directory
        await message.channel.send(content=f"There are {len(answer)} {request}s") # Number of files

    #  Return random file in directory
    elif request.startswith("!"):
        directory = request.replace("!", "") # Get directory name
        attachment = random.choice(os.listdir(directory)) # Get random file in directory
        path = f"{directory}/{attachment}" # Get path to file
        final = discord.File(path) # Create file object
        await message.channel.send(file=final) # Send file


client.run(TOKEN)
