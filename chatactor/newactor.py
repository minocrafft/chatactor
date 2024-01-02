from langchain.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from langchain_community.tools.tavily_search import TavilySearchResults


llm = Ollama(model="llama2")

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()

embeddings = OllamaEmbeddings()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}"),
        (
            "user",
            "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation",
        ),
    ]
)

retriever = vector.as_retriever()
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
history = [
    HumanMessage(content="Can LangSmith help test my LLM applications?"),
    AIMessage(content="Yes!"),
]

print(retriever_chain.invoke({"history": history, "input": "Tell me how"}))
