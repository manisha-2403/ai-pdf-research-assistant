from typing import List, Dict


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def split_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[str]:
    """
    Split text into overlapping chunks.
    """

    if not text:
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be smaller than chunk size."
        )

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


def create_chunks(pages: List[Dict]) -> List[Dict]:
    """
    Convert page-level PDF text into chunks
    while preserving page metadata.
    """

    all_chunks = []

    chunk_id = 1

    for page_data in pages:

        page_number = page_data["page"]
        text = page_data["text"]

        if not text:
            continue

        page_chunks = split_text(text)

        for chunk in page_chunks:

            all_chunks.append({
                "chunk_id": chunk_id,
                "page": page_number,
                "text": chunk
            })

            chunk_id += 1

    return all_chunks