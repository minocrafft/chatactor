import time
import base64
from typing import Optional

import pandas as pd
import streamlit as st
from PIL import Image
from pydantic import BaseModel
from streamlit_extras.switch_page_button import switch_page


class Actor(BaseModel):
    name: str
    image: Optional[str]
    occupation: Optional[str]
    tone: Optional[str]
    birth: Optional[str]
    death: Optional[str]
    summary: Optional[str]


def load_img(file):
    with open(file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)

    return "data:image/png;base64," + encoded.decode("utf-8")


def on_click_card(key):
    st.session_state.character = key


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


def card(actor: Actor):
    with st.container():
        st.subheader(actor.name)
        col1, col2 = st.columns(2)
        with col1:
            if actor.image:
                st.image(Image.open(actor.image))
            button = st.button(
                "Let's chat !",
                key=actor.name,
                type="primary",
                on_click=lambda: on_click_card(actor),
            )
        with col2:
            table = {k: v for k, v in actor if k not in ("name", "image")}
            headers = ["information"]

            df = pd.DataFrame.from_dict(table, orient="index", columns=headers)
            st.markdown(df.to_markdown())

        st.divider()

    if button:
        switch_page("chat")
