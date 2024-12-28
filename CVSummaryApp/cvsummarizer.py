from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain_openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

import textwrap

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

def process_docx(docx_file):
    # Add your docx processing code here
    text = ""
    # Docx2txtLoader loads the document
    loader = Docx2txtLoader(docx_file)
    
    # Load documents and split into chunks
    text = loader.load_and_split()
    
    return text

def process_pdf(pdf_file):
    text = ""
    # PyPDFLoader loads a list of PDF Document objects
    loader = PyPDFLoader(pdf_file)
    pages = loader.load()

    for page in pages:
        text += page.page_content
    text = text.replace('\t', ' ')

    # Splits a long document into smaller chunks that can fit into the LLM's model's context window
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=50
    )

    # create_documents() creates documents from a list of texts
    texts = text_splitter.create_documents([text])

    print(len(texts))

    return texts

