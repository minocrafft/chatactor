import json

from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

from functional.component import Actor


def _build_prompt(actor: Actor) -> str:
    prompt = f"당신은 '{actor.name}'이다.\n"
    if actor.summary:
        prompt += actor.summary

    if actor.occupation:
        prompt += f"직업은 {actor.occupation} 이다.\n"
    if actor.speaking_style:
        prompt += f"당신은 과장되게 '{actor.speaking_style}' 스타일로 말한다.\n"
    if actor.birth:
        prompt += f"당신은 {actor.birth}에 태어났다.\n"
        if actor.death not in [None, "N/A"]:
            prompt += f"당신은 {actor.death}에 죽었다.\n"
        else:
            prompt += f"당신은 아직 2023년 현재에 살고 있다.\n"
    prompt += "당신은 다음과 같은 사건들을 겪었다:\n"
    if actor.events is not None:
        for event in actor.events:
            prompt += f"  - {event.event_name} ({event.event_date})\n"
    prompt += """

    당신은 역사적인 인물 또는 유명인으로써 사용자와 대화를 나누고 있다.
    항상 한국어로 답하고, 해요체를 사용해라.
    당신은 역사적인 사실에 기반하지 않은 대답을 할 수 없다.
    """
    return prompt


def get_chatactor(actor: Actor) -> LLMChain:
    prompt = _build_prompt(actor)

    memory = ConversationBufferMemory()

    llm = ChatOpenAI()

    prompt_template = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}"),
        ],
        input_variables=["question", "chat_history"],
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

    chatactor_chain = LLMChain(
        llm=llm, prompt=prompt_template, verbose=True, memory=memory
    )

    return chatactor_chain


if __name__ == "__main__":
    path = "profiles/세종대왕.json"
    actor = Actor(
        **json.load(
            open(
                path,
                "r",
                encoding="utf-8",
            )
        )
    )
    chatactor = get_chatactor(actor)

    print(chatactor({"question": "당신에 대해 알려주세요."})["text"])
    print(chatactor({"question": "왜 한글을 만드셨나요?"})["text"])
    print(chatactor({"question": "함께 작업한 사람은 누구인가요?"})["text"])
