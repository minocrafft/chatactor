import time
import base64
import streamlit as st
from PIL import Image
from streamlit_card import card

from functional.page import set_page_config, initial_page


def load_img(file):
    with open(file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)

    return "data:image/png;base64," + encoded.decode("utf-8")


set_page_config()


if (
    not hasattr(st.session_state, "openai_api_key")
    or st.session_state.openai_api_key is None
    or not st.session_state.openai_api_key
):
    initial_page()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    # main pages
    st.title("Chat Actor")
    st.chat_input("Message", key="message")

    # sidebar
    with st.sidebar:
        st.title("Enjoy your chat! :nerd_face:")

        # Settings
        with st.expander("⚙️  Settings"):
            expand_new_thoughts = st.checkbox(
                "Expand New Thoughts",
                value=True,
                help="True if LLM thoughts should be expanded by default",
            )

            collapse_completed_thoughts = st.checkbox(
                "Collapse Completed Thoughts",
                value=True,
                help="True if LLM thoughts should be collapsed when they complete",
            )

            max_thought_containers = st.number_input(
                "Max Thought Containers",
                value=4,
                min_value=1,
                help="""
                Max number of completed thoughts to show.\n
                When exceeded, older thoughts will be moved into a 'History' expander.
                """,
            )

        st.header("Select your character")

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.title("👨‍✈️  General Yi")
                st.image(Image.open("static/general.png"))
            with col2:
                st.markdown(
                    """
                    ||information|
                    |---|---|
                    |Name|General Yi|
                    |Occupation|무신|
                    |Tone|No information found|
                    |Birth|1545-04-28|
                    |Death|1598-12-16|
                    """
                )
            st.button("Select", key="Yi", type="primary")

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.title("👑  King Sejong")
                st.image(Image.open("static/user.png"))
            with col2:
                st.markdown(
                    """
                    ||information|
                    |---|---|
                    |Name|King sejong|
                    |Occupation|King|
                    |Tone|No information found|
                    |Birth|NaN|
                    |Death|Nan|
                    """
                )
            st.button("Select", key="sejong", type="primary")

        # character selection
        card(
            title="👑  King Sejong",
            text="The 4th king of the Joseon Dynasty",
            image=load_img("static/user.png"),
        )

        card(
            title="👨🏻‍✈️  General Yi",
            text="The greatest admiral in Korean history",
            image=load_img("static/general.png"),
        )

        st.divider()
        st.header("or Input new character!")
        st.text_input("Name", key="new_character", placeholder="Input...")
