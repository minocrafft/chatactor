from pathlib import Path
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler

from chatactor import get_chatactor
from functional.page import (
    set_page_config,
    description,
)
from functional.component import settings


set_page_config()


def draw_prechat():
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.image(st.session_state.actor.image, width=300)

        with col2:
            st.title(st.session_state.actor.name)
            st.markdown("\n\n * ".join(st.session_state.actor.content))


def draw_chat():
    if current_actor != st.session_state.actor:
        st.session_state.messages.clear()

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    agent = get_chatactor(
        name=st.session_state.actor.name,
        profiles_path=Path("profiles"),
        openai_api_key=st.session_state.openai_api_key,
    )

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
            response = agent(prompt, callbacks=[st_callback])
            output = response["output"]
            st.write(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
    else:
        st.caption("Please enter a message to begin chatting.")


if (
    "openai_api_key" not in st.session_state
    or not st.session_state.openai_api_key
    or st.session_state.openai_api_key is None
):
    description()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    with st.sidebar:
        settings()

    if not st.session_state.actor:
        st.subheader("캐릭터 화면으로 돌아가 캐릭터를 선택해주세요. :hugging_face:")
    else:
        current_actor = st.session_state.actor
        draw_prechat()
        draw_chat()
