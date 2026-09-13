from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from backend.document_loader import extract_text_from_pdf
from backend.chunker import create_chunks


# 1. Load the PDF
pdf_path = "data/documents/machine_learning.pdf"

text = extract_text_from_pdf(pdf_path)

print("Extracted characters:", len(text))


# 2. Split the PDF text into chunks
chunks = create_chunks(
    text,
    chunk_size=500,
    overlap=100
)

print("Number of chunks:", len(chunks))


# 3. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# 4. Convert every chunk into an embedding
chunk_embeddings = model.encode(chunks)

print("Embeddings created.")


# 5. User's question
query = "What is machine learning?"


# 6. Convert question into an embedding
query_embedding = model.encode([query])


# 7. Compare question with every chunk
similarities = cosine_similarity(
    query_embedding,
    chunk_embeddings
)[0]


# 8. Rank chunks by similarity
ranked_indexes = similarities.argsort()[::-1]


# 9. Retrieve top 3 chunks
top_k = 3

print("\nTOP RELEVANT CHUNKS:\n")

for index in ranked_indexes[:top_k]:

    print(f"Score: {similarities[index]:.4f}")

    print(chunks[index])

    print("\n" + "-" * 80)