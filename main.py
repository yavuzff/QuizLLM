import streamlit as st


st.markdown("# Quiz 🎈")
st.sidebar.markdown("# Quiz 🎈")


# Initialization
if 'quiz' not in st.session_state:
    st.session_state.quiz = {"question_data": []}
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.correct = None
    st.session_state.explanation = None


# Sidebar
st.sidebar.write("Generate questions using GPT 3.5:")
st.sidebar.text_input("Enter topic:", key="topic")
st.sidebar.text_input("Enter OpenAI API Key:", key="user_key")

st.sidebar.write("Or upload your own questions:")
st.sidebar.file_uploader('Upload', label_visibility="collapsed")

st.sidebar.write("Download Quiz Questions:")
st.sidebar.download_button(label="Download", data=str(st.session_state.quiz))

# Main screen
def display_question(contents):
    # contents: dictionary
    # {"question": "", "options": [ , , , ], "answer": "", "explanation": '"}

    st.write(contents['question'])
    st.radio(
        contents['question'],
        contents['options'], key='chosen_answer',
        label_visibility="collapsed")

    st.session_state.correct = contents['answer']
    st.session_state.explanation = contents['answer']

    st.write(f"You have chosen {st.session_state.chosen_answer}")
    st.button("Submit")

def display_score():
    st.write(f"Correct answers: {st.session_state.score}")
    st.write(f"Percentage: {round(st.session_state.score/st.session_state.total, 0)}")


display_question({"question": "What is the name of the school that Harry Potter attends?", "options": ["Durmstrang Institute", "Beauxbatons Academy of Magic", "Hogwarts School of Witchcraft and Wizardry", "Ilvermorny School of Witchcraft and Wizardry"], "answer": "Hogwarts School of Witchcraft and Wizardry", "explanation": "Hogwarts is the primary setting for the Harry Potter series. Durmstrang Institute, Beauxbatons Academy of Magic, and Ilvermorny School of Witchcraft and Wizardry are other wizarding schools in the Harry Potter universe."})

if st.session_state.total != 0:
    display_score()
