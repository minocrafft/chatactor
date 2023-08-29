import streamlit as st

from functional.component import settings
from functional.page import (
    set_page_config,
    initial_session_state,
    description,
    actors_page,
)

set_page_config()
initial_session_state()

if st.session_state.openai_api_key is None or not st.session_state.openai_api_key:
    description()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    with st.sidebar:
        settings()

    actors_page()
