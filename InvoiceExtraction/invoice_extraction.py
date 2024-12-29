import streamlit as st
import invoiceutil as iu

def main():

    st.set_page_config(page_title="Invoice Extraction Bot")
    st.title("Invoice Extraction Bot 🧾")
    st.subheader("I can help you in extracting invoice data")

    # Upload the Invoices (PDF files)
    pdf = st.file_uploader(
        "Upload invoices here, only PDF files allowed", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    submit = st.button("Extract Data")

    if submit:
        with st.spinner("Wait for it..."):
            df = iu.create_docs(pdf)
            st.write(df.head())

            data_as_csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download data as CSV",
                data_as_csv,
                "benchmark-tools.csv",
                "text/csv",
                key="download-tools-csv",
            )
        st.success("Hopefully I am able to save the time")

if __name__ == "__main__":
    main()
