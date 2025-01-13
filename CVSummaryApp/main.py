import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from cvsummarizer import process_docx, process_pdf
import os

def main():
    st.title("CV Summary Generator")

    uploaded_file = st.file_uploader("Select CV", type=["docx", "pdf"])

    text = ""
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]

        st.write("File Details:")
        st.write(f"File Name: {uploaded_file.name}")
        st.write(f"File Type: {file_extension}")

        # Save uploaded file temporarily
        temp_file_path = f"temp_uploaded_file.{file_extension}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            if file_extension == "docx":
                text = process_docx(temp_file_path)
            elif file_extension == "pdf":
                text = process_pdf(temp_file_path)
            else:
                st.error("Unsupported file format. Please upload a .docx or .pdf file.")
                return

            st.success("File processed successfully!")
            st.write(f"Extracted Text: {text[:100]}...")  # Show the first 500 characters of the text

        except Exception as e:
            st.error(f"An error occurred: {e}")

        finally:
            #cleanup temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        llm = OpenAI(temperature=0)
        prompt_template = """You have been given a Resume to analyze.
        Write a verbose detail of the following:
        {text}
        Details:
        """
        prompt = PromptTemplate.from_template(prompt_template)

        refine_template = (
            "Your job is to produce a final outcome\n"
            "We have provided an existing detail: {existing_answer}\n"
            "We want a refined version of the existing detail based on initial details below\n"
            "---------------------\n"
            "{text}\n"
            "---------------------\n"
            "Given the new context, refine the original summary in the following manner:\n"
            "Name: \n"
            "Email: \n"
            "Key Skills: \n"
            "Last Company: \n"
            "Experience Summary: \n"
        )
        refine_prompt = PromptTemplate.from_template(refine_template)
        chain = load_summarize_chain(
            llm=llm,
            chain_type="refine",
            question_prompt=prompt,
            refine_prompt=refine_prompt,
            verbose=True
        )
        result = chain({"input_documents": text}, return_only_outputs=True)

        st.write("Resume Summary:")
        st.text_area("Text", result['output_text'], height=450)


if __name__ == "__main__":
    main()
