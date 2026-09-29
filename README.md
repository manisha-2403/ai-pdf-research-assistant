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
```
