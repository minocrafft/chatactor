import streamlit as st
from streamlit_extras.switch_page_button import switch_page


def set_page_config():
    st.set_page_config(page_title="Chat Actor", page_icon="🦜")


def initial_page():
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
