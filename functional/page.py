import math
import json
from pathlib import Path

import streamlit as st
from streamlit_card import card
from streamlit_extras.switch_page_button import switch_page
from pydantic import ValidationError

from chatactor.model import Actor
from functional.utils import on_click_card
from functional.component import settings  # , card


COLS = 2
DB_ACTORS = "profiles/"


def set_page_config():
    st.set_page_config(page_title="Chat Actor", page_icon="🦜")


def initial_session_state():
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "character" not in st.session_state:
        st.session_state.character = ""


def description():
    # main pages
    st.markdown(
        """
        # Welcome to 🦜 Chat Actor!

        안녕하세요! Chat Actor에 오신 것을 환영합니다! :wave:

        ## :thinking_face: Chat Actor가 무엇인가요?
        
        Chat Actor는 :red[**롤플레잉 역할 기반의 학습 플랫폼**]입니다.  
        다양한 캐릭터들로부터 대화를 통해 역사를 배우고, 지식을 습득할 수 있습니다.   
        해당 인물과 실제로 대화하며, Chat Actor를 통해 역사를 배워보세요! :nerd_face:
        
        ---

        ## Chat Actor는 어떻게 사용하나요:question:

        1. 사이드바에서 원하는 캐릭터를 선택하거나 궁금한 인물을 찾아보세요 🔍.
        2. 대화를 시작합니다. :speech_balloon:
        3. 캐릭터와 대화하며 다양한 질문과 학습을 진행합니다. :books:
        4. 질문을 토대로 생성된 퀴즈를 풀어보세요! :pencil2:
        5. 퀴즈를 통해 배운 지식을 확인할 수 있습니다. :bulb:

        ---

        ### 지금 시작해보세요! :rocket:

        """
    )


def actors_page():
    st.title("캐릭터를 선택해주세요 :seedling:")

    actors = [str(file) for file in Path(DB_ACTORS).glob("*.json")]
    rows = math.ceil(len(actors) / COLS)
    columns = {i: st.columns(COLS) for i in range(rows)}

    i = 0
    for row in range(rows):
        for col in columns[row]:
            with col, open(actors[i], "r") as file:
                model = Actor(**json.load(file))

                clicked = card(
                    title=model.name,
                    image=model.image,
                    text=model.summary,
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "400px",
                            "margin": "0px",
                            "padding": "0px",
                        }
                    },
                    on_click=lambda: on_click_card(model),
                )

                if clicked:
                    switch_page("chat")

                i += 1
                if i >= len(actors):
                    break

    st.divider()
    st.header("or Input new character!")
    st.chat_input("Input new character", key="new_character")


def draw_sidebar():
    with st.sidebar:
        settings()
        description()
