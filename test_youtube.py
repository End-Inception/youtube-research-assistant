
from app.search.youtube_search import search_youtube
from app.transcript.transcript_fetcher import fetch_transcript


if __name__ == "__main__":

    # Step 1: Search YouTube
    videos = search_youtube(
        "RAG architecture explained",
        max_results=5
    )

    print(f"Found {len(videos)} videos")

    # Step 2: Fetch transcript of first video
    if videos:

        video = videos[0]

        print("\nSelected video:", video["title"])

        result = fetch_transcript(video["video_id"])

        if result:

            print("\nTranscript language:", result["language"])
            print("\nTranscript preview:")
            print(result["text"][:1000])

        else:
            print("Could not retrieve transcript.")
