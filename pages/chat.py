import time
import streamlit as st
from streamlit_chat import message
from langchain.callbacks import StreamlitCallbackHandler

from chatactor import get_agent
from functional.page import (
    set_page_config,
    initial_page,
    initial_session_state,
    description,
)
from functional.component import settings


set_page_config()
initial_session_state()


def spinner(message: str):
    # Draw chat with character pages
    with st.spinner(message):
        time.sleep(2)


def draw_chat(character):
    st.title(character)

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    agent = get_agent(st.session_state.openai_api_key)

    prompt = st.chat_input("Message", key="message")
    if prompt:
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(
            st.container(),
            max_thought_containers=int(st.session_state.max_thought_containers),
            expand_new_thoughts=st.session_state.expand_new_thoughts,
            collapse_completed_thoughts=st.session_state.collapse_completed_thoughts,
        )
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


if st.session_state.openai_api_key is None or not st.session_state.openai_api_key:
    initial_page()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    character = st.session_state.character

    with st.sidebar:
        settings()
        description()

    # if character:
    #     draw_chat(character)
