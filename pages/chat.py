import streamlit as st
from streamlit_chat import message
from langchain.callbacks import StreamlitCallbackHandler

from chatactor import get_agent
from functional.page import (
    set_page_config,
    description,
    draw_sidebar,
)

from chatactor.model import Actor
from functional.component import settings


set_page_config()


def draw_chat(character: Actor):
    st.title(character.name)

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
    description()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    character = st.session_state.character

    with st.sidebar:
        settings()

    if not character:
        st.subheader("캐릭터 화면으로 돌아가 캐릭터를 선택해주세요. :hugging_face:")
    else:
        draw_chat(character)
