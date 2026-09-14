"""
Pure Python Recommender System Core Algorithms for Anime-DSRS.
Implements the core recommendation paradigms:
- Popularity-Based Recommender (Highest average rating from highest votes consensus)
- Content-Based Cosine Similarity (29-Genre Vector Space Model)
- Latent Factor Matrix Factorization / Truncated SVD
- User-Based & Item-Based Collaborative Filtering (k-NN)
- Knowledge-Based Constraints & Multi-Attribute Case Similarity
- Context-Aware Time Availability & Relevance Multipliers
"""

import math
import json
import csv
from typing import List, Dict, Any, Tuple, Optional

# ============================================================
# VECTOR MATHEMATICS & COSINE SIMILARITY
# ============================================================

def dot_product(v1: List[float], v2: List[float]) -> float:
    """Computes Euclidean dot product of two vectors."""
    return sum(a * b for a, b in zip(v1, v2))

def vector_norm(v: List[float]) -> float:
    """Computes L2 Euclidean norm of a vector."""
    return math.sqrt(sum(x * x for x in v))

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """
    Cosine Similarity between two numeric vectors.
    sim(A, B) = (A . B) / (||A|| * ||B||)
    """
    norm1 = vector_norm(v1)
    norm2 = vector_norm(v2)
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return dot_product(v1, v2) / (norm1 * norm2)

# ============================================================
# POPULARITY-BASED RECOMMENDATION: Highest Average Rating from Highest Votes
# ============================================================

def recommend_popular(
    catalog: List[Dict[str, Any]],
    pool_size: int = 100,
    top_n: int = 10
) -> List[Dict[str, Any]]:
    """
    Popularity-based recommendation: selects the highest average rating
    from the pool of highest-voted anime across the community.
    No Bayesian smoothing is used.
    """
    # 1. Select the pool of highest-voted anime
    highest_voted = sorted(catalog, key=lambda x: x.get("votes", 0), reverse=True)[:max(pool_size, top_n * 4)]
    # 2. Sort by highest average rating descending, with total votes as tie-breaker
    highest_voted.sort(key=lambda x: (x.get("rate", 0.0), x.get("votes", 0)), reverse=True)
    return highest_voted[:top_n]

# ============================================================
# CONTENT-BASED SIMILARITY RECOMMENDATION
# ============================================================

def recommend_content_similar(
    target_anime: Dict[str, Any],
    catalog: List[Dict[str, Any]],
    top_n: int = 10
) -> List[Tuple[Dict[str, Any], float]]:
    """
    Recommends items most similar to target anime using genre cosine similarity.
    """
    target_vec = target_anime["genre_vector"]
    scores = []

    for item in catalog:
        if item["anime_id"] == target_anime["anime_id"]:
            continue
        sim = cosine_similarity(target_vec, item["genre_vector"])
        if sim > 0.0:
            scores.append((item, sim))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]

def get_reference_content_vector(
    user_ratings: List[Dict[str, Any]],
    catalog_map: Dict[int, Dict[str, Any]]
) -> Tuple[List[float], Dict[str, float], Optional[Dict[str, Any]]]:
    """
    Pure Content-Based Reference Item extraction:
    Uses the user's latest selected or rated anime as the active reference anime.
    Ratings (1-5 stars) indicate user selection/like and do NOT apply mathematical weighting
    (Rating - 3.0 is strictly prohibited).

    Returns:
        (reference_vector, genres_dict, reference_anime)
    """
    dim = 29
    if not user_ratings:
        return [0.0] * dim, {}, None

    # Use the most recent rated or selected anime as the reference item
    latest_rating = user_ratings[-1]
    ref_anime = catalog_map.get(int(latest_rating["anime_id"]))
    if not ref_anime or "genre_vector" not in ref_anime:
        return [0.0] * dim, {}, None

    ref_vector = ref_anime["genre_vector"]
    preferred_genres = {g: 1.0 for g in ref_anime.get("genres", [])}

    return ref_vector, preferred_genres, ref_anime

# ============================================================
# KNOWLEDGE-BASED RECOMMENDATION & EXPLAINABILITY
# ============================================================

# Domain Knowledge Rules: Mood -> Preferred Genre Mapping
MOOD_GENRE_MAP = {
    "exciting": ["action", "shonen", "super power", "tournament", "martial arts"],
    "chill": ["slice of life", "comedy", "romance"],
    "dark": ["psychological", "thriller", "horror", "mystery"],
    "emotional": ["drama", "romance", "slice of life"]
}

