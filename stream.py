import streamlit as st
import requests
import uuid
import backend 



# Session state variable for theme
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "new_conversation_requested" not in st.session_state:
    st.session_state.new_conversation_requested = "False"

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = [] 

session_structure = {
    "id": None,
    "timestamp": None,  # Optional
    "chat_history": st.session_state.chat_history
}

chat_sessions = []

def display_chat_history(chat_history=None):
    if chat_history is None:
        chat_history = st.session_state.chat_history

    for message in chat_history:
        if message['sender'] == 'user':
            st.write('YOU: ', message['text'])
        elif message['sender'] == 'bot':
            st.write('BOT: ', message['text'])

def create_new_session():
  new_session = session_structure.copy()  # Create a copy of the session structure
  new_session["id"] =str(uuid.uuid4())
  st.session_state.chat_sessions.append(new_session)

if st.session_state is None:
    create_new_session()
if st.sidebar.button("New Conversation"):
    create_new_session()

for i, session in enumerate(st.session_state.chat_sessions):
    if st.sidebar.button(f"Session {session['id']}"):
        st.session_state.selected_chat_history = session['chat_history']

def set_theme():
  if st.session_state.theme == "light":
    st._config.set_option('theme.backgroundColor', "white")
    st._config.set_option('theme.base', "light")
    st._config.set_option('theme.primaryColor', "#5591f5")
    st._config.set_option('theme.secondaryBackgroundColor', "white")
    st._config.set_option('theme.textColor', "#0a1464")
  else:
    st._config.set_option('theme.backgroundColor', "black")
    st._config.set_option('theme.base', "dark")
    st._config.set_option('theme.primaryColor', "#c98bdb")
    st._config.set_option('theme.secondaryBackgroundColor', "black")
    st._config.set_option('theme.textColor', "white")

# Dark mode toggle button (integrated into bottom_container)
bottom_container = st.sidebar.container(height=110)


with bottom_container:
    part1,part2 = st.columns(2)
    with part1:
        st.write('Dark mode')
        st.write("Language") 
    with part2:
        theme_toggle = st.toggle(" ")
        st.button("ENG US")
    # Theme logic based on toggle button and session state
    if theme_toggle:
        if st.session_state.theme == "light":
            st.session_state.theme = "dark"
        else:
            st.session_state.theme = "light"
set_theme()


def get_current_session_index():
  current_session_id = st.session_state.get("selected_session_id", None)
  if current_session_id:
    for i, session in enumerate(chat_sessions):
      if session["id"] == current_session_id:
        return i
  return -1

def answer_callback(question):
    
    chat_history = st.session_state.chat_history
    answer = backend.get_answer(question,chat_history)

    update_chat_history = chat_history + [{'sender': 'user', 'text':question},
                                        {'sender': 'bot', 'text': answer.get("output")}]
    
    current_session_index = get_current_session_index()
    if current_session_index != -1:
        chat_sessions[current_session_index]["chat_history"] = update_chat_history
    

    
    st.session_state.chat_history = update_chat_history
    return answer
    
    

holder = st.container(height=400,border=True)
    

# User input for question
box = st.container(border=True)
with box:
    question = st.chat_input("Ask a question ")
with holder:
    if question:
        answer = answer_callback(question)
        
    current_session_index = get_current_session_index()
       
    if current_session_index != -1:
        display_chat_history(chat_sessions[current_session_index]["chat_history"])
    else:
    # Display empty history if no session is active
        display_chat_history()
    
    

if st.sidebar.button("Clear Conversation"):
    holder.empty()