import streamlit as st
from langGraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

# st.session_state ''' ek dictionary-like storage hai jo ek user ki 
# Streamlit session ke dauraan data ko yaad rakhta hai.'''
# **************************************** utility functions *************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []
    
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
# An important function of loading on the basis of thread id
def load_converastion(thread_id):
    state = chatbot.get_state(config={'configurable':{'thread_id':thread_id}}) 
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])       

# **************************************** Session Setup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
#st.session_state {'message_history': [] }
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []
    
add_thread(st.session_state['thread_id'])
        
#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hello'}

# ********************************* Sidebar UI ******************
st.sidebar.title('Langgrapher Arpit')

if st.sidebar.button('New Thread'):
    reset_chat()

st.sidebar.title('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']= thread_id
        messages = load_converastion(thread_id)
        temp_messages = []
        for msg in messages:
            if isinstance(msg,HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role':role,'content':msg.content})
        st.session_state['message_history'] = temp_messages
        
# **************************************** Main UI ************************************
# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
                
user_input = st.chat_input('Type Here')

if user_input:
    # first add the message to message history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    
    with st.chat_message('user',avatar="🧑"):
        st.text(user_input)
        
    CONFIG = {'configurable':{'thread_id':st.session_state['thread_id']}}
    # first add the message to message history
    
    with st.chat_message('assistant',avatar="🤖"):
        ai_message = st.write_stream(
           message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = CONFIG,
                stream_mode = 'messages'
            )
        )
        # st.text(ai_message)
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    