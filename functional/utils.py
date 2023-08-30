import requests
import openai
import streamlit as st
import wikipediaapi
import html2text
from PIL import Image


def on_click_card(model):
    st.session_state.character = model


def on_input_new_character(name):
    scraping(name)
    st.experimental_rerun()


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


def scraping(name: str, save_dir: str = "profiles"):
    wiki = wikipediaapi.Wikipedia(
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "ko",
        extract_format=wikipediaapi.ExtractFormat.HTML,
    )
    page = wiki.page(name)
    html = html2text.html2text(page.text)

    with open(f"{save_dir}/{page.title}.md", "w") as f:
        f.write(html)


def markdown_parser(file: str) -> str:
    with open(file, "r") as f:
        return f.read()


def divide_list(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
