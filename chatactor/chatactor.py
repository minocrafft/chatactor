import os
import json
from pathlib import Path

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.chat_models import ChatOpenAI
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import (
    AgentTokenBufferMemory,
)
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
from .model import Actor
from langchain.agents import AgentExecutor


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
    항상 한국어로 답하고, 인물의 시대적인 말투를 사용해라.
    당신은 역사적인 사실에 기반하지 않은 대답을 할 수 없다.
    """

    return prompt


def get_chatactor(name: str, profiles_path: Path) -> AgentExecutor:
    """
    Returns a chatactor agent executor.

    Args:
        name: Name of the chatactor.
        profiles_path: Path to the profiles directory.
    Returns:
        agent_executor: Agent executor for the chatactor.
    """

    name_md = Path(f"{name}.md")
    name_json = Path(f"{name}.json")

    if not profiles_path.is_dir():
        profiles_path.mkdir()

    if not (profiles_path / name_md).exists():
        raise ValueError(f"{name}.md is not found in profiles.")

    if not (profiles_path / name_json).exists():
        raise ValueError(f"{name}.json is not found in profiles.")

    actor = Actor(
        **json.load(
            open(
                str(profiles_path / name_json),
                "r",
                encoding="utf-8",
            )
        )
    )

    # Tools
    loader = TextLoader(file_path=str(profiles_path / name_md))
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)
    retriever = db.as_retriever()
    tool = create_retriever_tool(
        retriever,
        "search_history",
        f"Searches and returns history documents regarding the {actor.name}.",
    )
    tools = [tool]

    # LLM
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Prompt
    memory_key = "chat_history"
    memory = AgentTokenBufferMemory(memory_key=memory_key, llm=llm)
    system_message = SystemMessage(
        content=_build_prompt(actor),
    )
    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)],
    )

    # Agent
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        return_intermediate_steps=True,
    )

    return agent_executor


if __name__ == "__main__":
    name = "이순신"
    path = Path("profiles")
    chatactor = get_chatactor(name, path)
    chatactor({"input": "당신은 어떤 사람인가요?"})
