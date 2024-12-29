
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
import unstructured
import iso639
print(dir(iso639))  # Check the available attributes

import openai
# openai.api_requestor._verify_ssl_certs = False





def upload_htmls():
    # Load all the HTML pages in the given folder structure recursively using Directory Loader
    loader = DirectoryLoader(path=r"G:\GenAI\Chatbots\data\www.hrhelpboard.com\hr-policies", use_multithreading=True)
    documents = loader.load()
    print(f"{len(documents)} Pages Loaded")

    # Split loaded documents into Chunks using CharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )
    split_documents = text_splitter.split_documents(documents=documents)
    print(f"Split into {len(split_documents)} Documents...")

    print(split_documents[0].metadata)

    # Upload chunks as vector embeddings into FAISS
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(split_documents, embeddings)
    # Save the FAISS DB locally
    db.save_local("faiss_index")


def faiss_query():
    """
    This function does the following:
    1. Load the local FAISS Database
    2. Trigger a Semantic Similarity Search using a Query
    3. This retrieves semantically matching Vectors from the DB
    """
    embeddings = OpenAIEmbeddings()
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    query = "Explain the candidate onboarding process"
    docs = new_db.similarity_search(query=query)

    for doc in docs:
        print("##--Page--##")
        print(doc.metadata['source'])
        print("##--content--##")
        print(doc.page_content)

if __name__ == "__main__":

    upload_htmls()
    faiss_query()
