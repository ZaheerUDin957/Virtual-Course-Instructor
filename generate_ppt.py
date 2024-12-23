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
def generate_ppt():
    st.title("Upload file to create presentation of the topic")
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
            st.markdown("### Presentation for the document")

            Prompt = """
            You are an expert slide generator. Convert the following document into a well-structured presentation slide format. Ensure the following structure:

            1. **Slide Title**: Extract the main topic of the content for the title.
            2. **Headings**: Identify major sections and use them as slide headings.
            3. **Subheadings**: Break down each section into subtopics for clarity.
            4. **Bullet Points**: Summarize key information, ideas, or points under each subheading in concise and clear bullet points.
            5. **Consistency**: Maintain a professional and consistent tone throughout the slides.
            6. **Brevity**: Focus on summarizing only essential points, avoiding lengthy paragraphs.
            Ensure the slides cover a range of topics present in the document, avoiding repetition and maintaining clarity.
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

    

