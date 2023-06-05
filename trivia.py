import requests
import json
import random
import html

# Get a random trivia question
def get_random_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    data = json.loads(response.text)
    data = data['results'][0]
    
    question_text = html.unescape(data['question'])
    correct_answer = html.unescape(data['correct_answer'])
    incorrect_answers = [html.unescape(answer) for answer in data['incorrect_answers']]
    answers = incorrect_answers + [correct_answer]
    random.shuffle(answers)
        
    # Bold the question
    question = f"**{question_text}**\n"
    # Enumerate the answers
    answers = [f"{i+1}. {answer}" for i, answer in enumerate(answers)]
    # Prompt to answer via number
    prompt = "Please answer by sending the number of the correct answer within 10 seconds."
    # Combine the prompt, question, and answers
    reply = question + "\n".join(answers) + "\n" + prompt


    return answers, correct_answer, reply