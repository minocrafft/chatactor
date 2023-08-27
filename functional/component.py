import base64
import streamlit as st
from PIL import Image


def load_img(file):
    with open(file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)

    return "data:image/png;base64," + encoded.decode("utf-8")


def on_click_card(key):
    st.session_state.character = key


def create_character(title: str, image: str, text: str, key: str):
    with st.container():
        st.title(title)
        col1, col2 = st.columns(2)
        with col1:
            st.image(Image.open(image))
            st.button(
                "Select", key=key, type="primary", on_click=lambda: on_click_card(key)
            )
        with col2:
            st.markdown(text)
