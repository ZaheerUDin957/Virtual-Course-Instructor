import streamlit as st
from langchain_community.document_loaders import (
    TextLoader, PyMuPDFLoader, UnstructuredMarkdownLoader, Docx2txtLoader
)
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain_community.llms import OpenAI
import os
import base64
from fpdf import FPDF
# Function to load a .txt file
def load_as_textfile(file_path):
    loader = TextLoader(file_path)
    documents = loader.load()
    return documents

# Function to load a .markdown file
def load_as_markdown(file_path):
    loader = UnstructuredMarkdownLoader(file_path)
    documents = loader.load()
    return documents

# Function to load a .docx file
def load_as_docx(file_path):
    loader = Docx2txtLoader(file_path)
    documents = loader.load()
    return documents

# Function to load a .pdf file
def load_as_pdf(file_path):
    loader = PyMuPDFLoader(file_path, extract_images=True)
    documents = loader.load()
    return documents

# Streamlit application
def generate_paper():
    st.title("Upload file to generate Paper")
    st.markdown("Upload a single file (.txt, .docx, .pdf, .markdown) to process and view its content.")

    # File uploader (single file)
    uploaded_file = st.file_uploader(
        "Upload your file",
        type=["txt", "docx", "pdf", "md"]  # Added "md" for Markdown files
    )
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    if uploaded_file and api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        # Extract file name
        file_name = uploaded_file.name
        st.markdown(f"### File: {file_name}")

        # Save uploaded file to a temporary location
        temp_file_path = os.path.join("temp", file_name)
        os.makedirs("temp", exist_ok=True)  # Ensure temp directory exists
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Process the file based on its extension
        file_extension = file_name.split(".")[-1].lower()
        documents = None
        if file_extension == "txt":
            documents = load_as_textfile(temp_file_path)
        elif file_extension == "md":
            documents = load_as_markdown(temp_file_path)
        elif file_extension == "docx":
            documents = load_as_docx(temp_file_path)
        elif file_extension == "pdf":
            documents = load_as_pdf(temp_file_path)
        else:
            st.error(f"Unsupported file type: {file_extension}")

        # Display document content
        if documents:
            document = documents[0]  # Display the first document
            # st.markdown("#### Metadata")
            # st.json(document.metadata)
            # st.markdown("#### Page Content")
            # st.write(document.page_content)

            # QA chain integration
            st.markdown("---")
            st.markdown("### Generated Paper")

            Prompt = """
            You are an expert exam paper generator. Create a structured question paper from the following document. The paper should include:

            1. **Title**: A relevant title for the question paper.
            2. **Instructions**: Clear instructions for the students on how to attempt the paper.
            3. **Question Sections**: Include three sections as follows:
                - **Section A (Multiple Choice Questions)**: 
                    - Create 10 diverse and meaningful MCQs.
                    - Each question should have 4 options with only one correct answer.
                - **Section B (Short Questions)**:
                    - Create 5-10 short questions that test comprehension and key concepts.
                    - Questions should require brief, precise answers.
                - **Section C (Long Questions)**:
                    - Create 2-5 long questions that require detailed responses.
                    - Encourage critical thinking, analysis, and elaboration on key themes.
            Ensure the questions cover a range of topics in the document, avoiding repetition and ensuring clarity.
            """


            if Prompt:
                # Define a QA chain
                llm = OpenAI(temperature=0.0)  # Use OpenAI API (requires API key)
                qa_chain = load_qa_chain(llm=llm, chain_type="stuff")

                # Generate the QA response
                response = qa_chain.run(
                    input_documents=[document],
                    question=Prompt  # Pass the user's question with the correct key
                )

                st.write(response)
        else:
            st.error("No content found in the document.")

    


