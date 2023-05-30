import os
import random
import discord
from dotenv import load_dotenv  # Loads the .env file
import re
import requests
import json
import html
import asyncio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Bot token
SERVER = os.getenv('DISCORD_SERVER')  # Server ID
ADMIN = os.getenv('DISCORD_ADMIN')  # Admin ID

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# get a list of all the folders in a directory
def get_child_folders(path):
    return [entry for entry in os.listdir(path) if os.path.isdir(os.path.join(path, entry))]

# get the media paths
main_dir = os.path.dirname(os.path.realpath(__file__))
content_path = os.path.join(main_dir, "internet")

# get the command lists
content_commands = sorted(["!" + command for command in get_child_folders(content_path)])

# format the command lists
content_commands = "\n".join([f"`{command}`" for command in content_commands])

# utility help message
utility_commands = "`!info` - Links to my GitHub page.\n" \
                    "`!NdM` - Rolls N M-sided dice where N and M are positive integers.\n" \

# check if a string is in NdM format
def is_valid_dice_format(string):
    pattern = r"\d+d\d+"
    match = re.fullmatch(pattern, string)
    return match is not None

# get a random trivia question
import requests
import json

# Function to fetch a random trivia question with its answer from OTDB API
def get_random_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    data = json.loads(response.text)
    
    question = data['results'][0]
    question_text = html.unescape(question['question'])
    correct_answer = html.unescape(question['correct_answer'])
    incorrect_answers = [html.unescape(answer) for answer in question['incorrect_answers']]
    answers = incorrect_answers + [correct_answer]
    random.shuffle(answers)
    
    question_data = {
        'question': question_text,
        'answers': answers,
        'correct_answer': correct_answer
    }
    
    return question_data

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
                    "`!games` - Lists game commands.\n" \
                    "`!utility` - Lists utility commands."
            await message.channel.send(reply)
            return
            
        if request == "utility":
            reply = f"I react to the following utility commands:\n{utility_commands}"
            await message.channel.send(reply)
            return

        if request in "content":
            reply = f"I react to the following content commands by sending a random media file from the specified directory:\n{content_commands}"
            await message.channel.send(reply)
            return
        
        if request == "games":
            reply = f"I react to the following game commands:\n" \
                    "`!trivia` - Starts a game of trivia."
            await message.channel.send(reply)
            return

        if request == "info":
            reply = f"https://github.com/DavisStanko/Discord-Bot"
            await message.channel.send(reply)
            return
        
        # Trivia
        if message.content == "!trivia":            
            question_data = get_random_question()
            question = question_data['question']
            answers = question_data['answers']
            correct_answer = question_data['correct_answer']
            

            # prompt to answer via number
            prompt = "Please answer by sending the number of the correct answer within 10 seconds."
            # replace &quot; with "
            question = question.replace("&quot;", "\"")
            # format the question
            question = f"**{question}**\n"
            # format the answers
            answers = [f"{i+1}. {answer}" for i, answer in enumerate(answers)]
            # combine the prompt question and answers
            reply = question + "\n".join(answers) + "\n" + prompt     
            
            # send the question
            await message.channel.send(reply)
            
            # check if the answer is correct
            def check_answer(m):
                return m.author == message.author and m.channel == message.channel

            try:
                user_response = await client.wait_for('message', check=check_answer, timeout=10.0)
                user_answer = user_response.content.strip()
                if user_answer.isdigit():
                    user_answer = int(user_answer)
                    if 1 <= user_answer <= len(answers):
                        selected_answer = answers[user_answer - 1]
                        if selected_answer.endswith(correct_answer):
                            await message.channel.send("Correct answer!")
                        else:
                            await message.channel.send("Wrong answer! The correct answer is: " + correct_answer)
                        return
                await message.channel.send("Invalid answer. The correct answer is: " + correct_answer)
            except asyncio.TimeoutError:
                await message.channel.send("Time's up! The correct answer is: " + correct_answer)

            

        
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

client.run(TOKEN)
