# This program is intended to demo the use of the following:
# - Extracts the contents of a webpage, chunks and loads the chunks (documents) into a FAISS db
# - Creates a sample conversation, uses a "create_history_aware_retriever" retrieval chain
# - Can use it to pass the history and ask a follow up question

from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import os
import getpass

openai_api_key = os.getenv("OPENAI_API_KEY")
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPEN_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
    '''
if not openai_api_key:
    raise ValueError("Environment variable OPEN_API_KEY is not set or is empty!")'''

loader = WebBaseLoader("https://www.wikihow.com/Exercise")

docs = loader.load()

# The RecursiveCharacterTextSplitter takes a large text and splits it based on a specified chunk size.
# It does this by using a set of characters. The default characters provided to it are ["\n\n", "\n", " ", ""]
text_splitter = RecursiveCharacterTextSplitter()

chunks = text_splitter.split_documents(docs)

llm = ChatOpenAI(temperature=0, openai_api_key = openai_api_key)

embeddings = OpenAIEmbeddings()

vector = FAISS.from_documents(documents, embeddings)

retriever = vector.as_retriever()

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    {"user", "{input}"},
    {"user", "Given the above conversation, generate a search query to llok up in order to get information relevant to the conversation"}
])

retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

sample_answer = """some key points for exercise beginnetrs are:
    1. Find a near by gym and time to exercise.
    2. Set a routine that suits you.
    and so on.."""

chat_history = [
    HumanMessage(content="What are the key things to consider for someone starting to practice Yoga?"),
    AIMessage(content=sample_answer)
]

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the below context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

document_chain = create_stuff_documents_chain(llm,prompt)

retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

output = retrieval_chain.invoke({
    "chat_history": chat_history,
    "input": "Can you elaborate on the first point?"
})

print(output["output"])