"""
ANIVIBE 4-Paradigm Recommender Pipeline.
CSX/ITX 4207: Decision Support and Recommendation System, Assumption University.

Strictly separates:
1. Popularity-Based Recommendation (Highest average rating from highest votes)
2. Content-Based Filtering (CBF):
   - Item-to-Item ("More Like This" on Detail page)
   - Personalized User Profile ("Recommended For You" based on session ratings)
3. Knowledge-Based Recommendation (KBR):
   - Explicit situation constraints (episodes, rating, genres) + domain rules (mood, commitment)
   - Explainable rule evaluations ("Why does this match?")
4. 1+1 Hybrid Recommendation (CBF + KBR):
   - "Smart Match": 50% User Taste (CBF) + 50% Requirement Fit (KBR)
   - Graceful cold-start handling when user has 0 ratings.
"""

import json
import os
from typing import List, Dict, Any, Optional, Tuple

try:
    from recommender.algorithms import (
        cosine_similarity,
        recommend_popular,
        get_reference_content_vector,
        evaluate_kbr_rules,
        recommend_content_similar
    )
    from recommender.cbf import ContentBasedRecommender
except ModuleNotFoundError:
    from algorithms import (
        cosine_similarity,
        recommend_popular,
        get_reference_content_vector,
        evaluate_kbr_rules,
        recommend_content_similar
    )
    from cbf import ContentBasedRecommender

