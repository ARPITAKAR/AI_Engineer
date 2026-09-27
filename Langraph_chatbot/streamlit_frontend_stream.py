import streamlit as st
from langGraph_backend import chatbot
from langchain_core.messages import HumanMessage

# st.session_state ''' ek dictionary-like storage hai jo ek user ki 
# Streamlit session ke dauraan data ko yaad rakhta hai.'''
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
#st.session_state {'message_history': [] }

# Loading the conversation history 
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
        
#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hello'}

user_input = st.chat_input('Type Here')

if user_input:
    # first add the message to message history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    
    with st.chat_message('user',avatar="🧑"):
        st.text(user_input)
        
    response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=CONFIG)
    
    
    # first add the message to message history
    
    with st.chat_message('assistant',avatar="🤖"):
        ai_message = st.write_stream(
           message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = CONFIG,
                stream_mode = 'messages'
            )
        )
        st.text(ai_message)
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    