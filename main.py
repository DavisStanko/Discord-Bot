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
commandlist = ["!help", "!meme", "!meme amount"]
separator = ", "
commandlist = separator.join(commandlist).replace(',', '\n').replace(" ", "")
helpmessage = (f"I react to the following commands:\n{commandlist}")

# Number of votes to notify the dev
votes = 1

# Count memes for !meme function
number_of_memes = 0
dir = "memes"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        number_of_memes += 1
print(number_of_memes)

# Count spinningObjects for !object function
number_of_spinningObjects = 0
dir = "spinningObjects"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        number_of_spinningObjects += 1
print(number_of_spinningObjects)

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

    elif message.content.lower().replace(" ", "") == '!meme':
        meme = random.randint(1, number_of_memes)
        try:
            file = discord.File(f"memes/{meme}.gif")
        except:
            try:
                file = discord.File(f"memes/{meme}.mp4")
            except:
                file = discord.File(f"memes/{meme}.png")
        await message.channel.send(file=file)

    elif message.content.lower().replace(" ", "") == '!memeamount':
        await message.channel.send(content=number_of_memes)
    
    elif message.content.lower().replace(" ", "") == '!object':
        spinningObject = random.randint(1, number_of_spinningObjects)
        file = discord.File(f"spinningObjects/{spinningObject}.gif")
        await message.channel.send(file=file)

    elif message.content.lower().replace(" ", "") == '!objectamount':
        await message.channel.send(content=number_of_spinningObjects)
    
client.run(TOKEN)
