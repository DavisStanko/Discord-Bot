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

songhelpmessage = (f"Add a playlist to the end of the !song command to get a random song from that playlist.\nPlaylists include:\nchill\ncountry\nheavy\nlight\npop\nrap\nAdd \"amount\" after a playlist to get the total number of possible songs. You can find these playlists on my spotify profile: {SPOTIFY_PROFILE}")

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
                await message.channel.send(f"There are 6 playlists.") # Hardcoded for now
            elif request == "!songchillamount":
                await message.channel.send(f"There are {chillamount} songs in the chill playlist.")
            elif request == "!songcountryamount":
                await message.channel.send(f"There are {countryamount} songs in the country playlist.")
            elif request == "!songheavyamount":
                await message.channel.send(f"There are {heavyamount} songs in the heavy playlist.")
            elif request == "!songlightamount":
                await message .channel.send(f"There are {lightamount} songs in the light playlist.")
            elif request == "!songpopamount":
                await message.channel.send(f"There are {popamount} songs in the pop playlist.")
            elif request == "!songrapamount":
                await message.channel.send(f"There are {rapamount} songs in the rap playlist.")
        # Get random song from playlist
        elif request == "!songchill":
            await message.channel.send(content=random.choice(chill))
        elif request == "!songcountry":
            await message.channel.send(content=random.choice(country))
        elif request == "!songheavy":
            await message.channel.send(content=random.choice(heavy))
        elif request == "!songlight":
            await message .channel.send(content=random.choice(light))
        elif request == "!songpop":
            await message.channel.send(content=random.choice(pop))
        elif request == "!songrap":
            await message.channel.send(content=random.choice(rap))  

    # Return ammount of files in directory
    elif request.endswith("amount"):
        directory = request.replace("amount", "")
        answer = os.listdir(directory)
        await message.channel.send(content=f"There are {len(answer)} {request}s")

    #  Return random file in directory
    elif request.startswith("!"):
        try:
            directory = request.replace("!", "")
            attachment = random.choice(os.listdir(directory))
            path = f"{request}/{attachment}"
            final = discord.File(path)
            await message.channel.send(file=final)
        except:
            #Bad command, maybe meant for a different bot
            pass
    
    #Last resort, deletes a file if admin
    if message.author.id == ADMIN:
        if request == ("!delete"):
            try:
                request = message.content.lower().replace(" ", "").replace("!delete", "")
                os.remove(request)
                await message.channel.send(content=f"Deleted {request}")
            except:
                await message.channel.send(content=f"Could not delete {request}. Format is: !delete command/file.extension")

client.run(TOKEN)