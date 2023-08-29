import requests
import openai
import streamlit as st
from io import BytesIO
from PIL import Image


def on_click_card(model):
    st.session_state.character = model


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
