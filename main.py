import os
import random
import discord
from dotenv import load_dotenv
import re
import requests
import json
import html
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
ADMIN = os.getenv('DISCORD_ADMIN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Get a list of all the folders in a directory
def get_child_folders(path):
    return [entry for entry in os.listdir(path) if os.path.isdir(os.path.join(path, entry))]

# Get the media paths
main_dir = os.path.dirname(os.path.realpath(__file__))
content_path = os.path.join(main_dir, "internet")

# Get the command lists
content_commands = sorted(["!" + command for command in get_child_folders(content_path)])

# Format the command lists
content_commands = "\n".join([f"`{command}`" for command in content_commands])

# Utility help message
utility_commands = "`!info` - Links to my GitHub page.\n" \
                   "`!NdM` - Rolls N M-sided dice where N and M are positive integers.\n"

# Check if a string is in NdM format
def is_valid_dice_format(string):
    pattern = r"\d+d\d+"
    match = re.fullmatch(pattern, string)
    return match is not None

# Get a random trivia question
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

@client.event
async def on_ready():
    # Connects to servers from .env
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    # Print out information for debugging
    print(f'{client.user} is connected to the following servers:\n{SERVER}')


@client.event
async def on_message(message):
    request = message.content.lower()

    # If message is from the bot, ignore
    if message.author == client.user:
        return

    # If message is a command
    elif request.startswith('!'):
        # Remove the '!' from the request
        request = request[1:]
        # Remove spaces from the request
        request = request.replace(" ", "")
        # .lower the request
        request = request.lower()

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

        if request == "content":
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
        if request == "trivia":            
            question_data = get_random_question()
            question = question_data['question']
            answers = question_data['answers']
            correct_answer = question_data['correct_answer']

            # Prompt to answer via number
            prompt = "Please answer by sending the number of the correct answer within 10 seconds."
            # Replace &quot; with "
            question = question.replace("&quot;", "\"")
            # Format the question
            question = f"**{question}**\n"
            # Format the answers
            answers = [f"{i+1}. {answer}" for i, answer in enumerate(answers)]
            # Combine the prompt, question, and answers
            reply = question + "\n".join(answers) + "\n" + prompt

            # Send the question and ping the user
            await message.channel.send(f"{message.author.mention}\n{reply}")
            
            # Check if the answer is correct
            def check_answer(m):
                return m.author == message.author and m.channel == message.channel and m.content.strip() in ["1", "2", "3", "4"]

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

        # Content
        if request in content_commands:
            # Get the path to the folder
            folder_path = os.path.join(content_path, request)
            # Get a list of all the files in the folder
            files = os.listdir(folder_path)
            # Get a random file from the list
            file = random.choice(files)
            # Get the path to the file
            file_path = os.path.join(folder_path, file)
            # Send the file
            await message.channel.send(f"Here is your {request}!", file=discord.File(file_path))
            return

        # Utility
        # If request is in NdM format
        if is_valid_dice_format(request):
            # Split the string into N and M
            N, M = request.split("d")
            # Convert N and M to integers
            N = int(N)
            M = int(M)
            # Roll the dice
            rolls = [random.randint(1, M) for i in range(N)]
            # Format the reply
            reply = f"You rolled {N}d{M} and got {sum(rolls)} ({rolls})"
            await message.channel.send(reply)
            return

client.run(TOKEN)
