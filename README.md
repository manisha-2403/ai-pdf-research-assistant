# AI PDF Research Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to upload a PDF, ask questions about its contents, and receive grounded answers based only on the information retrieved from the document.

The project demonstrates how modern AI applications combine **PDF processing, text chunking, embeddings, vector search, retrieval, and LLM generation** to build a document question-answering system.

---

## 🚀 Features

* 📄 Upload PDF documents
* 🔍 Extract text from PDF pages
* ✂️ Split documents into smaller chunks
* 🧠 Generate semantic embeddings
* 📚 Store and search document vectors using FAISS
* 🔎 Retrieve the most relevant document chunks
* 🤖 Generate answers using Groq LLM
* 📌 Display source page numbers
* 📊 Show similarity scores
* 🐛 Retrieval Debugger to inspect retrieved chunks
* 🧩 Display the exact context sent to the LLM
* 🌐 Responsive web interface
* ☁️ Designed for cloud deployment

---

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation (RAG) pipeline.

```text
                 PDF Upload
                     │
                     ▼
              PDF Text Extraction
                     │
                     ▼
                Text Chunking
                     │
                     ▼
             Generate Embeddings
                     │
                     ▼
              FAISS Vector Index
                     │
                     │
             User asks a question
                     │
                     ▼
           Generate Query Embedding
                     │
                     ▼
             Similarity Search
                     │
                     ▼
           Retrieve Relevant Chunks
                     │
                     ▼
              Build PDF Context
                     │
                     ▼
                 Groq LLM
                     │
                     ▼
             Grounded Answer
                     │
                     ▼
              Source References
```

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn

### PDF Processing

* PyPDF

### Embeddings

* Sentence Transformers
* `all-MiniLM-L6-v2`

### Vector Search

* FAISS
* Cosine similarity through normalized embeddings

### Large Language Model

* Groq API
* `openai/gpt-oss-120b`

### Frontend

* HTML
* CSS
* JavaScript

### Deployment

* GitHub
* Vercel

---

## 📁 Project Structure

```text
ai-pdf-research-assistant/
│
├── api/
│   └── index.py
│
├── rag/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── generator.py
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

> `.env` is used only for local development and should never be committed to GitHub.

---

# 🔄 RAG Pipeline

## 1. PDF Upload

The user uploads a PDF through the web interface.

FastAPI receives the file and extracts text from each page using PyPDF.

Each page is stored with its page number.

---

## 2. Text Chunking

Large documents are divided into smaller sections called chunks.

Current configuration:

```text
Chunk size: 1000 characters
Chunk overlap: 200 characters
```

The overlap helps preserve context between neighboring chunks.

Each chunk contains:

```text
chunk_id
page
text
```

---

## 3. Embeddings

Each text chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The model produces:

```text
384-dimensional embeddings
```

These embeddings represent the semantic meaning of the text.

---

## 4. Vector Search

FAISS is used to perform similarity search.

The user's question is also converted into an embedding.

The application then searches for the document chunks that are semantically closest to the question.

The current system retrieves up to:

```text
Top 5 chunks
```

---

## 5. Context Construction

The retrieved chunks are combined into a context block.

The context includes the original PDF page number:

```text
[Page 3]

Relevant document text...

[Page 7]

Another relevant section...
```

---

## 6. LLM Generation

The retrieved context is sent to the Groq LLM together with the user's question.

The LLM is instructed to:

* Use only the supplied PDF context
* Avoid outside knowledge
* Avoid inventing information
* Avoid hallucinating
* State when the document does not contain enough information

This helps keep responses grounded in the uploaded document.

---

# 🔎 Retrieval Debugger

One of the main features of this project is the **Retrieval Debugger**.

Instead of only showing the final answer, the application exposes what happened during retrieval.

The debugger displays:

### Retrieved Chunks

```text
Chunk ID
Page
Similarity Score
Retrieved Text
```

### Context Sent to LLM

The exact document context passed to the language model is also displayed.

This makes it possible to investigate questions such as:

```text
Did the retriever find the correct section?

