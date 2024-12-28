import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from cvsummarizer import process_docx, process_pdf


def main():
    st.title("CV Summary Generator")

    uploaded_file = st.file_uploader("Select CV", type=["docx", "pdf"])

    text = ""
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]

        st.write("File Details:")
        st.write(f"File Name: {uploaded_file.name}")
        st.write(f"File Type: {file_extension}")

        if file_extension == "docx":
            text = process_docx(uploaded_file.name)
        elif file_extension == "pdf":
            text = process_pdf(uploaded_file.name)
        else:
            st.error("Unsupported file format. Please upload a .docx or .pdf file.")
            return

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
            refine_intermediate_steps=True,
            input_keys="input_documents",
            output_keys="output_text",
        )
        result = chain({"input_documents": text}, return_only_outputs=True)

        st.write("Resume Summary:")
        st.text_area("Text", result['output_text'], height=450)

if __name__ == "__main__":
    main()