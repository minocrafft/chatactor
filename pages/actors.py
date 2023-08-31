import json
from pathlib import Path

import streamlit as st
from streamlit_card import card
from streamlit_extras.switch_page_button import switch_page

from chatactor.model import Actor, CardModel
from functional.variables import COLS, DATADIR
from functional.utils import (
    on_click_card,
    divide_list,
    submit_new_actor,
    load_image,
)
from functional.component import settings
from functional.page import set_page_config, initial_session_state, description


set_page_config()
initial_session_state()

if st.session_state.openai_api_key is None or not st.session_state.openai_api_key:
    description()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    with st.sidebar:
        settings()

    st.title("캐릭터를 선택해주세요 :seedling:")

    actors = [f"{DATADIR}/{file.stem}" for file in Path(DATADIR).glob("*.md")]

    for row in divide_list(actors, COLS):
        columns = st.columns(COLS)
        for file, col in zip(row, columns):
            with col, open(f"{file}.json", "r") as f:
                model = Actor(**json.load(f))
                cardmodel = CardModel(
                    name=model.name,
                    image=f"{file}.jpg",
                    imagedata=load_image(f"{file}.jpg"),
                    content=[
                        model.occupation,
                        f"{model.birth} ~ {model.death if model.death else '현재'}",
                        model.summary,
                    ],
                )
                clicked = card(
                    title=cardmodel.name,
                    text=cardmodel.content,
                    image=cardmodel.imagedata,
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "400px",
                            "margin": "0px",
                            "padding": "0px",
                        }
                    },
                    on_click=lambda: on_click_card(cardmodel),
                )

                if clicked:
                    switch_page("chat")

    st.divider()

    col1, col2 = st.columns([4, 1])
    with col1:
        new_character = st.text_input(
            label="새로운 캐릭터를 입력해보세요 :hatching_chick:",
            placeholder="Here!",
            help="""
            새로운 캐릭터를 입력하면 해당 캐릭터의 프로필을 생성합니다.

            현재 새로운 캐릭터는 Wikipedia에서 찾을 수 있는 인물만 생성할 수 있습니다:exclamation: 
            """,
        )

    with col2:
        button = st.button(
            "Submit",
            type="primary",
            on_click=lambda: submit_new_actor(new_character),
        )
