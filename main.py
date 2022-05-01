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
commandlist = [" !help", "!info", "!song", "**!meme**", "**!object**", "**!frog**", "**!shrigma**", "**!chill**"]
commandlist = ", ".join(commandlist).replace(',', '\n')
helpmessage = (f"I react to the following commands:\n{commandlist}\nAdd \"amount\" to the end of bold commands to get the total number of possible files.")

gitrepo = "https://github.com/DavisStanko/Discord-Bot"

songhelpmessage = ("Add a playlist to the end of the !song command to get a random song from that playlist.\nPlaylists include:\nchill\ncountry\nheavy\nlight\npop\nrap\nAdd \"amount\" after a playlist to get the total number of possible songs.")

playlists = ["chill", "country", "heavy", "light", "pop", "rap"]

#Split songs
chill = open('song/chill.txt').read().splitlines()
country = open('song/country.txt').read().splitlines()
heavy = open('song/heavy.txt').read().splitlines()
light = open('song/light.txt').read().splitlines()
pop = open('song/pop.txt').read().splitlines()
rap = open('song/rap.txt').read().splitlines()

chillamount = len(chill)
countryamount = len(country)
heavyamount = len(heavy)
lightamount = len(light)
popamount = len(pop)
rapamount = len(rap)


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

    elif message.content.lower().replace(" ", "") == "!test":
        await message.channel.send(content='test')

    #Random song from txt file
    elif message.content.replace(" ", "").startswith("!song"):
        if message.content.lower().replace(" ", "").endswith("amount"):
            if message.content.lower().replace(" ", "") == "!songchill":
                await message.channel.send(chillamount)
            elif message.content.lower().replace(" ", "") == "!songcountry":
                await message.channel.send(countryamount)
            elif message.content.lower().replace(" ", "") == "!songheavy":
                await message.channel.send(heavyamount)
            elif message.content.lower().replace(" ", "") == "!songlight":
                await message .channel.send(lightamount)
            elif message.content.lower().replace(" ", "") == "!songpop":
                await message.channel.send(popamount)
            elif message.content.lower().replace(" ", "") == "!songrap":
                await message.channel.send(rapamount)
        elif message.content.lower().replace(" ", "") == "!song":
            await message.channel.send(content=songhelpmessage)
        elif message.content.lower().replace(" ", "") == "!songchill":
            await message.channel.send(content=random.choice(chill))
        elif message.content.lower().replace(" ", "") == "!songcountry":
            await message.channel.send(content=random.choice(country))
        elif message.content.lower().replace(" ", "") == "!songheavy":
            await message.channel.send(content=random.choice(heavy))
        elif message.content.lower().replace(" ", "") == "!songlight":
            await message .channel.send(content=random.choice(light))
        elif message.content.lower().replace(" ", "") == "!songpop":
            await message.channel.send(content=random.choice(pop))
        elif message.content.lower().replace(" ", "") == "!songrap":
            await message.channel.send(content=random.choice(rap))  

    # Return ammount of files in directory
    elif message.content.lower().replace(" ", "").endswith("amount"):
        request = message.content.lower().replace(" ", "").replace("!", "").replace("amount", "")
        answer = os.listdir(request)
        await message.channel.send(content=f"There are {len(answer)} {request}s")

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