def get_episode_commitment(episodes: int) -> str:
    """
    Domain Knowledge Rule: Viewing Commitment Classification
    IF episodes <= 13 THEN short commitment
    IF episodes > 13 AND episodes <= 26 THEN medium commitment
    IF episodes > 26 THEN long commitment
    """
    if episodes <= 13:
        return "Short (≤ 13 eps)"
    elif episodes <= 26:
        return "Medium (14–26 eps)"
    else:
        return "Long (> 26 eps)"

def evaluate_kbr_rules(
    anime: Dict[str, Any],
    constraints: Dict[str, Any],
    mood: Optional[str] = None
) -> Tuple[bool, List[Dict[str, Any]], float]:
    """
    Evaluates explicit Knowledge-Based rules against an anime candidate.
    Returns:
        (all_hard_rules_passed, rule_evaluations_list, kbr_fit_score)
    """
    rules = []
    hard_passed = True
    anime_genres = set(g.lower() for g in anime.get("genres", []))
    rate = float(anime.get("rate", 0.0))
    episodes = int(anime.get("episodes", 1))

    # Rule 1: Maximum Episodes Limit
    max_eps = constraints.get("max_episodes")
    if max_eps:
        max_eps = int(max_eps)
        passed = (episodes <= max_eps)
        if not passed:
            hard_passed = False
        rules.append({
            "rule": "Episode Commitment",
            "target": f"≤ {max_eps} episodes",
            "actual": f"{episodes} eps ({get_episode_commitment(episodes)})",
            "passed": passed,
            "is_hard": True
        })

    # Rule 2: Minimum Rating Threshold
    min_rate = constraints.get("min_rating")
    if min_rate:
        min_rate = float(min_rate)
        passed = (rate >= min_rate)
        if not passed:
            hard_passed = False
        rules.append({
            "rule": "Quality Threshold",
            "target": f"Rating ≥ {min_rate:.1f}",
            "actual": f"{rate:.2f} rating",
            "passed": passed,
            "is_hard": True
        })

    # Rule 3: Required Genres
    req_genres = [g.lower() for g in constraints.get("required_genres", [])]
    if req_genres:
        passed = all(g in anime_genres for g in req_genres)
        if not passed:
            hard_passed = False
        matched = [g for g in req_genres if g in anime_genres]
        rules.append({
            "rule": "Required Genres",
            "target": f"Must include: {', '.join(req_genres)}",
            "actual": f"Matched: {', '.join(matched) if matched else 'None'}",
            "passed": passed,
            "is_hard": True
        })

    # Rule 4: Excluded Genres
    exc_genres = [g.lower() for g in constraints.get("excluded_genres", [])]
    if exc_genres:
        violated = [g for g in exc_genres if g in anime_genres]
        passed = (len(violated) == 0)
        if not passed:
            hard_passed = False
        rules.append({
            "rule": "Excluded Genres",
            "target": f"Avoid: {', '.join(exc_genres)}",
            "actual": f"Violated: {', '.join(violated)}" if violated else "Clean (none present)",
            "passed": passed,
            "is_hard": True
        })

    # Rule 5: Viewing Mood Domain Rule (Soft Multiplier / Preference)
    mood_passed = True
    if mood and mood.lower() in MOOD_GENRE_MAP:
        preferred = MOOD_GENRE_MAP[mood.lower()]
        overlap = [g for g in preferred if g in anime_genres]
        mood_passed = (len(overlap) > 0)
        rules.append({
            "rule": "Viewing Mood",
            "target": f"Mood: {mood.capitalize()} ({', '.join(preferred[:3])})",
            "actual": f"Matched: {', '.join(overlap)}" if overlap else "No direct mood genre overlap",
            "passed": mood_passed,
            "is_hard": False
        })

    # Compute Continuous KBR Fit Score (0.0 to 1.0)
    if not hard_passed:
        fit_score = 0.0
    else:
        fit_score = 0.70  # Baseline for passing all hard criteria
        if mood_passed:
            fit_score += 0.15
        # Quality bonus (up to 0.10 for high-rated titles)
        fit_score += min(0.10, max(0.0, (rate - 3.5) / 15.0))
        # Episode proximity bonus (up to 0.05)
        if max_eps:
            fit_score += 0.05 * (1.0 - (episodes / (max_eps * 2.0)))

    fit_score = min(1.0, max(0.0, fit_score))
    return hard_passed, rules, round(fit_score, 4)

