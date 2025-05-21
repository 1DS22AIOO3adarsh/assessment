import os

# Folder structure to create inside 'Task4/'
folders = [
    "src"
]

# Files and their initial content
files = {
    ".env": "OPENAI_API_KEY=your_api_key_here\n",
    "README.md": "# RAG Streamlit App\n\nAn interactive app to chat with uploaded documents using RAG.\n",
    "requirements.txt": "\n".join([
        "streamlit",
        "langchain",
        "openai",
        "pypdf",
        "python-docx",
        "faiss-cpu",
        "tiktoken",
        "python-dotenv"
    ]),
    "main.py": "from src.ui import render_app\n\nif __name__ == \"__main__\":\n    render_app()\n",
    "src/__init__.py": "",
    "src/config.py": "from dotenv import load_dotenv\nimport os\n\nload_dotenv()\n\nOPENAI_API_KEY = os.getenv(\"OPENAI_API_KEY\")\n",
    "src/loaders.py": '''import tempfile
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

def load_document(uploaded_file):
    suffix = uploaded_file.name.split('.')[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    if suffix == 'pdf':
        return PyPDFLoader(tmp_path).load()
    elif suffix == 'docx':
        return Docx2txtLoader(tmp_path).load()
    elif suffix == 'txt':
        return TextLoader(tmp_path).load()
    else:
        return []
''',
    "src/processor.py": '''from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)
''',
    "src/rag_chain.py": '''from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from .config import OPENAI_API_KEY

def build_qa_chain(chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    retriever = vectorstore.as_retriever()

    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa
''',
    "src/ui.py": '''import streamlit as st
from .loaders import load_document
from .processor import split_documents
from .rag_chain import build_qa_chain

def render_app():
    st.set_page_config(page_title="RAG Streamlit App", layout="wide")
    st.title("Chat with Your Documents")

    files = st.file_uploader("Upload PDF, DOCX, or TXT", accept_multiple_files=True)
    if not files:
        st.info("Please upload at least one document to get started.")
        return

    docs = []
    for f in files:
        docs.extend(load_document(f))

    with st.spinner("Processing documents..."):
        chunks = split_documents(docs)
        qa_chain = build_qa_chain(chunks)
        st.success("Documents processed!")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    query = st.text_input("Ask a question:")
    if query:
        result = qa_chain(query)
        st.session_state.messages.append(("You", query))
        st.session_state.messages.append(("Bot", result["result"]))

    for sender, message in st.session_state.messages:
        st.markdown(f"**{sender}:** {message}")
'''
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file_path, content in files.items():
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Folder structure and files created successfully.")
