# bot.py
import os
import os.path
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

client = discord.Client()

# List of commands
# Space in front of first command is intentional
commandlist = [" !help", "!info", "!meme", "!object", "!frog", "!shrigma"]
commandlist = ", ".join(commandlist).replace(',', '\n')
helpmessage = (f"I react to the following commands:\n{commandlist}\nAdd \"amount\" to the end of a command to get the total number of possible files.")

gitrepo = "https://github.com/DavisStanko/Discord-Bot"


@client.event  # Connect to discord
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    print(f'{client.user} is connected to the following servers:\n{SERVER}')


@client.event  # Send message reply
async def on_message(message):
    # If message is from bot, ignore
    if message.author == client.user:
        return

    elif message.content.lower().replace(" ", "") == "!help":
        await message.channel.send(content=helpmessage)

    elif message.content.lower().replace(" ", "") == "!info":
        await message.channel.send(content=gitrepo)

    elif message.content.lower().replace(" ", "").endswith("amount"):
        try:
            request = message.content.lower().replace(" ", "").replace("!", "").replace("amount", "")
            answer = os.listdir(request)
            await message.channel.send(content=f"There are {len(answer)} {request}s")
        except:
            pass

    elif message.content.replace(" ", "").startswith("!"):
        try:
            request = message.content.lower().replace(" ", "").replace("!", "")
            attachment = random.choice(os.listdir(request))
            path = f"{request}/{attachment}"
            final = discord.File(path)
            await message.channel.send(file=final)
        except:
            pass

client.run(TOKEN)