
from app.orchestration.research_pipeline import ResearchPipeline


pipeline = ResearchPipeline()

result = pipeline.research(
    question="Why is RAG useful when LLMs already have knowledge?",
    max_videos=3,
    top_k=5
)

print("\n========== RESEARCH RESULT ==========")

print("\nQuestion:")
print(result["question"])

print("\nAnswer:")
print(result["answer"])

print("\nVideos found:", result["videos_found"])
print("Chunks created:", result["chunks_created"])

# New: Transcript processing statistics
print("Videos successfully processed:", result["videos_processed"])
print("Videos skipped:", result["videos_skipped"])

if result.get("skipped_video_ids"):
    print("Skipped video IDs:", result["skipped_video_ids"])

print("\nSources:")

for i, source in enumerate(result["sources"], start=1):

    chunk = source["chunk"]

    timestamp = int(chunk["start_time"])

    video_url = (
        f"https://www.youtube.com/watch?v="
        f"{chunk['video_id']}&t={timestamp}s"
    )

    print(f"\nSource {i}")
    print("Video:", video_url)
    print("Similarity:", round(source["score"], 4))
