

---

```markdown
# 📄 RAG Streamlit App

A simple Retrieval-Augmented Generation (RAG) application built using:
- **Streamlit** for the user interface
- **Google Gemini API** for response generation
- **FAISS** for fast similarity search
- **Sentence Transformers** for semantic embeddings

---

## 🚀 Features

- Upload and chat with **PDF**, **DOCX**, or **TXT** files.
- Uses **RAG pipeline** to fetch relevant document chunks before answering.
- Gemini strictly responds based on document context.
- Chat history is preserved and exportable to `.docx`.

---

## 🧠 How It Works

1. **Upload Documents**  
   Upload multiple files (`.pdf`, `.docx`, `.txt`).

2. **Preprocessing**  
   Documents are chunked and encoded using `all-MiniLM-L6-v2`.

3. **Retrieval**  
   FAISS retrieves top relevant chunks for each query.

4. **Answer Generation**  
   Gemini 2.0 Flash answers using only the context provided.

---

## 📂 Project Structure

```

project/
│
├── app.py                   # Main Streamlit app
├── config.py                # Contains Gemini API key
├── loaders.py               # PDF/DOCX/TXT loader utilities
├── processor.py             # Text chunking logic
├── gemini\_chain.py          # Core RAG logic
├── requirements.txt
└── README.md

````

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
````

### 2. Create a virtual environment and activate it

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API Key

Create a file named `config.py`:

```python
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

---

## 📦 Export Chat History

All chat logs are saved in `.docx` format with a clean structure for reference.

---

## 📄 License

This project is licensed under the MIT License.

```

---


```
