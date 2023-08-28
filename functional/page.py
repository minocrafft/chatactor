import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functional.component import settings, card


def set_page_config():
    st.set_page_config(page_title="Chat Actor", page_icon="🦜")


def initial_session_state():
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "character" not in st.session_state:
        st.session_state.character = ""


def initial_page():
    st.markdown(
        """
        # Welcome to 🦜 Chat Actor!

        This is a **:red[history studying platform]** based on role-playing chatbots 🤖.

        You can learn history by chatting with a chatbot that acts as a historical figure.

        To start, Please enter your **OpenAI API key** 🔑.

        Enjoy our system! 🎉

        """
    )
    st.divider()


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

        ## 지금 시작해보세요! :rocket:

        """
    )


def characters_page():
    st.title("Enjoy your character! 🎉")
    st.header("Select your character")

    # Search for Databases later
    card(
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

    card(
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

    st.header("or Input new character!")
    st.chat_input("Input new character", key="new_character")

    # if input the character name, append to the databases according to template


def draw_sidebar():
    with st.sidebar:
        settings()
        description()
