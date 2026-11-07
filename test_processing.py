
from app.search.youtube_search import search_youtube
from app.transcript.transcript_fetcher import fetch_transcript
from app.processing.cleaner import create_chunks


videos = search_youtube(
    "RAG architecture explained",
    max_results=5
)

print("Found videos:", len(videos))

for video in videos:

    print("\nTrying:", video["title"])

    transcript = fetch_transcript(video["video_id"])

    if transcript:

        chunks = create_chunks(transcript)

        print("\nTranscript language:", transcript["language"])
        print("Total chunks:", len(chunks))

        for chunk in chunks[:3]:

            print("\nChunk ID:", chunk["chunk_id"])
            print("Start:", chunk["start_time"])
            print("End:", chunk["end_time"])
            print("Text:", chunk["text"][:300])

        break

else:
    print("No accessible transcripts found.")
