import app as st
from dataclasses import dataclass
import time as t
from datetime import datetime, time 
from pathlib import Path
from utils import util
from prompts import qna_chain, standalone_ques_chain
from vector_db import store_to_vector, match_context
import os
from dotenv import load_dotenv

load_dotenv()

CONTEXT = "file_context"
PREV_QUES = 'prev_question'
directory_path = os.getenv("UPLOAD_FOLDER")

if CONTEXT not in st.session_state:
    st.session_state[CONTEXT] = ''

if PREV_QUES not in st.session_state:
    st.session_state[PREV_QUES] = ''

def clear_file():
    progress_bar.empty()

st.header("👨🏻‍💻 Ask QnA Assistant")

st.sidebar.header("Upload Report")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=['pdf', 'docx'])

progress_bar = st.empty()
bar = progress_bar.progress(0) 

if uploaded_file and uploaded_file.name:
    filename = uploaded_file.name
    save_path = Path(directory_path, filename)
    with open(save_path, 'wb') as f:
        f.write(uploaded_file.getvalue())

    bar.progress(30) 
    if uploaded_file.name is not None:
        store_to_vector(save_path, filename)
        st.session_state[CONTEXT] = filename

    bar.progress(90) 

    if save_path.exists():
        st.write(f'Report: {uploaded_file.name.capitalize()} !')
    bar.progress(100) 
    
clear_file()



st.sidebar.header("Available Reports")

# List files in the specified directory
try:
    files = os.listdir(directory_path)
except FileNotFoundError:
    st.sidebar.error("Directory not found. Please check the path.")
    files = []

# Display the list of files as a selectbox
if files:
    files.insert(0, "Select a file...")

    selected_file = st.sidebar.selectbox("Choose report:", files)
    if selected_file != "Select a file...":
        save_path = Path(directory_path, selected_file)
        st.session_state[CONTEXT] = selected_file
        st.write(f'Report: {selected_file.capitalize()} !')
else:
    st.sidebar.write("No files found in the directory.")


# Chat Interface section

@dataclass
class Message:
    actor: str
    payload: str

USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"


if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="Hi! How can I help you?")]

for msg in st.session_state[MESSAGES]:
    with st.chat_message(msg.actor):
        st.write(msg.payload)

prompt = st.chat_input("Enter your message...")

if prompt:
    st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
    with st.chat_message(USER):
        st.write(prompt)

    prev_ques = st.session_state[PREV_QUES]
    standalone_ques = standalone_ques_chain.invoke({'prev_ques':prev_ques, 'current_ques':prompt})['text']
    context = match_context(standalone_ques, st.session_state[CONTEXT])
    response = qna_chain.invoke({'context':context, 'query':standalone_ques})
    llm_msg = response['text'].replace('$', '\$')
    st.session_state[PREV_QUES] = standalone_ques
    st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=llm_msg))

    with st.chat_message(ASSISTANT):
        st.write(llm_msg)