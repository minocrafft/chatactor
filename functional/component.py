import time
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from chatactor.model import Actor
from functional.utils import load_img_from_url


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


# def card(actor: Actor):
#     with st.container():
#         st.subheader(actor.name)
#         col1, col2 = st.columns(2)
#         with col1:
#             if actor.image:
#                 try:
#                     st.image(load_img_from_url(actor.image))
#                 except Exception as e:
#                     print(e)
#         with col2:
#             button = st.button(
#                 "Let's chat !",
#                 key=actor.name,
#                 type="primary",
#                 on_click=lambda: on_click_card(actor),
#             )
#         table = {k: v for k, v in actor if k not in ("name", "image")}
#         headers = ["information"]
#
#         df = pd.DataFrame.from_dict(table, orient="index", columns=headers)
#         st.markdown(df.to_markdown())
#
#         st.divider()
#
#     if button:
#         switch_page("chat")
