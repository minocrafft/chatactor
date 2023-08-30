import requests
import openai
import streamlit as st
from io import BytesIO
from PIL import Image

from chatactor.wikipedia import wikipedia2markdown


def on_click_card(model):
    st.session_state.character = model


def on_input_new_character(name):
    if wikipedia2markdown(query=name)
        st.success("New character added!")
        st.experimental_rerun()
    else:
        st.error("Failed to add a new character...  \n\nPlease try again.")


def load_img_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    return img


def validate_openai_api_key(api_key):
    openai.api_key = api_key

    try:
        openai.Completion.create(
            engine="davinci",
            prompt="This is a test.",
            max_tokens=5,
        )
    except Exception as e:
        print(e)
        return False
    else:
        return True


def markdown_parser(file: str) -> str:
    with open(file, "r") as f:
        return f.read()


def divide_list(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
