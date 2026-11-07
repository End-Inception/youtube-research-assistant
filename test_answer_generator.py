from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vectorstore.faiss_store import FAISSVectorStore
from app.llm.answer_generator import AnswerGenerator


# Step 1: User question
question = "Why is RAG useful when LLMs already have knowledge?"


# Step 2: Load embedding model
embedding_generator = EmbeddingGenerator()


# Step 3: Load saved FAISS database
vector_store = FAISSVectorStore.load("data")


# Step 4: Convert question into embedding
query_embedding = embedding_generator.generate_embeddings(
    [question]
)


# Step 5: Retrieve relevant transcript chunks
retrieved_results = vector_store.search(
    query_embedding,
    top_k=5
)


print("\nRetrieved chunks:", len(retrieved_results))


# Step 6: Initialize Gemini
answer_generator = AnswerGenerator()


# Step 7: Generate answer
result = answer_generator.generate_answer(
    question,
    retrieved_results
)


# Step 8: Display answer
print("\n========== GEMINI ANSWER ==========\n")

print(result["answer"])


# Step 9: Display source references
print("\n========== VIDEO SOURCES ==========\n")

for i, source in enumerate(result["sources"], start=1):

    chunk = source["chunk"]

    video_id = chunk["video_id"]
    start_time = int(chunk["start_time"])

    video_url = (
        f"https://www.youtube.com/watch?v={video_id}"
        f"&t={start_time}s"
    )

    print(f"Source {i}")
    print("Video ID:", video_id)
    print("Timestamp:", start_time)
    print("Video URL:", video_url)
    print()