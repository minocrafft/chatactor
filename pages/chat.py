import streamlit as st
from functional.page import set_page_config, initial_page


set_page_config()


if (
    not hasattr(st.session_state, "openai_api_key")
    or st.session_state.openai_api_key is None
    or not st.session_state.openai_api_key
):
    initial_page()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    st.title("Chat Actor")
    st.sidebar.title("Enjoy your chat! 🎉")
    st.chat_input("Message", key="message")
