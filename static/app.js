// ============================================
// ELEMENTS
// ============================================

const dropZone =
    document.getElementById("dropZone");

const pdfInput =
    document.getElementById("pdfInput");

const uploadStatus =
    document.getElementById("uploadStatus");

const questionSection =
    document.getElementById("questionSection");

const questionInput =
    document.getElementById("questionInput");

const askButton =
    document.getElementById("askButton");

const askButtonText =
    document.getElementById("askButtonText");

const askLoader =
    document.getElementById("askLoader");

const answerSection =
    document.getElementById("answerSection");

const answer =
    document.getElementById("answer");

const sources =
    document.getElementById("sources");

const debugSection =
    document.getElementById("debugSection");

const retrievedChunks =
    document.getElementById("retrievedChunks");

const llmContext =
    document.getElementById("llmContext");


// ============================================
// PDF UPLOAD
// ============================================

dropZone.addEventListener(
    "click",
    () => {

        pdfInput.click();

    }
);


pdfInput.addEventListener(
    "change",
    () => {

        if (pdfInput.files.length > 0) {

            uploadPDF(
                pdfInput.files[0]
            );

        }

    }
);


// ============================================
// DRAG & DROP
// ============================================

dropZone.addEventListener(
    "dragover",
    (event) => {

        event.preventDefault();

        dropZone.classList.add(
            "dragover"
        );

    }
);


dropZone.addEventListener(
    "dragleave",
    () => {

        dropZone.classList.remove(
            "dragover"
        );

    }
);


dropZone.addEventListener(
    "drop",
    (event) => {

        event.preventDefault();

        dropZone.classList.remove(
            "dragover"
        );

        const files =
            event.dataTransfer.files;

        if (files.length > 0) {

            uploadPDF(files[0]);

        }

    }
);


// ============================================
// UPLOAD PDF FUNCTION
// ============================================

async function uploadPDF(file) {

    // Check PDF
    if (
        file.type !== "application/pdf" &&
        !file.name.toLowerCase().endsWith(".pdf")
    ) {

        showUploadStatus(
            "Please upload a PDF file.",
            false
        );

        return;
    }


    showUploadStatus(
        "Processing PDF... Please wait.",
        null
    );


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    try {

        const response =
            await fetch(
                "/upload",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "PDF upload failed."
            );

        }


        showUploadStatus(

            `
            <strong>${escapeHTML(
                data.filename
            )}</strong>

            <br>

            ${data.total_pages} pages ·
            ${data.total_chunks} chunks ·
            ${data.embedding_dimensions}D embeddings

            <br>

            ✓ PDF is ready for questions.
            `,

            true

        );


        questionSection.classList.remove(
            "hidden"
        );


        questionInput.focus();


    } catch (error) {

        showUploadStatus(
            error.message,
            false
        );

    }
}


// ============================================
// UPLOAD STATUS
// ============================================

function showUploadStatus(
    message,
    success
) {

    uploadStatus.classList.remove(
        "hidden",
        "upload-success",
        "upload-error"
    );


    uploadStatus.innerHTML =
        message;


    if (success === true) {

        uploadStatus.classList.add(
            "upload-success"
        );

    }


    if (success === false) {

        uploadStatus.classList.add(
            "upload-error"
        );

    }

}


// ============================================
// ASK QUESTION
// ============================================

askButton.addEventListener(
    "click",
    askQuestion
);


questionInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            event.ctrlKey
        ) {

            askQuestion();

        }

    }
);


async function askQuestion() {

    const question =
        questionInput.value.trim();


    if (!question) {

        alert(
            "Please enter a question."
        );

        return;
    }


    // ----------------------------------------
    // Loading state
    // ----------------------------------------

    askButton.disabled = true;

    askButtonText.textContent =
        "Thinking...";

    askLoader.classList.remove(
        "hidden"
    );


    answerSection.classList.add(
        "hidden"
    );

    debugSection.classList.add(
        "hidden"
    );


    try {

        const response =
            await fetch(
                `/ask?query=${encodeURIComponent(
                    question
                )}`,
                {
                    method: "POST",
                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Question answering failed."
            );

        }


        // ------------------------------------
        // Display answer
        // ------------------------------------

        answer.textContent =
            data.answer;


        answerSection.classList.remove(
            "hidden"
        );


        // ------------------------------------
        // Display sources
        // ------------------------------------

        displaySources(
            data.sources || []
        );


        // ------------------------------------
        // Display debugger
        // ------------------------------------

        displayDebugger(
            data.debug
        );


        // Scroll to answer
        answerSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


    } catch (error) {

        alert(
            error.message
        );

    } finally {

        askButton.disabled =
            false;

        askButtonText.textContent =
            "Ask Question";

        askLoader.classList.add(
            "hidden"
        );

    }

}


// ============================================
// DISPLAY SOURCES
// ============================================

function displaySources(
    sourceList
) {

    sources.innerHTML = "";


    if (
        !sourceList ||
        sourceList.length === 0
    ) {

        sources.innerHTML =
            "<span>No sources found.</span>";

        return;
    }


    sourceList.forEach(
        (source) => {

            const sourceElement =
                document.createElement(
                    "div"
                );


            sourceElement.className =
                "source";


            sourceElement.innerHTML = `

                Page ${source.page}

                <span class="source-score">

                    · similarity
                    ${source.similarity_score}

                </span>

            `;


            sources.appendChild(
                sourceElement
            );

        }
    );

}


// ============================================
// DISPLAY RETRIEVAL DEBUGGER
// ============================================

function displayDebugger(
    debug
) {

    if (!debug) {

        return;

    }


    retrievedChunks.innerHTML =
        "";


    const chunks =
        debug.retrieved_chunks || [];


    chunks.forEach(
        (chunk) => {

            const chunkElement =
                document.createElement(
                    "div"
                );


            chunkElement.className =
                "chunk";


            chunkElement.innerHTML = `

                <div class="chunk-header">

                    <span>

                        Chunk ${chunk.chunk_id}
                        · Page ${chunk.page}

                    </span>

                    <span class="score">

                        Similarity:
                        ${chunk.similarity_score}

                    </span>

                </div>


                <div class="chunk-text">

                    ${escapeHTML(
                        chunk.text
                    )}

                </div>

            `;


            retrievedChunks.appendChild(
                chunkElement
            );

        }
    );


    llmContext.textContent =
        debug.context_sent_to_llm ||
        "No context available.";


    debugSection.classList.remove(
        "hidden"
    );

}


// ============================================
// ESCAPE HTML
// ============================================

function escapeHTML(
    text
) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        text;

    return div.innerHTML;

}