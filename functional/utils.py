import base64
import os.path as osp
from urllib import request

import openai
import streamlit as st
from duckduckgo_search import DDGS

from chatactor.wikipedia import wikipedia2markdown


def on_click_card(model):
    st.session_state.actor = model


def add_new_character(key):
    # data = {
    #     "name": name,
    #     "image": search_images(name, count=1)[0].url)
    #
    # }
    with st.spinner():
        if not wikipedia2markdown(query=key):
            st.error(f"{key}: Character does not found...  \n\nPlease try again.")
        else:
            download_images(key)
            st.success("New character added!")


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


def search_images(keywords, count=5):
    with DDGS() as ddgs:
        ddgs_images_gen = ddgs.images(
            keywords,
            region="kr-kr",
            safesearch="on",
            size=None,
            color=None,
            type_image="photo",
            layout="Tall",
            license_image=None,
        )

        return [next(ddgs_images_gen) for _ in range(count)]


def download_images(keywords: str, path: str = "profiles", count: int = 3):
    filepath = osp.join("profiles", f"{keywords}.jpg")
    try:
        images = search_images(keywords, count)
        for img in images:
            request.urlretrieve(img["thumbnail"], filepath)
    except Exception as e:
        print(e)


def load_image(file):
    with open(file, "rb") as f:
        encoded = base64.b64encode(f.read())

    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data


download_images("J. 로버트 오펜하이머")
