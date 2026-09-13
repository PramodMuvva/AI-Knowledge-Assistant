import chromadb

from backend.document_loader import extract_pages_from_pdf
from backend.chunker import create_sentence_chunks

def ingest_document(file_path, source_name):

    client = chromadb.PersistentClient(
        path="data/chroma_db"
    )

    collection = client.get_or_create_collection(
        name="knowledge_base"
    )

    pages = extract_pages_from_pdf(file_path)

    chunks = create_sentence_chunks(
        pages,
        chunk_size=500,
        overlap=100
    )

    ids = [
        f"{source_name}_chunk_{i}"
        for i in range(len(chunks))
    ]

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "source": source_name,
            "page": chunk["page"]
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    return {
        "pages": len(pages),
        "chunks": len(chunks)
    }
    
if __name__ == "__main__":

    result = ingest_document(
        "data/documents/machine_learning.pdf",
        "machine_learning.pdf"
    )

    print("Ingestion complete!")
    print("Pages:", result["pages"])
    print("Chunks:", result["chunks"])