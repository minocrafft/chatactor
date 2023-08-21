from langchain import OpenAI
from langchain.agents.agent import AgentExecutor
from langchain.agents import AgentType, initialize_agent,load_tools

def get_agent(openai_api_key:str)-> AgentExecutor:
    llm = OpenAI(temperature=0.5, openai_api_key=openai_api_key, streaming=True)
    tools = load_tools(["ddg-search", "wikipedia"], llm=llm)
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True,
    ) 

    return agent

