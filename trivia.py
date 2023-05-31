import requests
import json
import random
import html

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
    
    # Decode HTML entities from question_data
    for key, value in question_data.items():
        question_data[key] = html.unescape(value)
        
    # Bold the question
    question = f"**{question}**\n"
    # Enumerate the answers
    answers = [f"{i+1}. {answer}" for i, answer in enumerate(answers)]
    # Prompt to answer via number
    prompt = "Please answer by sending the number of the correct answer within 10 seconds."
    # Combine the prompt, question, and answers
    reply = question + "\n".join(answers) + "\n" + prompt


    return question_data['answers'], question_data['correct_answer'], reply