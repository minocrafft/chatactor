import streamlit as st
from functional.pages import initial_page


if (
    not hasattr(st.session_state, "openai_api_key")
    or st.session_state.openai_api_key is None
    or not st.session_state.openai_api_key
):
    initial_page()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    st.title("Chat Actor")
