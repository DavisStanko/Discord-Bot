# bot.py
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

# List of commands
# Space in front of first command is intentional
commandlist = [" !help", "!info", "!song", "**!meme**", "**!object**", "**!frog**", "**!shrigma**", "**!chill**"]
commandlist = ", ".join(commandlist).replace(',', '\n')
helpmessage = (f"I react to the following commands:\n{commandlist}\nAdd \"amount\" to the end of bold commands to get the total number of possible files.")

gitrepo = "https://github.com/DavisStanko/Discord-Bot"

# List of playlistss
# Space in front of first playlists is intentional
playlists = [" chill", "country", "heavy", "light", "pop", "rap"]
playlists = ", ".join(playlists).replace(',', '\n')
songhelpmessage = (f"Add a playlist to the end of the !song command to get a random song from that playlist.\nPlaylists include:\n{playlists}\nAdd \"amount\" after a playlist to get the total number of possible songs. You can find these playlists on my spotify profile: {SPOTIFY_PROFILE}")

playlists = ["chill", "country", "heavy", "light", "pop", "rap"]

@client.event  # Connect to discord
async def on_ready():
    #connects to servers from .env
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
    
    elif request == "!help":
        await message.channel.send(content=helpmessage)

    elif request == "!info":
        await message.channel.send(content=gitrepo)
        
    elif request == "!song":
        await message.channel.send(content=songhelpmessage)

    #All song commands
    elif request.startswith("!song"):
        #Get number of songs in playlist
        if request.endswith("amount"):
            if request == "!songamount": #If no playlist is specified
                await message.channel.send(f"There are {len(playlists)} playlists.") # Number of playlists
            else:
                request = request.replace("!song", "").replace("amount", "")
                await message.channel.send(content=len(open(f'song/{request}.txt').read().splitlines()))
            
        # Get random song from playlist
        else:
            request = request.replace("!song", "")
            await message.channel.send(content=random.choice(open(f'song/{request}.txt').read().splitlines()))

    # Return ammount of files in directory
    elif request.endswith("amount"):
        directory = request.replace("amount", "")
        answer = os.listdir(directory)
        await message.channel.send(content=f"There are {len(answer)} {request}s")

    #  Return random file in directory
    elif request.startswith("!"):
        directory = request.replace("!", "")
        attachment = random.choice(os.listdir(directory))
        path = f"{directory}/{attachment}"
        final = discord.File(path)
        await message.channel.send(file=final)
    
    #Last resort, deletes a file if admin
    elif message.author.id == ADMIN:
        if request == ("!delete"):
            try:
                request = message.content.lower().replace(" ", "").replace("!delete", "")
                os.remove(request)
                await message.channel.send(content=f"Deleted {request}")
            except:
                await message.channel.send(content=f"Could not delete {request}. Format is: !delete command/file.extension")

client.run(TOKEN)