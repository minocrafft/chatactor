import json
from pathlib import Path

import streamlit as st
from streamlit_card import card
from streamlit_extras.switch_page_button import switch_page
from langchain.callbacks import StreamlitCallbackHandler

from chatactor.model import Actor, CardModel
from chatactor.profiler import get_profiler
from chatactor.wikipedia import wikipedia2markdown
from functional.variables import COLS, DATADIR
from functional.utils import (
    download_images,
    on_click_card,
    divide_list,
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

    for message in st.session_state.profiler_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    agent = get_profiler(openai_api_key=st.session_state.openai_api_key)
    prompt = st.chat_input("Message", key="message")
    if prompt:
        with st.chat_message("profiler", avatar="🕵"):
            st_callback = StreamlitCallbackHandler(
                st.container(),
                max_thought_containers=int(st.session_state.max_thought_containers),
                expand_new_thoughts=st.session_state.expand_new_thoughts,
                collapse_completed_thoughts=st.session_state.collapse_completed_thoughts,
            )
            output = agent.run(prompt, callbacks=[st_callback])
            summary = json.loads(output)  # json str -> dict

            with open(f"{DATADIR}/{summary['name']}.json", "w") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)  # save as json file

            with st.status(f"{summary['name']}를 조사하는 중.. :mag:", expanded=True):
                wikipedia2markdown(summary["name"])

            with st.status(f"{summary['name']}의 사진을 가져오는 중.. :camera:", expanded=True):
                download_images(summary["name"])

            output = summary
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(f"{DATADIR}/{summary['name']}.jpg", use_column_width=True)

            with col2:
                st.write(f"# {summary['name']}")
                st.write(f"{summary['occupation']}")
                st.write(
                    f"{summary['birth']} ~ {summary['death'] if summary['death'] else '현재'}"
                )
                st.write(summary["summary"])

            st.experimental_rerun()
    else:
        st.caption(f"새로운 대화 상대를 검색해보세요. :hugging_face:")
