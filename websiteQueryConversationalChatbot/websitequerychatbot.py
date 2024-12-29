import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

def query(question, chat_history):
    """
    This function does the following:
    1. Receives two parameters - 'question' - a string and 'chat_history' - a Python List of tuples containing accumulating question-answer pairs
    2. Load the local FAISS database where the entire website is stored as Embedding vectors
    3. Create a ConversationalBufferMemory object with 'chat_history'
    4. Create a ConversationalRetrievalChain object with the FAISS DB as the Retriever (LLM lets us create Retriever objects against data stores)
    5. Invoke the Retriever object with the Query and Chat History
    6. Returns the response
    """
    embeddings = OpenAIEmbeddings()
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Initialize a ConversationalRetrievalChain
    query = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=new_db.as_retriever(),
        return_source_documents=True
    )

    # Invoke the Chain with the Query and History
    return query({"question": question, "chat_history": chat_history})


def show_ui():
    st.title("Yours Truly Human Resources Chatbot")
    st.subheader("Please enter your HR Query")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_history = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("Enter your HR Policy related Query: "):
        # Invoke the function with the Retriever with chat history and display responses in chat container in question-answer pairs
        with st.spinner("Working on your query..."):
            response = query(question=prompt, chat_history=st.session_state.chat_history)
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(response["answer"])
        
        # Append user messages to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
        st.session_state.chat_history.extend([[prompt, response["answer"]]])

# Program Entry
if __name__ == "__main__":
    show_ui()
