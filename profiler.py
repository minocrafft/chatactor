import json
from typing import List

from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper
from langchain.prompts import PromptTemplate


def _build_tools() -> List[Tool]:
    search = DuckDuckGoSearchAPIWrapper()
    wiki = WikipediaAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Useful for when you want to search for something on the internet.",
        ),
        Tool(
            name="Wikipedia",
            func=wiki.run,
            description="Useful for when you want to search for something on Wikipedia.",
        ),
    ]
    return tools


def _build_prompt() -> PromptTemplate:
    prefix = """
    You are a Entertainment Reporter. 
    You have been tasked to profile a given person.
    Do not use your own knowledge, use the internet to find the information.

    You have access to the following tools:"""

    suffix = """Begin! Remember to use the tools to find the information.
    The Final Answer is json formatted. as follows:
    You have to find the following information about the person:
    name: the person's name
    image: the url of the person's image
    occupation: the person's occupation
    summary: the summary of the person in 1-2 sentences
    speaking style: the person's speaking style
    birth: the birth of the person formatted in YYYY-MM-DD
    death: the death of the person formatted in YYYY-MM-DD
    events: List of the person's notable events while alive, the items of the list are formatted as follows:
      event_name: the name of the event
        event date: the date of the event formatted in YYYY-MM-DD
        event description: A line of the description of the event
      event_name: the name of the event ...


    Person: {input}
    {agent_scratchpad}"""

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "agent_scratchpad"],
    )

    return prompt


class Profiler(ZeroShotAgent):
    # TODO: Implement this
    # Profiler.run() should save the output to a json file
    pass


def get_profiler(
    tools: List[Tool] | None, prompt: PromptTemplate | None
) -> AgentExecutor:
    if tools is None:
        tools = _build_tools()

    if prompt is None:
        prompt = _build_prompt()

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    tool_names = [tool.name for tool in tools]
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True
    )
    return agent_executor


if __name__ == "__main__":
    tools = _build_tools()
    prompt = _build_prompt()
    profiler = get_profiler(tools=tools, prompt=prompt)

    output = profiler.run("일론 머스크")
    name = output.split('"name":')[-1].split('"')[1]
    json.dump(output, open(f"profiles/{name}.json", "w"), indent=2)
