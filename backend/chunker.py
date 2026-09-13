import re


def create_sentence_chunks(
    pages,
    chunk_size=500,
    overlap=100
):
    chunks = []

    for page in pages:

        text = page["text"]
        page_number = page["page"]

        # Split text into sentences
        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        current_chunk = ""

        for sentence in sentences:

            # Check whether adding this sentence
            # would exceed our target size
            if (
                len(current_chunk) + len(sentence) + 1
                <= chunk_size
            ):
                current_chunk += sentence + " "

            else:
                # Store the current chunk
                if current_chunk.strip():
                    chunks.append({
                        "text": current_chunk.strip(),
                        "page": page_number
                    })

                # Start a new chunk
                current_chunk = sentence + " "

        # Store remaining text
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "page": page_number
            })

    return chunks

if __name__ == "__main__":

    pages = [
        {
            "page": 1,
            "text": """
            Machine learning allows computers to learn patterns from data.
            These patterns can be used to make predictions.
            Overfitting occurs when a model learns the training data too closely.
            This causes poor performance on unseen data.
            """
        }
    ]

    chunks = create_sentence_chunks(
        pages,
        chunk_size=150
    )

    for i, chunk in enumerate(chunks):

        print(f"\n--- Chunk {i + 1} ---")
        print("Page:", chunk["page"])
        print("Text:", chunk["text"])