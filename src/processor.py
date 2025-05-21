from typing import List
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

def split_documents(docs: List[Document], chunk_size=1000, chunk_overlap=100) -> List[Document]:
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_documents([doc]))
    return chunks
