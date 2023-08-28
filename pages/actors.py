import streamlit as st

from functional.page import (
    set_page_config,
    initial_session_state,
    initial_page,
    actors_page,
    draw_sidebar,
)

set_page_config()
initial_session_state()

if st.session_state.openai_api_key is None or not st.session_state.openai_api_key:
    initial_page()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    draw_sidebar()
    actors_page()
