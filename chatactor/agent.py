from langchain import OpenAI
from langchain.agents.agent import AgentExecutor
from langchain.agents import AgentType, Tool, initialize_agent,load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.utilities import DuckDuckGoSearchAPIWrapper

def get_agent(openai_api_key:str)-> AgentExecutor:
    # Tools setup
    search = DuckDuckGoSearchAPIWrapper(region="kr-kr")
    llm = OpenAI(temperature=0.5, openai_api_key=openai_api_key, streaming=True)
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions",
        ),
    ] + load_tools(["wikipedia"], llm=llm)

    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True,
    ) 

    return agent

