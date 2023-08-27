import time
import streamlit as st
from streamlit_chat import message
from langchain.callbacks import StreamlitCallbackHandler

from chatactor import get_agent
from functional.page import set_page_config, initial_page, initial_session_state
from functional.component import create_card


set_page_config()
initial_session_state()


def draw_main_page():
    # main pages
    st.markdown(
        """
        # Welcome to 🦜 Chat Actor!

        안녕하세요! Chat Actor에 오신 것을 환영합니다! :wave:

        ### :thinking_face: Chat Actor가 무엇인가요?
        
        Chat Actor는 :red[**롤플레잉 역할 기반의 학습 플랫폼**]입니다.  
        다양한 캐릭터들로부터 대화를 통해 역사를 배우고, 지식을 습득할 수 있습니다.   
        해당 인물과 실제로 대화하며, Chat Actor를 통해 역사를 배워보세요! :nerd_face:
        
        ---

        ### Chat Actor는 어떻게 사용하나요:question:

        1. 사이드바에서 원하는 캐릭터를 선택하거나 궁금한 인물을 찾아보세요 🔍.
        2. 대화를 시작합니다. :speech_balloon:
        3. 캐릭터와 대화하며 다양한 질문을 학습을 진행합니다. :books:
        4. 질문을 토대로 생성된 퀴즈를 풀어보세요! :pencil2:
        5. 퀴즈를 통해 배운 지식을 확인할 수 있습니다. :bulb:

        ---

        ### 지금 시작해보세요! :rocket:

        """
    )


def spinner(message: str):
    # Draw chat with character pages
    with st.spinner(message):
        time.sleep(2)


def draw_chat(character):
    st.title(character)

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    agent = get_agent(st.session_state.openai_api_key)

    prompt = st.chat_input("Message", key="message")
    if prompt:
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(
            st.container(),
            max_thought_containers=int(st.session_state.max_thought_containers),
            expand_new_thoughts=st.session_state.expand_new_thoughts,
            collapse_completed_thoughts=st.session_state.collapse_completed_thoughts,
        )
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


def draw_sidebar():
    # sidebar
    with st.sidebar:
        st.title("Enjoy your character! 🎉")

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

        st.header("Select your character")

        # Search for Databases later
        create_card(
            title="👨‍✈️  이순신 장군",
            image="static/general.png",
            text="""
                    ||information|
                    |---|---|
                    |Name|General Yi|
                    |Occupation|무신|
                    |Tone|No information found|
                    |Birth|1545-04-28|
                    |Death|1598-12-16|
            """,
            key="이순신 장군",
        )

        create_card(
            title="👑  세종대왕",
            image="static/user.png",
            text="""
                    ||information|
                    |---|---|
                    |Name|King sejong|
                    |Occupation|King|
                    |Tone|No information found|
                    |Birth|NaN|
                    |Death|NaN|
            """,
            key="세종대왕",
        )

        st.divider()
        st.header("or Input new character!")
        st.text_input("Name", key="new_character", placeholder="Input...")

        # if input the character name, append to the databases according to template


if st.session_state.openai_api_key is None or not st.session_state.openai_api_key:
    initial_page()

    st.caption("Please return to the home page and enter your :red[OpenAI API key].")
else:
    draw_sidebar()
    character = st.session_state.character

    if not character:
        draw_main_page()
    else:
        draw_chat(character)
