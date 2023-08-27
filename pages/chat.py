import streamlit as st
from functional.page import set_page_config, initial_page, initial_session_state
from functional.component import create_character


set_page_config()
initial_session_state()


if (
    not hasattr(st.session_state, "openai_api_key")
    or st.session_state.openai_api_key is None
    or not st.session_state.openai_api_key
):
    initial_page()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    # main pages
    st.title(st.session_state.character or "Chat Actor")
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

        # Search for Databases later
        create_character(
            title="👨‍✈️  General Yi",
            image="static/general.png",
            text="""
                    ||information|
                    |---|---|
                    |Name|General Yi|
                    |Occupation|무신|
                    |Tone|No information found|
                    |Birth|1545-04-28|
                    |Death|1598-12-16|
            """,
            key="General Yi",
        )

        create_character(
            title="👑  King Sejong",
            image="static/user.png",
            text="""
                    ||information|
                    |---|---|
                    |Name|King sejong|
                    |Occupation|King|
                    |Tone|No information found|
                    |Birth|NaN|
                    |Death|NaN|
            """,
            key="King sejong",
        )

        st.divider()
        st.header("or Input new character!")
        st.text_input("Name", key="new_character", placeholder="Input...")

        # if input the character name, append to the databases according to template
