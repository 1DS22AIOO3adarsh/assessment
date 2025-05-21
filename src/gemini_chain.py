from sentence_transformers import SentenceTransformer
import faiss
import google.generativeai as genai
from .config import GEMINI_API_KEY
import hashlib

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


def hash_documents(documents):
    """Create a simple hash for a document list to use for caching"""
    text_blob = "".join(doc.page_content for doc in documents)
    return hashlib.md5(text_blob.encode()).hexdigest()


class RAGChat:
    _embedding_cache = {}

    def __init__(self, documents):
        self.docs = documents
        self.texts = [doc.page_content for doc in documents]

        # Check if embeddings for these docs are already cached
        doc_hash = hash_documents(documents)
        if doc_hash in RAGChat._embedding_cache:
            self.embeddings = RAGChat._embedding_cache[doc_hash]
        else:
            self.embeddings = embedding_model.encode(self.texts)
            RAGChat._embedding_cache[doc_hash] = self.embeddings

        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def retrieve(self, query, top_k=3):
        query_emb = embedding_model.encode([query])
        scores, indices = self.index.search(query_emb, top_k)
        return [self.texts[i] for i in indices[0]]

    def __call__(self, query):
        relevant_chunks = self.retrieve(query)
        if not relevant_chunks:
            return "I could not find the answer to your question in the uploaded document."

        context = "\n\n".join(relevant_chunks)

        prompt = f"""
You are a helpful assistant. Answer the question strictly using only the context provided below. 

If the answer is not found in the context, reply:
"I could not find the answer to your question in the uploaded document."

Format your response like this:
- **Answer:** <Your answer here>
- **Supporting Info (if any):**
  - <Bullet point with quote or reference>
  - <Another supporting detail>
- **Page Reference (if available):** Mention the page or section title if known.

---
Context:
{context}
---
Question:
{query}
"""
        response = model.generate_content(prompt)
        return response.text.strip()
