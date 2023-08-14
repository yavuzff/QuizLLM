import openai
import json


def get_question_from_topic(topic, history):

    message = [{"role": "user", "content": topic}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=history+message)
    print(response)

    quiz_response = response.choices[0].message.content

    #sample quiz response value:
    #{"question": "What is the name of the school that Harry Potter attends?", "options": ["Durmstrang Institute", "Beauxbatons Academy of Magic", "Hogwarts School of Witchcraft and Wizardry", "Ilvermorny School of Witchcraft and Wizardry"], "answer": "Hogwarts School of Witchcraft and Wizardry", "explanation": "Hogwarts is the primary setting for the Harry Potter series. Durmstrang Institute, Beauxbatons Academy of Magic, and Ilvermorny School of Witchcraft and Wizardry are other wizarding schools in the Harry Potter universe."}

    try:
        return json.loads(quiz_response)
    except ValueError as e:
        raise Exception(f"Cannot convert OpenAI response to JSON. This was the OpenAI response:\n {quiz_response}\n") from e



#uses environment variable or set below
#openai.api_key = api_key

#models = openai.Model.list()
#print(models)

initial_history = [{"role": "system", "content": "You are a quiz generator which when given a topic, returns a question with 4 options, 1 correct answer and an explanation in JSON format."},
                   {"role": "user", "content": "Premier League"},
                   {"role": "assistant", "content": '{"question": "Who is the all-time top scorer in the Premier League?", "options": ["Harry Kane", "Wayne Rooney", "Alan Shearer", "Michael Owen"], "answer": "Alan Shearer", "explanation":"Shearer has scored 260 goals whereas Kane, Rooney and Owen have scored 213, 208 and 150 respectively.}'}
                   ]

#get_question_from_topic("Harry Potter", initial_history)
