import streamlit as st
from chat_completion import test
import json
from datetime import datetime

st.markdown("# Quiz 🎈")
st.sidebar.markdown("# Quiz 🎈")


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
st.sidebar.write("Generate questions using GPT 3.5:")
topic = st.sidebar.text_input("Enter topic:", key="topic")
api_key = st.sidebar.text_input("Enter OpenAI API Key:", key="user_key")

st.sidebar.write("Or upload your own questions:")
uploaded_file = st.sidebar.file_uploader('Upload', label_visibility="collapsed" )

st.sidebar.write("Download Current Quiz:")
dt = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
st.sidebar.download_button(label="Download", data=json.dumps(st.session_state.quiz), file_name=f"quiz_{dt}.json")


# Main screen
def display_question(contents):
    # contents: dictionary
    # {"question": "", "options": [ , , , ], "answer": "", "explanation": '"}
    st.session_state.quiz["quiz_data"].append(contents)
    st.session_state.asking_question = True
    st.write(contents['question'])
    st.radio(
        contents['question'],
        contents['options'], key='chosen_answer',
        label_visibility="collapsed")

    st.write(f"You have chosen {st.session_state.chosen_answer}")
    # TODO: display question after submit pressed and disable submit button and options using disabled = st.session_state.disable_choose)
    st.button("Submit", on_click=update_submit)

def update_submit():
    st.session_state.submit_button = True
    st.session_state.asking_question = False

def check_answer():
    print('checking answer')
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
    st.write(f"Percentage: {round(st.session_state.score/st.session_state.total, 2)}")

def is_valid_api_key(key):
    return key == 'secret'

def get_next_question():
    print('clicked next question')
    next_question_data = None

    if uploaded_file is not None:
        st.session_state.user_quiz = read_file(uploaded_file)
        if st.session_state.user_quiz is None:
            st.write("Uploaded file is not in the correct format ( must be .json file containing {'quiz_data':[]} ).")
        else:
            next_question_data = st.session_state.user_quiz[st.session_state.total % len(st.session_state.user_quiz)]

    elif topic == '':
        st.write("Please enter a topic.")
    elif not is_valid_api_key(api_key):
        st.write("Please enter a valid OpenAI API key.")
    else:
        next_question_data = test(topic)

    if next_question_data is not None:
        st.session_state.asking_question = True
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
