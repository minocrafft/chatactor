import os
import time
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functional.page import set_page_config, initial_page, initial_session_state


set_page_config()
initial_page()


with st.container():
    # check api key
    apikey = os.getenv("OPENAI_API_KEY")
    apikey = st.text_input(
        label="🔑 Credentials",
        type="password",
        value=apikey,
        placeholder="Input your OpenAI API Key!",
    )

    submit = st.button("Submit", type="primary")

    if submit:
        if apikey is None or not apikey or not apikey.startswith("sk-"):
            st.session_state.openai_api_key = None
            st.warning("Invalid OpenAI API Key...  \n\nPlease try again.")
        else:
            st.session_state.openai_api_key = apikey
            st.success("API key set! \n\nYou can start chatting now!")

            with st.spinner("Loading..."):
                time.sleep(2)

            switch_page("chat")
