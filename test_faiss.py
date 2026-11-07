from app.search.youtube_search import search_youtube
from app.transcript.transcript_fetcher import fetch_transcript
from app.processing.cleaner import create_chunks
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vectorstore.faiss_store import FAISSVectorStore


# Step 1: Search YouTube
videos = search_youtube(
    "RAG architecture explained",
    max_results=5
)

print("Videos found:", len(videos))


# Step 2: Find an accessible transcript
transcript = None

for video in videos:

    print("\nTrying:", video["title"])

    transcript = fetch_transcript(video["video_id"])

    if transcript:
        break

if not transcript:
    raise RuntimeError("No accessible transcript found.")


# Step 3: Create transcript chunks
chunks = create_chunks(transcript)

print("\nTotal chunks:", len(chunks))


# Step 4: Generate embeddings
generator = EmbeddingGenerator()

texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = generator.generate_embeddings(texts)


# Step 5: Store embeddings in FAISS
vector_store = FAISSVectorStore(dimension=384)

vector_store.add_embeddings(
    embeddings,
    chunks
)


# Save the index
vector_store.save("data")

# Load the saved index
vector_store = FAISSVectorStore.load("data")

print("\nVectors stored in FAISS:", vector_store.index.ntotal)


# Step 6: Search using a natural-language question
query = "Why is RAG useful when LLMs already have knowledge?"

query_embedding = generator.generate_embeddings([query])

results = vector_store.search(
    query_embedding,
    top_k=5
)


# Step 7: Display retrieved results
print("\n========== RETRIEVED RESULTS ==========")

for i, result in enumerate(results, start=1):

    chunk = result["chunk"]

    print(f"\nResult {i}")
    print("Similarity score:", round(result["score"], 4))
    print("Video ID:", chunk["video_id"])
    print("Start time:", chunk["start_time"])
    print("End time:", chunk["end_time"])
    print("Text:", chunk["text"][:500])