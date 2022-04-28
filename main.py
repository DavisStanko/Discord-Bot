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
separator = ", "
commandlist = separator.join(commandlist).replace(',', '\n')
helpmessage = (f"I react to the following commands:\n{commandlist}")

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

    elif message.content.lower().replace(" ", "").startswith("!"):
        print(message.content)
        attachment = random.choice(os.listdir(message.content.lower().replace(" ", "").replace("!", "")))
        print(attachment)
        final = discord.File(f"{message.content.lower().replace('!', '')}/{attachment}")
        await message.channel.send(file=final)


client.run(TOKEN)