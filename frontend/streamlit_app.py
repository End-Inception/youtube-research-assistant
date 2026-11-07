
import streamlit as st
import requests


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="YouTube AI Research Assistant",
    page_icon="🎥",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/research"


# -------------------------------
# Helper Function
# -------------------------------

def format_timestamp(seconds):

    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

    return f"{minutes:02d}:{remaining_seconds:02d}"


# -------------------------------
# Application UI
# -------------------------------

st.title("🎥 YouTube AI Research Assistant")

st.write(
    "Research any topic using YouTube videos, "
    "transcripts, semantic search, and AI."
)

st.divider()


# -------------------------------
# User Input
# -------------------------------

question = st.text_area(
    "Enter your research question",
    placeholder="Example: Why is RAG useful when LLMs already have knowledge?",
    height=120
)

max_videos = st.slider(
    "Number of YouTube videos to analyze",
    min_value=1,
    max_value=10,
    value=5
)

top_k = st.slider(
    "Number of relevant sources to retrieve",
    min_value=1,
    max_value=20,
    value=5
)

# -------------------------------
# Research Execution
# -------------------------------

if st.button("🔍 Start Research", type="primary"):

    if not question.strip():

        st.warning("Please enter a research question.")

    else:

        payload = {
            "question": question,
            "max_videos": max_videos,
            "top_k": top_k
        }

        try:

            with st.spinner(
                "Researching YouTube videos and generating your answer..."
            ):

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=600
                )

                response.raise_for_status()

                result = response.json()


            # -------------------------------
            # Research Answer
            # -------------------------------

            st.success("Research completed successfully!")

            st.header("🧠 AI Research Answer")

            st.markdown(result["answer"])


            # -------------------------------
            # Research Statistics
            # -------------------------------

            st.divider()

            st.header("📊 Research Statistics")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Videos Found",
                result.get("videos_found", 0)
            )

            col2.metric(
                "Videos Processed",
                result.get("videos_processed", 0)
            )

            col3.metric(
                "Videos Skipped",
                result.get("videos_skipped", 0)
            )

            col4.metric(
                "Chunks Created",
                result.get("chunks_created", 0)
            )


            # -------------------------------
            # Sources
            # -------------------------------

            st.divider()

            st.header("📚 Research Sources")

            sources = result.get("sources", [])

            if sources:

                for index, source in enumerate(sources, start=1):

                    chunk = source["chunk"]

                    video_id = chunk["video_id"]

                    start_time = chunk["start_time"]

                    timestamp = format_timestamp(start_time)

                    video_url = (
                        f"https://www.youtube.com/watch?v={video_id}"
                        f"&t={int(start_time)}s"
                    )

                    with st.expander(
                        f"Source {index}: {chunk.get('title', 'Unknown video')}"
                    ):

                        # Video thumbnail
                        thumbnail = chunk.get("thumbnail")

                        if thumbnail:
                            st.image(thumbnail, width=320)

                        # Video information
                        st.write("**Video Title:**", chunk.get("title", "Unknown video"))

                        st.write("**Channel:**", chunk.get("channel", "Unknown channel"))

                        st.write("**Video ID:**", video_id)

                        # Similarity score
                        st.write(
                            "**Similarity Score:**",
                            round(source["score"], 4)
                        )

                        # Timestamp
                        st.write("**Timestamp:**", timestamp)

                        # YouTube link
                        st.markdown(
                            f"[▶ Watch this part of the video]({video_url})"
                        )

                        # Transcript
                        st.write("**Relevant Transcript:**")

                        st.write(chunk["text"])

            else:

                st.info("No relevant sources were retrieved.")


        except requests.exceptions.Timeout:

            st.error(
                "The research request timed out. "
                "Please try again."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to FastAPI. "
                "Please check whether the backend server is running."
            )

        except requests.exceptions.HTTPError as error:

            st.error(f"API error: {error}")

            if error.response is not None:
                st.write(error.response.text)

        except Exception as error:

            st.error(f"Something went wrong: {error}")
