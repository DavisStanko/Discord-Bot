import os
import random
import discord
from dotenv import load_dotenv  # Loads the .env file
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Bot token
SERVER = os.getenv('DISCORD_SERVER')  # Server ID
ADMIN = os.getenv('DISCORD_ADMIN')  # Admin ID
# spotify
SPOTIFY_PROFILE = os.getenv('SPOTIFY_PROFILE')
CHILL = os.getenv('CHILL')
HEAVY = os.getenv('HEAVY')
ROCK = os.getenv('ROCK')
LIGHT = os.getenv('LIGHT')
RAP = os.getenv('RAP')
POP = os.getenv('POP')
HYPERPOP = os.getenv('HYPERPOP')
NOISE = os.getenv('NOISE')
COUNTRY = os.getenv('COUNTRY')
SIGMA = os.getenv('SIGMA')
BOOMER = os.getenv('BOOMER')
# Email authentication
MAIL_USER = os.getenv('GMAIL_USERNAME')
MAIL_PASS = os.getenv('GMAIL_APP_PASSWORD')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# get a list of all the folders in a directory
def get_child_folders(path):
    return [entry for entry in os.listdir(path) if os.path.isdir(os.path.join(path, entry))]

# get the media paths
main_dir = os.path.dirname(os.path.realpath(__file__))
content_path = os.path.join(main_dir, "internet")
music_path = os.path.join(main_dir, "music")

# get the command lists
content_commands = sorted(["!" + command for command in get_child_folders(content_path)])
music_commands = sorted(["!" + command for command in get_child_folders(music_path)])

# format the command lists
content_commands = "\n".join([f"`{command}`" for command in content_commands])
music_commands = "\n".join([f"`{command}`" for command in music_commands])


# utility help message
utility_commands = "`!info` - Links to my GitHub page.\n" \
                    "`!NdM` - Rolls N M-sided dice where N and M are positive integers.\n" \

# check if a string is in NdM format
def is_valid_dice_format(string):
    pattern = r"\d+d\d+"
    match = re.fullmatch(pattern, string)
    return match is not None

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
    request = message.content.lower()

    # If message is from bot, ignore
    if message.author == client.user:
        return

    # If message is a command
    elif request.startswith('!'):   
        # remove the ! from the request
        request = request[1:]
        
        if request == "help":
            reply = "I can help you with the following commands:\n" \
                    "`!help` - Displays this help message.\n" \
                    "`!content` - Lists content commands.\n" \
                    "`!music` - Lists music commands.\n" \
                    "`!utility` - Lists utility commands."
            await message.channel.send(reply)
            return
            
        if request == "utility":
            reply = f"I react to the following utility commands:\n{utility_commands}"
            await message.channel.send(reply)
            return

        if request in ["content", "content help"]:
            reply = f"I react to the following content commands by sending a random media file from the specified directory:\n{content_commands}"
            await message.channel.send(reply)
            return
            
        if request == "music":
            reply = f"I react to the following music commands by sending a random song from the specified playlist:\n{music_commands}"
            await message.channel.send(reply)
            return

        if request == "info":
            reply = f"https://github.com/DavisStanko/Discord-Bot"
            await message.channel.send(reply)
            return

        # content
        if request in content_commands:
            # get the path to the folder
            folder_path = os.path.join(content_path, request)
            # get a list of all the files in the folder
            files = os.listdir(folder_path)
            # get a random file from the list
            file = random.choice(files)
            # get the path to the file
            file_path = os.path.join(folder_path, file)
            # send the file
            await message.channel.send(f"here is your {request}!", file=discord.File(file_path))
            return
        
        # music
        if request in music_commands:
            # get the path to the folder
            folder_path = os.path.join(music_path, request)
            # get a list of all the files in the folder
            files = os.listdir(folder_path)
            # get a random file from the list
            file = random.choice(files)
            # get the path to the file
            file_path = os.path.join(folder_path, file)
            # send the file
            await message.channel.send(f"here is your {request} song!", file=discord.File(file_path))
            return
        except FileNotFoundError:  # If directory doesn't exist
            pass

        # utility
        # if request is in NdM format
        if is_valid_dice_format(request):
            # split the string into N and M
            N, M = request.split("d")
            # convert N and M to integers
            N = int(N)
            M = int(M)
            # roll the dice
            rolls = [random.randint(1, M) for i in range(N)]
            # format the reply
            reply = f"you rolled {N}d{M} and got {sum(rolls)} ({rolls})"
            await message.channel.send(reply)
            return
            except IndexError:  # If no file is attached
                pass

client.run(TOKEN)
