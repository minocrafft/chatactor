import streamlit as st

from functional.component import settings
from functional.page import (
    set_page_config,
    initial_page,
    description,
    characters_page,
    draw_sidebar,
)


if st.session_state.openai_api_key is None or not st.session_state.openai_api_key:
    initial_page()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    draw_sidebar()
    characters_page()
