import os
import time
import streamlit as st
from streamlit_extras.switch_page_button import switch_page


def on_submit():
    pass


def initialize():
    # set page config
    st.set_page_config(page_title="Chat Actor", page_icon="🦜")

    st.markdown(
        """
        # Welcome to 🦜Chat Actor!

        This is a **:red[history studying platform]** based on role-playing chatbots 🤖.

        You can learn history by chatting with a chatbot that acts as a historical figure.

        To start, Please enter your **OpenAI API key** 🔑.

        Enjoy your chat! 🎉

        """
    )
    st.divider()


initialize()


with st.container():
    # check api key
    apikey = os.getenv("OPENAI_API_KEY")
    apikey = st.text_input(
        label="🔑 Credentials",
        value=apikey,
        type="password",
        placeholder="Input your OpenAI API Key!",
    )

    submit = st.button("Submit", type="primary")

    if submit:
        if apikey is None or not apikey:
            st.session_state.openai_api_key = None
            st.warning("Invalid OpenAI API Key...  \n\nPlease try again.")
        else:
            st.session_state.openai_api_key = apikey
            st.success("API key set! \n\nYou can start chatting now!")

            switch_page("chat")


if "message" not in st.session_state:
    st.session_state.messages = []
