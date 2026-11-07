
from youtube_transcript_api import YouTubeTranscriptApi


def fetch_transcript(video_id: str):

    try:
        api = YouTubeTranscriptApi()

        transcript = api.fetch(
            video_id,
            languages=["en", "hi"]
        )

        segments = transcript.to_raw_data()

        return {
            "video_id": video_id,
            "language": transcript.language_code,
            "segments": segments,
            "text": " ".join(
                segment["text"] for segment in segments
            )
        }

    except Exception as error:

        print(
            f"Transcript unavailable for {video_id}: {error}"
        )

        return None
