from sentence_transformers import SentenceTransformer
model=SentenceTransformer('all-MiniLM-L6-v2')
sentences = [
    "Machine learning allows computers to learn from data.",
    "Overfitting happens when a model memorizes training data.",
    "Neural networks are made of interconnected neurons.",
    "I really enjoy playing football."
]
embeddings = model.encode(sentences)

for sentence,embedding in zip(sentences,embeddings):
    print(sentence)
    print("vector size:",len(embedding))
    print()