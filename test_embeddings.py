
from app.search.youtube_search import search_youtube
from app.transcript.transcript_fetcher import fetch_transcript
from app.processing.cleaner import create_chunks
from app.embeddings.embedding_generator import EmbeddingGenerator


# Step 1: Search YouTube
videos = search_youtube(
    "RAG architecture explained",
    max_results=5
)

print("Videos found:", len(videos))


# Step 2: Extract transcript
transcript = None

for video in videos:

    print("\nTrying:", video["title"])

    transcript = fetch_transcript(video["video_id"])

    if transcript:
        break

if not transcript:
    raise RuntimeError("No accessible transcript found.")


# Step 3: Generate chunks
chunks = create_chunks(transcript)

print("\nTotal chunks:", len(chunks))


# Step 4: Extract chunk text
texts = [
    chunk["text"]
    for chunk in chunks
]


# Step 5: Generate embeddings
generator = EmbeddingGenerator()

embeddings = generator.generate_embeddings(texts)


# Step 6: Verify embeddings
print("\nEmbedding generation successful!")

print("Number of vectors:", embeddings.shape[0])
print("Vector dimensions:", embeddings.shape[1])

print("\nFirst vector preview:")
print(embeddings[0][:10])
