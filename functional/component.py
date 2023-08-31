import time
import streamlit as st


def spinner(message: str):
    with st.spinner(message):
        time.sleep(2)


def settings():
    # Settings
    with st.expander("⚙️  Settings"):
        st.session_state.expand_new_thoughts = st.checkbox(
            "Expand New Thoughts",
            value=True,
            help="True if LLM thoughts should be expanded by default",
        )

        st.session_state.collapse_completed_thoughts = st.checkbox(
            "Collapse Completed Thoughts",
            value=True,
            help="True if LLM thoughts should be collapsed when they complete",
        )

        st.session_state.max_thought_containers = st.number_input(
            "Max Thought Containers",
            value=4,
            min_value=1,
            help="""
            Max number of completed thoughts to show.\n
            When exceeded, older thoughts will be moved into a 'History' expander.
            """,
        )
