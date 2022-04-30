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

client = discord.Client()

# List of commands
# Space in front of first command is intentional
commandlist = [" !help", "!info", "!meme", "!object", "!frog", "!shrigma", "!chill"]
commandlist = ", ".join(commandlist).replace(',', '\n')
helpmessage = (f"I react to the following commands:\n{commandlist}\nAdd \"amount\" to the end of an applicable command to get the total number of possible files.")

gitrepo = "https://github.com/DavisStanko/Discord-Bot"


@client.event  # Connect to discord
async def on_ready():
    #connects to servers from .env
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    print(f'{client.user} is connected to the following servers:\n{SERVER}')


@client.event  # Send message reply
async def on_message(message):
    # If message is from bot, ignore
    if message.author == client.user:
        return
    
    #deletes a file
    if message.author.id == ADMIN:
        if message.content.replace(" ", "").startswith("!delete"):
            try:
                request = message.content.lower().replace(" ", "").replace("!delete", "")
                os.remove(request)
                await message.channel.send(content=f"Deleted {request}")
            except:
                await message.channel.send(content=f"Could not delete {request}. Format is: !delete command/file.extension")

    elif message.content.lower().replace(" ", "") == "!help":
        await message.channel.send(content=helpmessage)

    elif message.content.lower().replace(" ", "") == "!info":
        await message.channel.send(content=gitrepo)

    #Random song from txt file
    elif message.content.lower().replace(" ", "").startswith("!song"):
        lines = open('list.txt').read().splitlines()
        myline =random.choice(lines)
        await message.content.channel.send(content=myline)

    # Return ammount of files in directory
    elif message.content.lower().replace(" ", "").endswith("amount"):
        try:
            request = message.content.lower().replace(" ", "").replace("!", "").replace("amount", "")
            answer = os.listdir(request)
            await message.channel.send(content=f"There are {len(answer)} {request}s")
        except:
            pass

    # Last resort, return random file in directory
    elif message.content.replace(" ", "").startswith("!"):
        try:
            request = message.content.lower().replace(" ", "").replace("!", "")
            attachment = random.choice(os.listdir(request))
            path = f"{request}/{attachment}"
            final = discord.File(path)
            await message.channel.send(file=final)
        except:
            #Bad command, maybe meant for a different bot
            pass

client.run(TOKEN)