
from googleapiclient.discovery import build
from app.config import YOUTUBE_API_KEY


def search_youtube(query: str, max_results: int = 5):

    youtube = build(
        "youtube",
        "v3",
        developerKey=YOUTUBE_API_KEY
    )

    response = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results,
        order="relevance"
    ).execute()

    videos = []

    for item in response.get("items", []):

        video_id = item["id"]["videoId"]
        snippet = item["snippet"]

        videos.append({
            "video_id": video_id,
            "title": snippet["title"],
            "description": snippet["description"],
            "channel": snippet["channelTitle"],
            "published_at": snippet["publishedAt"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "url": f"https://www.youtube.com/watch?v={video_id}"
        })

    return videos


if __name__ == "__main__":

    results = search_youtube(
        "Model Context Protocol architecture",
        max_results=5
    )

    for video in results:
        print("\nTitle:", video["title"])
        print("Channel:", video["channel"])
        print("URL:", video["url"])
