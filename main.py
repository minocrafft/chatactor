import os
from pathlib import Path

import streamlit as st
from langchain import OpenAI
from langchain.agents import AgentType, Tool, initialize_agent,load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.utilities import DuckDuckGoSearchAPIWrapper

from chatactor import playback_callbacks, with_clear_container, get_agent

st.set_page_config(page_title="Chat Actor", page_icon="🦜", layout="centered")

"# 🦜🔗 Chat Actor"

"""
Chat with your favorite celebrities, fictional characters, and historical figures!
"""

openai_api_key = os.environ.get("OPENAI_API_KEY", None)
with st.expander("🔑  Credentials", expanded=False if openai_api_key else True):
    openai_api_key = st.text_input(
        label="OpenAI API Key",
        type="password",
        help="Set this to start chatting!",
        value=openai_api_key,
        label_visibility="hidden",
    )

agent = get_agent(openai_api_key)

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
        help="Max number of completed thoughts to show. When exceeded, older thoughts will be moved into a 'History' expander.",
    )

# Input
user_input = None
with st.form(key="form"):
    if openai_api_key:
        user_input = st.text_input("Submit to Chat!")
        submit_clicked = st.form_submit_button("Submit Question")
    else:
        st.write("Please enter your OpenAI API Key!")
        submit_clicked = st.form_submit_button(disabled=True)


question_container = st.empty()
results_container = st.empty()

# A hack to "clear" the previous result when submitting a new prompt.
if with_clear_container(submit_clicked):
    # Create our StreamlitCallbackHandler
    res = results_container.container()
    streamlit_handler = StreamlitCallbackHandler(
        parent_container=res,
        max_thought_containers=int(max_thought_containers),
        expand_new_thoughts=expand_new_thoughts,
        collapse_completed_thoughts=collapse_completed_thoughts,
    )

    question_container.write(f"**Question:** {user_input}")

    # If we've saved this question, play it back instead of actually running LangChain
    # (so that we don't exhaust our API calls unnecessarily)
    answer = agent.run(user_input, callbacks=[streamlit_handler])
    res.write(f"**Answer:** {answer}")
