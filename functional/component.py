import base64
import streamlit as st
from PIL import Image
from streamlit_extras.switch_page_button import switch_page


def load_img(file):
    with open(file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)

    return "data:image/png;base64," + encoded.decode("utf-8")


def on_click_card(key):
    st.session_state.character = key


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


def card(title: str, image: str, text: str, key: str):
    with st.container():
        st.title(title)
        col1, col2 = st.columns(2)
        with col1:
            st.image(Image.open(image))
            st.button(
                ":green[Let's chat !]",
                key=key,
                # type="primary",
                on_click=lambda: on_click_card(key),
            )
        with col2:
            st.markdown(text)

        st.divider()