class RecommenderPipeline:
    def __init__(self, catalog_path: str):
        self.catalog_path = catalog_path
        self.catalog = []
        self.catalog_map = {}
        self.cbf = None
        self.load_data()

    def load_data(self):
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)
            self.catalog_map = {item["anime_id"]: item for item in self.catalog}
        self.cbf = ContentBasedRecommender(self.catalog)
        print(f"[RecommenderPipeline] Loaded {len(self.catalog)} anime records; CBF initialized with {len(self.cbf.vocabulary)} genres.")

    # ----------------------------------------------------------------------
    # 1. POPULARITY-BASED RECOMMENDATION: Highest Average Rating from Highest Votes
    # ----------------------------------------------------------------------
    def get_popular(self, top_k: int = 12, pool_size: int = 100) -> List[Dict[str, Any]]:
        """
        Global consensus recommendations based on highest average rating from highest votes.
        No Bayesian smoothing.
        1. Selects candidate pool of highest-voted anime across the catalog.
        2. Sorts by highest average rating (rate descending), tie-breaking by total votes.
        """
        return recommend_popular(self.catalog, pool_size=pool_size, top_n=top_k)

    # ----------------------------------------------------------------------
    # 2. CONTENT-BASED FILTERING (ITEM-TO-ITEM): "More Like This"
    # ----------------------------------------------------------------------
    def get_item_similar(self, anime_id: int, top_k: int = 8) -> Dict[str, Any]:
        """
        Item-to-Item CBF for Anime Detail page using CountVectorizer + Cosine Similarity.
        Compares target anime's genre count vector with all other catalog anime.
        Excludes the target anime itself.
        """
        target = self.catalog_map.get(anime_id)
        if not target:
            return {"error": "Anime not found", "similar": []}

        similar = self.cbf.recommend(anime_id, top_n=top_k)
        return {
            "target": target["title"],
            "target_id": anime_id,
            "similar": similar
        }

    # ----------------------------------------------------------------------
    # 3. CONTENT-BASED FILTERING (PERSONALIZED): "Recommended For You"
    # ----------------------------------------------------------------------
    def get_personalized_cbf(
        self,
        session_ratings: List[Dict[str, Any]],
        top_k: int = 12
    ) -> Dict[str, Any]:
        """
        Personalized CBF using user-selected/rated reference anime.
        The user's latest selected/rated anime acts as the reference item.
        Ratings are NOT mathematically weighted (Rating - 3.0 is prohibited).
        """
        if not session_ratings:
            return {
                "has_profile": False,
                "message": "No reference anime selected or rated yet. Rate or select an anime to generate Content-Based recommendations.",
                "reference_anime": None,
                "preferred_genres": {},
                "recommendations": []
            }

        ref_id = int(session_ratings[-1]["anime_id"])
        ref_anime = self.catalog_map.get(ref_id)
        if not ref_anime:
            return {
                "has_profile": False,
                "message": f"Reference anime #{ref_id} not found in catalog.",
                "reference_anime": None,
                "preferred_genres": {},
                "recommendations": []
            }

        recommendations = self.cbf.recommend(ref_id, top_n=top_k)
        preferred_genres = {g: 1.0 for g in ref_anime.get("genres", [])}

        return {
            "has_profile": True,
            "reference_anime": {
                "anime_id": ref_anime["anime_id"],
                "title": ref_anime["title"],
                "genres": ref_anime.get("genres", []),
                "rate": ref_anime.get("rate", 0),
                "anime_img": ref_anime.get("anime_img", "")
            },
            "ratings_count": len(session_ratings),
            "preferred_genres": preferred_genres,
            "recommendations": recommendations
        }

    # ----------------------------------------------------------------------
    # 4. KNOWLEDGE-BASED RECOMMENDATION: "Find What Fits"
    # ----------------------------------------------------------------------
    def get_knowledge_based(
        self,
        constraints: Dict[str, Any],
        mood: Optional[str] = None,
        top_k: int = 12
    ) -> Dict[str, Any]:
        """
        Knowledge-Based Recommendation based on explicit user requirements and domain rules.
        Completely separate from user ratings.
        Includes explainable rule evaluations for each candidate.
        """
        candidates = []

        for anime in self.catalog:
            passed, rules, score = evaluate_kbr_rules(anime, constraints, mood)
            if passed:
                candidates.append({
                    "anime_id": anime["anime_id"],
                    "title": anime["title"],
                    "anime_url": anime["anime_url"],
                    "anime_img": anime["anime_img"],
                    "episodes": anime["episodes"],
                    "votes": anime["votes"],
                    "rate": anime["rate"],
                    "rate_1": anime.get("rate_1", 0),
                    "rate_2": anime.get("rate_2", 0),
                    "rate_3": anime.get("rate_3", 0),
                    "rate_4": anime.get("rate_4", 0),
                    "rate_5": anime.get("rate_5", 0),
                    "genres": anime["genres"],
                    "kbr_score": score,
                    "match_percentage": min(99, int(round(score * 100))),
                    "rule_evaluations": rules
                })

        candidates.sort(key=lambda x: x["kbr_score"], reverse=True)

        return {
            "total_matches": len(candidates),
            "constraints_applied": constraints,
            "mood_applied": mood,
            "recommendations": candidates[:top_k]
        }

    # ----------------------------------------------------------------------
    # 5. HYBRID RECOMMENDATION: 70% KBR + 40% CBR Multi-Anime User Profile
    # ----------------------------------------------------------------------
    def get_hybrid(
        self,
        session_ratings: List[Dict[str, Any]],
        constraints: Dict[str, Any],
        mood: Optional[str] = None,
        top_k: int = 12
    ) -> Dict[str, Any]:
        """
        70/40 Hybrid Recommendation combining:
        - 70% Situation Fit Score from Knowledge-Based Rules (KBR)
        - 40% User Taste Score from Single Aggregated Content Profile across ALL rated anime (CBF)
        Formula: Hybrid Score = 0.70 * KBR + 0.40 * CBF
        """
        dim = 29
        user_profile = [0.0] * dim
        has_ratings = False
        preferred_genres = {}

        if session_ratings:
            for r in session_ratings:
                anime = self.catalog_map.get(int(r["anime_id"]))
                if anime and "genre_vector" in anime:
                    has_ratings = True
                    for i, val in enumerate(anime["genre_vector"][:dim]):
                        user_profile[i] += val
                    for g in anime.get("genres", []):
                        preferred_genres[g] = preferred_genres.get(g, 0) + 1

        candidates = []
        for anime in self.catalog:
            passed, rules, kbr_score = evaluate_kbr_rules(anime, constraints, mood)
            if not passed:
                continue

            if has_ratings:
                cbf_score = cosine_similarity(user_profile, anime["genre_vector"])
            else:
                cbf_score = 0.0

            # 70/40 Hybrid Fusion
            hybrid_score = round(0.70 * kbr_score + 0.40 * cbf_score, 4)

            candidates.append({
                "anime_id": anime["anime_id"],
                "title": anime["title"],
                "anime_url": anime["anime_url"],
                "anime_img": anime["anime_img"],
                "episodes": anime["episodes"],
                "votes": anime["votes"],
                "rate": anime["rate"],
                "rate_1": anime.get("rate_1", 0),
                "rate_2": anime.get("rate_2", 0),
                "rate_3": anime.get("rate_3", 0),
                "rate_4": anime.get("rate_4", 0),
                "rate_5": anime.get("rate_5", 0),
                "genres": anime["genres"],
                "hybrid_score": hybrid_score,
                "match_percentage": min(99, max(15, int(round((hybrid_score / 1.10) * 100)))),
                "cbf_score": round(cbf_score, 3),
                "kbr_score": round(kbr_score, 3),
                "cbf_match_pct": min(99, int(round(cbf_score * 100))) if has_ratings else 0,
                "kbr_match_pct": min(99, int(round(kbr_score * 100))),
                "rule_evaluations": rules
            })

        candidates.sort(key=lambda x: x["hybrid_score"], reverse=True)

        return {
            "cold_start": not has_ratings,
            "has_user_profile": has_ratings,
            "ratings_count": len(session_ratings),
            "preferred_genres": preferred_genres,
            "total_matches": len(candidates),
            "recommendations": candidates[:top_k]
        }
