import os

import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

from chatactor import get_agent

st.set_page_config(page_title="Chat Actor", page_icon="🦜", layout="centered")

"# 🦜🔗 Chat Actor"

"""
Chat with your favorite celebrities, fictional characters, and historical figures!
"""

def is_key_valid(key: str) -> bool:
    if len(key) == 0:
        return False

    if not key.startswith('sk-'):
        return False

    return True


openai_api_key = os.getenv("OPENAI_API_KEY", "")
with st.expander("🔑  Credentials", expanded=openai_api_key == ""):
    openai_api_key = st.text_input(
        label="OpenAI API Key",
        type="password",
        help="Set this to start chatting!",
        label_visibility="hidden",
    )

    if is_key_valid(openai_api_key):
        st.session_state.openai_api_key = openai_api_key
        st.success("API key set!")
    else:
        st.warning("Invalid API key")


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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if (prompt := st.chat_input(
    placeholder="Type something to start chatting!",
    disabled=not is_key_valid(openai_api_key),
)) and st.session_state.openai_api_key:
    agent = get_agent(st.session_state.openai_api_key)

    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
