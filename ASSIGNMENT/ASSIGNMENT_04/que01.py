import streamlit as st
import time

st.title("Chatbot UI")

user_msg = st.text_input("You: ", placeholder ="Type your message here...")

def bot_reply(message):

    reply = f"You said: {message}"
    for word in reply.split():
        yield word + ' '
        time.sleep(0.3)

if user_msg:
    st.markdown(f"**You:** {user_msg}")
    st.write_stream(bot_reply(user_msg))

