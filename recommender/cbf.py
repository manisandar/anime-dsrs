"""
Pure Content-Based Filtering (CBF) Recommender Engine.
CSX/ITX 4207: Decision Support and Recommendation System, Assumption University.

Core Method:
CountVectorizer + Cosine Similarity + User-Selected/Rated Reference Anime

Mathematical Formulation:
sim(A, B) = (A • B) / (||A|| * ||B||)

Strict Constraints:
- Pure CountVectorizer genre representation
- Exact Cosine Similarity ranking
- Reference item comparison (User-selected or rated anime)
- Self-exclusion (Reference anime excluded from recommendations)
- NO SVD, NO Collaborative Filtering, NO TF-IDF
- NO Centered Taste Weighting (Rating - 3.0)
- NO Synthetic users, NO Anchor anime
"""

import json
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_genres(genres_input: Any) -> str:
    """
    Cleans and normalizes anime genres:
    - Strips whitespace, converts to lowercase.
    - Handles list of strings, comma-separated strings, or empty/missing data safely.
    - Preserves multi-word genres (e.g. 'martial arts' -> 'martial arts').
    """
    if not genres_input:
        return ""
    if isinstance(genres_input, list):
        clean_list = [str(g).strip().lower() for g in genres_input if str(g).strip()]
        return ", ".join(clean_list)
    elif isinstance(genres_input, str):
        clean_list = [g.strip().lower() for g in genres_input.split(",") if g.strip()]
        return ", ".join(clean_list)
    return ""


class ContentBasedRecommender:
    """
    Pure Content-Based Filtering Recommender using CountVectorizer and Cosine Similarity.
    """

    def __init__(self, catalog_or_path: Any):
        """
        Initializes the recommender with either a file path to anime_catalog.json
        or an in-memory list of anime dictionaries.
        """
        if isinstance(catalog_or_path, str):
            with open(catalog_or_path, "r", encoding="utf-8") as f:
                self.catalog: List[Dict[str, Any]] = json.load(f)
        elif isinstance(catalog_or_path, list):
            self.catalog = catalog_or_path
        else:
            raise ValueError("catalog_or_path must be a file path string or a list of anime records.")

        # Map by anime_id and index in catalog
        self.catalog_map: Dict[int, Dict[str, Any]] = {}
        self.id_to_index: Dict[int, int] = {}
        for idx, item in enumerate(self.catalog):
            anime_id = int(item["anime_id"])
            self.catalog_map[anime_id] = item
            self.id_to_index[anime_id] = idx

        # Step 1: Clean and normalize genre data for all anime
        self.genre_corpus = [normalize_genres(item.get("genres")) for item in self.catalog]

        # Step 2: Fit CountVectorizer to extract exact genre vocabulary
        self.vectorizer = CountVectorizer(
            tokenizer=lambda text: [g.strip().lower() for g in text.split(",") if g.strip()],
            token_pattern=None,
            binary=True
        )

        # Step 3: Convert each anime's genres into a genre count matrix
        self.genre_matrix = self.vectorizer.fit_transform(self.genre_corpus)
        self.vocabulary = self.vectorizer.get_feature_names_out().tolist()

    def get_reference_anime(self, anime_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves an anime record by its ID."""
        return self.catalog_map.get(int(anime_id))

    def recommend(
        self,
        reference_anime_id: int,
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Computes Top-N Content-Based recommendations for a given reference anime.

        Algorithm:
        1. Locate reference anime index.
        2. Extract reference anime's CountVectorizer genre vector.
        3. Compute Cosine Similarity against all other anime in the catalog.
        4. Exclude the reference anime itself.
        5. Sort by cosine similarity in descending order.
        6. Return the Top-N most similar anime with title, genres, similarity score, and metadata.
        """
        ref_id = int(reference_anime_id)
        if ref_id not in self.id_to_index:
            return []

        ref_idx = self.id_to_index[ref_id]
        ref_vector = self.genre_matrix[ref_idx]

        # Step 4: Calculate Cosine Similarity across all anime
        similarity_scores = cosine_similarity(ref_vector, self.genre_matrix).flatten()

        # Step 5 & 6: Exclude reference anime itself and sort descending
        scored_pairs = []
        for idx, sim in enumerate(similarity_scores):
            if idx == ref_idx:
                continue  # Exclude reference anime
            scored_pairs.append((idx, float(sim)))

        # Sort descending by cosine similarity score
        scored_pairs.sort(key=lambda x: x[1], reverse=True)

        # Step 7: Format Top-N output
        recommendations = []
        seen_ids = set()

        for idx, sim in scored_pairs:
            item = self.catalog[idx]
            anime_id = int(item["anime_id"])
            if anime_id in seen_ids:
                continue
            seen_ids.add(anime_id)

            recommendations.append({
                "anime_id": anime_id,
                "title": item.get("title", ""),
                "genres": item.get("genres", []),
                "similarity": round(sim, 3),
                "similarity_percentage": min(100, int(round(sim * 100))),
                "episodes": item.get("episodes", 1),
                "rate": item.get("rate", 0.0),
                "votes": item.get("votes", 0),
                "anime_img": item.get("anime_img", ""),
                "anime_url": item.get("anime_url", "")
            })

            if len(recommendations) >= top_n:
                break

        return recommendations
