import os
import pickle
import faiss
import numpy as np


class FAISSVectorStore:

    def __init__(self, dimension: int = 384):

        self.dimension = dimension

        # Exact similarity search using inner product
        self.index = faiss.IndexFlatIP(dimension)

        # Stores the original transcript chunks
        self.metadata = []

    def add_embeddings(self, embeddings, chunks):
        """
        Store embeddings and their corresponding transcript chunks.
        """

        vectors = np.asarray(
            embeddings,
            dtype=np.float32
        )

        if vectors.ndim != 2:
            raise ValueError("Embeddings must be a 2D array.")

        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Expected {self.dimension} dimensions, "
                f"received {vectors.shape[1]}."
            )

        if len(vectors) != len(chunks):
            raise ValueError(
                "Number of embeddings must match number of chunks."
            )

        if len(vectors) == 0:
            return

        self.index.add(vectors)
        self.metadata.extend(chunks)

    def search(
        self,
        query_embedding,
        top_k=5,
        max_per_video=2
    ):
        if self.index.ntotal == 0:
            return []

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        if max_per_video <= 0:
            raise ValueError("max_per_video must be greater than zero.")

        query_vector = np.asarray(
            query_embedding,
            dtype=np.float32
        ).reshape(1, -1)

        if query_vector.shape[1] != self.dimension:
            raise ValueError("Query embedding has incorrect dimensions.")

        # Search all chunks so that we can select diverse sources.
        scores, indices = self.index.search(
            query_vector,
            self.index.ntotal
        )

        results = []
        video_counts = {}

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            chunk = self.metadata[index]
            video_id = chunk["video_id"]

            # Count how many chunks we have selected from this video.
            count = video_counts.get(video_id, 0)

            if count >= max_per_video:
                continue

            results.append({
                "score": float(score),
                "chunk": chunk
            })

            video_counts[video_id] = count + 1

            if len(results) >= top_k:
                break

        return results

    def save(self, directory="data"):
        """
        Save FAISS index and transcript metadata to disk.
        """

        os.makedirs(directory, exist_ok=True)

        index_path = os.path.join(
            directory,
            "youtube_index.faiss"
        )

        metadata_path = os.path.join(
            directory,
            "youtube_metadata.pkl"
        )

        faiss.write_index(self.index, index_path)

        with open(metadata_path, "wb") as file:
            pickle.dump(self.metadata, file)

        print("FAISS index and metadata saved successfully.")

    @classmethod
    def load(cls, directory="data"):
        """
        Load a previously saved FAISS index and metadata.
        """

        index_path = os.path.join(
            directory,
            "youtube_index.faiss"
        )

        metadata_path = os.path.join(
            directory,
            "youtube_metadata.pkl"
        )

        if not os.path.exists(index_path):
            raise FileNotFoundError("FAISS index not found.")

        if not os.path.exists(metadata_path):
            raise FileNotFoundError("Metadata file not found.")

        instance = cls()

        instance.index = faiss.read_index(index_path)

        with open(metadata_path, "rb") as file:
            instance.metadata = pickle.load(file)

        if instance.index.ntotal != len(instance.metadata):
            raise ValueError("Index and metadata are inconsistent.")

        print("FAISS index and metadata loaded successfully.")

        return instance

