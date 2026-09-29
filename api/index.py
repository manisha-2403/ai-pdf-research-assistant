from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pypdf import PdfReader

import io

from rag.text_splitter import create_chunks
from rag.embeddings import EmbeddingModel
from rag.retriever import VectorRetriever
from rag.generator import LLMGenerator


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI PDF Research Assistant",
    description="A RAG-based PDF question answering application",
    version="1.0.0"
)


# ============================================================
# STATIC FRONTEND
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ============================================================
# INITIALIZE AI COMPONENTS
# ============================================================

# Embedding model
embedding_model = EmbeddingModel()

# FAISS vector retriever
retriever = VectorRetriever()

# Groq LLM
llm_generator = LLMGenerator()


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/")
def home():

    return FileResponse(
        "static/index.html"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# UPLOAD PDF
# ============================================================

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    try:

        # ----------------------------------------------------
        # Read uploaded PDF
        # ----------------------------------------------------

        file_bytes = await file.read()

        pdf_file = io.BytesIO(
            file_bytes
        )

        reader = PdfReader(
            pdf_file
        )

        # ----------------------------------------------------
        # Extract text page by page
        # ----------------------------------------------------

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            text = page.extract_text() or ""

            pages.append({
                "page": page_number,
                "text": text.strip()
            })

        # ----------------------------------------------------
        # Create chunks
        # ----------------------------------------------------

        chunks = create_chunks(
            pages
        )

        # Check whether usable text exists
        if not chunks:

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text was found "
                    "in the PDF."
                )
            )

        # ----------------------------------------------------
        # Generate embeddings
        # ----------------------------------------------------

        embeddings = (
            embedding_model.embed_chunks(
                chunks
            )
        )

        # ----------------------------------------------------
        # Build FAISS vector index
        # ----------------------------------------------------

        retriever.build_index(
            embeddings,
            chunks
        )

        # ----------------------------------------------------
        # Calculate document statistics
        # ----------------------------------------------------

        total_pages = len(
            pages
        )

        pages_with_text = sum(
            1
            for page in pages
            if page["text"]
        )

        total_characters = sum(
            len(page["text"])
            for page in pages
        )

        total_chunks = len(
            chunks
        )

        embedding_dimensions = (
            int(embeddings.shape[1])
            if embeddings.size > 0
            else 0
        )

        # ----------------------------------------------------
        # Return upload result
        # ----------------------------------------------------

        return {

            "success": True,

            "filename": file.filename,

            "total_pages": total_pages,

            "pages_with_text": (
                pages_with_text
            ),

            "total_characters": (
                total_characters
            ),

            "total_chunks": (
                total_chunks
            ),

            "embedding_dimensions": (
                embedding_dimensions
            ),

            "message": (
                "PDF processed successfully. "
                "FAISS vector index is ready."
            )
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to process PDF: {str(e)}"
            )
        )


# ============================================================
# SEARCH PDF
# ============================================================

@app.post("/search")
async def search_pdf(
    query: str
):

    try:

        # ----------------------------------------------------
        # Convert question to embedding
        # ----------------------------------------------------

        query_embedding = (
            embedding_model.generate_embeddings(
                [query]
            )
        )

        # ----------------------------------------------------
        # Search FAISS
        # ----------------------------------------------------

        results = retriever.search(
            query_embedding,
            top_k=5
        )

        # ----------------------------------------------------
        # Return search results
        # ----------------------------------------------------

        return {

            "success": True,

            "query": query,

            "results": results

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Search failed: {str(e)}"
            )
        )


# ============================================================
# ASK QUESTION — COMPLETE RAG PIPELINE
# ============================================================

@app.post("/ask")
async def ask_question(
    query: str
):

    try:

        # ----------------------------------------------------
        # Validate question
        # ----------------------------------------------------

        if not query.strip():

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        # ----------------------------------------------------
        # STEP 1
        # Question → Embedding
        # ----------------------------------------------------

        query_embedding = (
            embedding_model.generate_embeddings(
                [query]
            )
        )

        # ----------------------------------------------------
        # STEP 2
        # Retrieve relevant PDF chunks
        # ----------------------------------------------------

        results = retriever.search(
            query_embedding,
            top_k=5
        )

        # ----------------------------------------------------
        # STEP 3
        # No results
        # ----------------------------------------------------

        if not results:

            no_answer = (
                "I couldn't find enough information "
                "in the uploaded document to answer "
                "this question."
            )

            return {

                "success": True,

                "question": query,

                "answer": no_answer,

                "sources": [],

                "debug": {

                    "retrieved_chunks": [],

                    "context_sent_to_llm": ""

                }

            }

        # ----------------------------------------------------
        # STEP 4
        # Build context for LLM
        # ----------------------------------------------------

        context_parts = []

        for result in results:

            context_parts.append(

                f"[Page {result['page']}]\n"
                f"{result['text']}"

            )

        context = "\n\n".join(
            context_parts
        )

        # ----------------------------------------------------
        # STEP 5
        # Send context + question to Groq
        # ----------------------------------------------------

        answer = (
            llm_generator.generate_answer(
                question=query,
                context=context
            )
        )

        # ----------------------------------------------------
        # STEP 6
        # Create source information
        # ----------------------------------------------------

        sources = []

        for result in results:

            sources.append({

                "page": result["page"],

                "similarity_score": round(
                    result["similarity_score"],
                    4
                )

            })

        # ----------------------------------------------------
        # STEP 7
        # Create Retrieval Debugger information
        # ----------------------------------------------------

        retrieved_chunks = []

        for result in results:

            retrieved_chunks.append({

                "chunk_id": (
                    result["chunk_id"]
                ),

                "page": (
                    result["page"]
                ),

                "similarity_score": round(
                    result["similarity_score"],
                    4
                ),

                "text": (
                    result["text"]
                )

            })

        # ----------------------------------------------------
        # STEP 8
        # Return complete RAG response
        # ----------------------------------------------------

        return {

            "success": True,

            "question": query,

            "answer": answer,

            "sources": sources,

            "debug": {

                "retrieved_chunks": (
                    retrieved_chunks
                ),

                "context_sent_to_llm": (
                    context
                )

            }

        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Question answering failed: "
                f"{str(e)}"
            )
        )