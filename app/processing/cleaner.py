
import re
import html


def clean_text(text: str) -> str:
    """
    Clean individual transcript text.
    """

    text = html.unescape(text)

    # Remove unnecessary HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def create_chunks(
    transcript: dict,
    max_words: int = 250,
    overlap_words: int = 40
):
    """
    Divide transcript into smaller chunks.
    Preserve video ID and timestamps.
    """

    segments = transcript["segments"]

    cleaned_segments = []

    for segment in segments:

        text = clean_text(segment["text"])

        if text:
            cleaned_segments.append({
                "text": text,
                "start": segment["start"],
                "duration": segment["duration"]
            })

    chunks = []
    start_index = 0
    chunk_id = 0

    while start_index < len(cleaned_segments):

        current_words = 0
        end_index = start_index

        while end_index < len(cleaned_segments):

            words = len(
                cleaned_segments[end_index]["text"].split()
            )

            if current_words + words > max_words and end_index > start_index:
                break

            current_words += words
            end_index += 1

            if current_words >= max_words:
                break

        selected = cleaned_segments[start_index:end_index]

        if not selected:
            break

        chunk_text = " ".join(
            segment["text"] for segment in selected
        )

        start_time = selected[0]["start"]

        last_segment = selected[-1]

        end_time = last_segment["start"] + last_segment["duration"]

        chunks.append({
            "chunk_id": chunk_id,
            "video_id": transcript["video_id"],
            "title": transcript.get("title", "Unknown video"),
            "channel": transcript.get("channel", "Unknown channel"),
            "thumbnail": transcript.get("thumbnail"),
            "url": transcript.get("url"),
            "text": chunk_text,
            "start_time": start_time,
            "end_time": end_time
        })

        chunk_id += 1

        if end_index >= len(cleaned_segments):
            break

        # Retain some previous text for context.
        next_start = end_index
        overlap_count = 0

        while next_start > start_index + 1:
            previous_segment = cleaned_segments[next_start - 1]

            overlap_count += len(
                previous_segment["text"].split()
            )

            next_start -= 1

            if overlap_count >= overlap_words:
                break

        start_index = max(start_index + 1, next_start)

    return chunks
