from app.search.youtube_search import search_youtube
from app.transcript.transcript_fetcher import fetch_transcript
from app.processing.cleaner import create_chunks
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vectorstore.faiss_store import FAISSVectorStore
from app.llm.answer_generator import AnswerGenerator


class ResearchPipeline:

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.answer_generator = AnswerGenerator()

    def research(
        self,
        question: str,
        max_videos: int = 5,
        top_k: int = 5
    ):

        if not question.strip():
            raise ValueError("Research question cannot be empty.")

        # Step 1: Search YouTube
        videos = search_youtube(
            query=question,
            max_results=max_videos
        )

        if not videos:
            return {
                "question": question,
                "answer": "No YouTube videos were found.",
                "sources": [],
                "videos_found": 0,
                "videos_processed": 0,
                "videos_skipped": 0,
                "chunks_created": 0
            }

        all_chunks = []
        videos_processed = 0
        skipped_video_ids = []

        # Step 2: Fetch transcripts and create chunks
        for video in videos:

            video_id = video["video_id"]

            try:
                transcript = fetch_transcript(video_id)

                if transcript is None:
                    skipped_video_ids.append(video_id)
                    continue

                # Attach YouTube video metadata to the transcript
                transcript["title"] = video["title"]
                transcript["channel"] = video["channel"]
                transcript["thumbnail"] = video["thumbnail"]
                transcript["url"] = video["url"]

                chunks = create_chunks(transcript)

                if not chunks:
                    skipped_video_ids.append(video_id)
                    continue

                all_chunks.extend(chunks)
                videos_processed += 1

            except Exception as error:
                print(
                    f"Skipping video {video_id} due to error: {error}"
                )
                skipped_video_ids.append(video_id)
                continue

        # Step 3: Check whether any usable transcripts were found
        if not all_chunks:
            return {
                "question": question,
                "answer": (
                    "No accessible transcripts were found "
                    "for the retrieved videos."
                ),
                "sources": [],
                "videos_found": len(videos),
                "videos_processed": 0,
                "videos_skipped": len(skipped_video_ids),
                "skipped_video_ids": skipped_video_ids,
                "chunks_created": 0
            }

        # Step 4: Generate embeddings
        texts = [
            chunk["text"] for chunk in all_chunks
        ]

        embeddings = self.embedding_generator.generate_embeddings(
            texts
        )

        # Step 5: Create a FAISS store
        vector_store = FAISSVectorStore()

        vector_store.add_embeddings(
            embeddings,
            all_chunks
        )

        # Step 6: Embed the user's question
        query_embedding = self.embedding_generator.generate_embeddings(
            [question]
        )[0]

        # Step 7: Retrieve relevant chunks with source diversity
        retrieved_results = vector_store.search(
            query_embedding,
            top_k=top_k,
            max_per_video=2
        )

        # Step 8: Generate the final answer
        result = self.answer_generator.generate_answer(
            question,
            retrieved_results
        )

        return {
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"],
            "videos_found": len(videos),
            "videos_processed": videos_processed,
            "videos_skipped": len(skipped_video_ids),
            "skipped_video_ids": skipped_video_ids,
            "chunks_created": len(all_chunks)
        }