from typing import Optional

import faiss
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.llms import OpenAIChat
from langchain.embeddings import OpenAIEmbeddings
from langchain.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain_experimental.autonomous_agents import BabyAGI


# Define your embedding model
embeddings_model = OpenAIEmbeddings()

# Initialize the vectorstore as empty
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})


todo_prompt = PromptTemplate.from_template(
    "You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list for this objective: {objective}"
)
todo_chain = LLMChain(llm=OpenAI(temperature=0), prompt=todo_prompt)
ddg_wrapper = DuckDuckGoSearchAPIWrapper(region="kr-kr", time='d')
search = DuckDuckGoSearchRun(api_wrapper=ddg_wrapper)
wiki_wrapper = WikipediaAPIWrapper(lang='ko')
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    ),
    Tool(
        name="Wikipedia",
        func=wiki.run,
        description="useful for when you need to answer questions about historical events",
    ),
    Tool(
        name="TODO",
        func=todo_chain.run,
        description="useful for when you need to come up with todo lists. Input: an objective to create a todo list for. Output: a todo list for that objective. Please be very clear what the objective is!",
    ),
]


prefix = """You are an AI who performs one task based on the following objective: {objective}. Take into account these previously completed tasks: {context}."""
suffix = """Question: {task}
{agent_scratchpad}"""
prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["objective", "task", "context", "agent_scratchpad"],
)

llm = OpenAIChat(model='gpt-3.5-turbo-16k', temperature=0, max_tokens=-1)
llm_chain = LLMChain(llm=llm, prompt=prompt)
tool_names = [tool.name for tool in tools]
agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)

OBJECTIVE = "오늘 구미 날씨 예보 요약 만들기"

# Logging of LLMChains
verbose = True
# If None, will keep on going forever
max_iterations: Optional[int] = 10
baby_agi = BabyAGI.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    task_execution_chain=agent_executor,
    verbose=verbose,
    max_iterations=max_iterations,
)

baby_agi({"objective": OBJECTIVE})