def filter_knowledge_constraints(
    catalog: List[Dict[str, Any]],
    max_episodes: Optional[int] = None,
    min_rating: Optional[float] = None,
    required_genres: Optional[List[str]] = None,
    excluded_genres: Optional[List[str]] = None,
    mood: Optional[str] = None
) -> List[Tuple[Dict[str, Any], List[Dict[str, Any]], float]]:
    """
    Evaluates all anime against knowledge rules.
    Returns:
        List of (anime_dict, rule_evaluations, kbr_score) that pass all hard constraints.
    """
    constraints = {
        "max_episodes": max_episodes,
        "min_rating": min_rating,
        "required_genres": required_genres,
        "excluded_genres": excluded_genres
    }
    candidates = []
    for anime in catalog:
        passed, rules, score = evaluate_kbr_rules(anime, constraints, mood)
        if passed:
            candidates.append((anime, rules, score))
    return candidates

# ============================================================
# MEMORY-BASED COLLABORATIVE FILTERING
# ============================================================

def predict_user_cf_rating(
    target_user_ratings: Dict[int, float],
    all_users_matrix: Dict[int, Dict[int, float]],
    target_anime_id: int,
    k_neighbors: int = 10
) -> Tuple[float, List[Tuple[int, float]]]:
    """
    User-based collaborative filtering using Cosine Similarity on common ratings.
    """
    similarities = []

    for other_user_id, other_ratings in all_users_matrix.items():
        if target_anime_id not in other_ratings:
            continue
        
        # Find co-rated anime
        common_anime = set(target_user_ratings.keys()).intersection(other_ratings.keys())
        if len(common_anime) < 2:
            continue
        
        v1 = [target_user_ratings[a] for a in common_anime]
        v2 = [other_ratings[a] for a in common_anime]
        sim = cosine_similarity(v1, v2)
        if sim > 0:
            similarities.append((other_user_id, sim, other_ratings[target_anime_id]))

    if not similarities:
        return (0.0, [])

    # Sort top-k neighbors
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_k = similarities[:k_neighbors]

    weighted_sum = sum(sim * rating for _, sim, rating in top_k)
    sim_sum = sum(sim for _, sim, _ in top_k)

    predicted_rating = weighted_sum / sim_sum if sim_sum > 0 else 0.0
    return (round(predicted_rating, 2), [(u, round(s, 3)) for u, s, _ in top_k])

# ============================================================
# MATRIX FACTORIZATION / TRUNCATED SVD
# ============================================================

class SVDModel:
    """
    Latent Factor Model for anime recommendations.
    Uses power-iteration / alternating gradient updates to learn latent vectors P and Q.
    """
    def __init__(self, n_factors: int = 20, lr: float = 0.01, reg: float = 0.05, n_epochs: int = 15):
        self.n_factors = n_factors
        self.lr = lr
        self.reg = reg
        self.n_epochs = n_epochs
        self.user_factors = {}
        self.item_factors = {}
        self.global_mean = 3.65
        self.user_biases = {}
        self.item_biases = {}

    def fit(self, ratings: List[Tuple[int, int, float]]):
        import random
        # Initialize
        users = set(r[0] for r in ratings)
        items = set(r[1] for r in ratings)
        self.global_mean = sum(r[2] for r in ratings) / len(ratings)

        for u in users:
            self.user_factors[u] = [random.uniform(-0.1, 0.1) for _ in range(self.n_factors)]
            self.user_biases[u] = 0.0
        for i in items:
            self.item_factors[i] = [random.uniform(-0.1, 0.1) for _ in range(self.n_factors)]
            self.item_biases[i] = 0.0

        # SGD updates
        for epoch in range(self.n_epochs):
            for u, i, r in ratings:
                pred = self.predict(u, i)
                err = r - pred

                # Update biases
                self.user_biases[u] += self.lr * (err - self.reg * self.user_biases[u])
                self.item_biases[i] += self.lr * (err - self.reg * self.item_biases[i])

                # Update latent factors
                p = self.user_factors[u]
                q = self.item_factors[i]
                for f in range(self.n_factors):
                    p_f = p[f]
                    q_f = q[f]
                    p[f] += self.lr * (err * q_f - self.reg * p_f)
                    q[f] += self.lr * (err * p_f - self.reg * q_f)

    def predict(self, u: int, i: int) -> float:
        """Predicts rating r_hat_ui = mu + b_u + b_i + p_u . q_i"""
        b_u = self.user_biases.get(u, 0.0)
        b_i = self.item_biases.get(i, 0.0)
        p = self.user_factors.get(u)
        q = self.item_factors.get(i)

        dot = sum(p[f] * q[f] for f in range(self.n_factors)) if p and q else 0.0
        val = self.global_mean + b_u + b_i + dot
        return max(1.0, min(5.0, val))
