# bot.py
import os
import os.path
import random
import time
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

client = discord.Client()

# Count memes for random meme function
number_of_memes = 0
dir = "memes"
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        number_of_memes += 1
print(number_of_memes)


@client.event  # Connect to discord
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    print(f'{client.user} is connected to the following guilds:\n{SERVER}')


@client.event  # Send message reply
async def on_message(message):
    # If message is from bot, ignore
    if message.author == client.user:
        return

    if message.content.lower().replace(" ", "") == '!meme':
        meme = random.randint(1, number_of_memes)
        try:
            file = discord.File(f"memes/{meme}.gif")
        except:
            try:
                file = discord.File(f"memes/{meme}.mp4")
            except:
                file = discord.File(f"memes/{meme}.png")
        await message.channel.send(file=file, content="")
        
    elif message.content.lower().replace(" ", "") == '!memeamount':
        await message.channel.send(content=number_of_memes)


client.run(TOKEN)
