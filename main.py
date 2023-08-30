import streamlit as st
import openai
import json
from datetime import datetime
import random
import os
from chat_completion import get_question_from_topic
from aws_connection import upload_to_s3

st.markdown("# QuizLLM 🎈")
st.sidebar.markdown("# QuizLLM 🎈")


# Initialization
if 'quiz' not in st.session_state:
    st.session_state.quiz = {"quiz_data": []}
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.asking_question = False
    st.session_state.submit_button = False
    st.session_state.current_question = None
    st.session_state.chosen_answer = None
    st.session_state.user_quiz = None


# Sidebar
st.sidebar.write("Generate questions!")
topic = st.sidebar.text_input("Enter topic:")
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")

st.sidebar.write("Or upload your own questions:")
uploaded_file = st.sidebar.file_uploader('Upload', label_visibility="collapsed" )

st.sidebar.write("Save Current Quiz:")
dt = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
saved_quiz_name = f"quiz_{dt}.json"
st.sidebar.download_button(label="Download", data=json.dumps(st.session_state.quiz), file_name=saved_quiz_name)

with st.sidebar.expander("Upload to AWS S3"):
    aws_api_key = st.text_input("Enter AWS Access key:", type="password")
    aws_secret_key = st.text_input("Enter AWS Secret key:", type="password")
    bucket_name = st.text_input("Enter Bucket Name:")
    if st.button("Save"):
        if aws_api_key == 'local' and aws_secret_key == 'local':
            upload_to_s3(bucket_name, json.dumps(st.session_state.quiz), saved_quiz_name)
        else:
            upload_to_s3(bucket_name, json.dumps(st.session_state.quiz), saved_quiz_name, aws_api_key, aws_secret_key)
        st.write("Saved to S3!")

# Main screen
def display_question(contents):
    # contents: dictionary
    # {"question": "", "options": [ , , , ], "answer": "", "explanation": '"}
    st.session_state.asking_question = True
    st.write(contents['question'])
    st.radio(
        contents['question'],
        contents['options'], key='chosen_answer',
        label_visibility="collapsed")

    #  st.write(f"You have chosen {st.session_state.chosen_answer}")
    # TODO: display question after submit pressed and disable submit button and options using disabled = st.session_state.disable_choose)
    st.button("Submit", on_click=update_submit)


def update_submit():
    st.session_state.submit_button = True
    st.session_state.asking_question = False


def check_answer():
    st.session_state.quiz["quiz_data"].append(st.session_state.current_question)
    if st.session_state.chosen_answer == st.session_state.current_question['answer']:
        st.markdown(":green[Correct!]")
        st.session_state.score += 1
    else:
        st.markdown(f":red[Incorrect.] Correct answer was {st.session_state.current_question['answer']}")

    st.session_state.total += 1
    st.write(st.session_state.current_question['explanation'])
    display_score()


def display_score():
    st.write(f"Correct answers: {st.session_state.score}")
    st.write(f"Score: {round(st.session_state.score/st.session_state.total, 3)*100}%")


def get_next_question():
    next_question_data = None

    if uploaded_file is not None:
        st.session_state.user_quiz = read_file(uploaded_file)
        if st.session_state.user_quiz is None:
            st.write("Uploaded file is not in the correct format ( must be .json file containing {'quiz_data':[]} ).")
        else:
            next_question_data = st.session_state.user_quiz[st.session_state.total % len(st.session_state.user_quiz)]

    elif topic == '':
        st.write("Please enter a topic.")
    elif (api_key == 'local' and "QUIZ-LLM-PASSWORD" not in os.environ) or ("QUIZ-LLM-PASSWORD" in os.environ and api_key == os.environ.get("QUIZ-LLM-PASSWORD")):
        next_question_data = get_question_from_topic(topic)
    else:
        try:
            next_question_data = get_question_from_topic(topic, api_key)
        except openai.error.AuthenticationError:
            st.write("Please enter a valid OpenAI API key.")

    if next_question_data is not None:
        st.session_state.asking_question = True
        random.shuffle(next_question_data['options'])
        st.session_state.current_question = next_question_data

def read_file(file):
    try:
        data = json.load(file)

        if isinstance(data, dict):
            if 'quiz_data' in data:
                return data['quiz_data']
            else:
                st.write("Error: There isn't a quiz_data key in the json document")

            return None
    except:
        return None


if st.session_state.asking_question:
    st.session_state.submit_button = False
    display_question(st.session_state.current_question)

if st.session_state.submit_button:
    check_answer()
    st.session_state.submit_button = False

if not st.session_state.asking_question:
    st.button("Next Question", on_click=get_next_question())