Which page was retrieved?

How similar was the retrieved chunk?

What information was actually given to the LLM?
```

This is useful when evaluating and debugging RAG systems.

---

# 🧪 Example

Suppose a PDF contains information about a company's annual report.

The user asks:

```text
What was the company's revenue in 2025?
```

The application:

```text
Question
   ↓
Question embedding
   ↓
FAISS similarity search
   ↓
Top relevant PDF chunks
   ↓
Relevant context
   ↓
Groq LLM
   ↓
Answer + source pages
```

The final response is grounded in the retrieved document content.

---

# ⚙️ Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-pdf-research-assistant.git
```

Navigate into the project:

```bash
cd ai-pdf-research-assistant
```

---

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never upload this file to GitHub.

---

## 5. Start the FastAPI server

```bash
uvicorn api.index:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

FastAPI API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🔐 Environment Variables

The application requires:

| Variable       | Description                         |
| -------------- | ----------------------------------- |
| `GROQ_API_KEY` | API key used to access the Groq LLM |

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

# 📡 API Endpoints

## Health Check

```http
GET /health
```

Returns:

```json
{
  "status": "healthy"
}
```

---

## Upload PDF

```http
POST /upload
```

Processes the uploaded PDF and builds the vector index.

Example response:

```json
{
  "success": true,
  "filename": "research.pdf",
  "total_pages": 10,
  "pages_with_text": 10,
  "total_chunks": 25,
  "embedding_dimensions": 384
}
```

---

## Search

```http
POST /search
```

Performs semantic similarity search against the uploaded document.

---

## Ask Question

```http
POST /ask
```

Retrieves relevant document chunks and generates a grounded answer using the LLM.

The response includes:

```text
Answer
Sources
Similarity scores
Retrieved chunks
Context sent to LLM
```

---

# 📊 Current Configuration

| Component            | Configuration       |
| -------------------- | ------------------- |
| Chunk size           | 1000 characters     |
| Chunk overlap        | 200 characters      |
| Embedding model      | all-MiniLM-L6-v2    |
| Embedding dimensions | 384                 |
| Vector database      | FAISS               |
| Retrieved chunks     | Top 5               |
| LLM                  | openai/gpt-oss-120b |
| LLM temperature      | 0.1                 |

---

# ⚠️ Limitations

The current version has some limitations:

* Scanned/image-only PDFs may not contain extractable text.
* Very large PDFs may take longer to process.
* The current FAISS implementation stores the vector index in application memory.
* The local development architecture is different from a fully persistent production RAG architecture.
* PDF uploads are processed during the application session.

For production-scale usage, the system can be extended with persistent object storage and a managed/vector database.

---

# 🔮 Future Improvements

Possible future versions could include:

* Persistent vector database
* Multiple PDF support
* User accounts
* Document history
* OCR for scanned PDFs
* Streaming LLM responses
* Conversation memory
* Hybrid keyword + semantic search
* Reranking
* Better citation highlighting
* PDF page preview
* Retrieval evaluation metrics
* Production cloud storage
* Authentication and access control

---

# 🎯 Learning Objectives

This project was built to demonstrate practical understanding of:

* Retrieval-Augmented Generation (RAG)
* Semantic search
* Text embeddings
* Vector databases
* Document processing
* Prompt grounding
* LLM application development
* FastAPI
* REST APIs
* Frontend-backend integration
* AI application debugging
* Cloud deployment

---

# 👩‍💻 Author

**Serena**

BCA Graduate | AI & Generative AI Enthusiast

Interested in:

* Artificial Intelligence
* Generative AI
* RAG Applications
* LLM Applications
* AI Engineering

---

## ⭐ Project Goal

The goal of this project is to demonstrate how a real-world **document-based AI assistant** can be designed using retrieval, embeddings, vector search, and large language models rather than relying only on direct LLM prompting.
