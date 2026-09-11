"""
Academic Evaluation Benchmark Suite for Anime-DSRS.
CSX/ITX 4207: Decision Support & Recommendation System, Assumption University.

Evaluates the 4 Distinct Paradigms:
1. Baseline: Popularity / Bayesian Rating Consensus
2. Group [1,2,3]: Content-Based Filtering via Session Rating Profile
3. Group [4,5,6]: Knowledge-Based Recommendation via Constraints & Rules
4. Group [7]: 1+1 Hybrid (CBF Taste + KBR Situation Requirements)

Metrics Computed:
- Precision@10: Fraction of top-10 recommendations that match target test profile
- Recall@10: Fraction of relevant catalog items captured in top-10
- Intra-List Diversity: 1 - Mean Cosine Similarity across recommended items
- Catalog Coverage: Percentage of catalog accessible across diverse recommendation seeds
"""

import os
import sys
import json
import math
from typing import List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from algorithms import cosine_similarity
from pipeline import RecommenderPipeline

def run_evaluation_benchmarks(catalog_path: str):
    print("==================================================================")
    print("ANIME-DSRS ACADEMIC EVALUATION BENCHMARK (CSX/ITX 4207)")
    print("==================================================================")

    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    catalog_map = {item["anime_id"]: item for item in catalog}

    print(f"Loaded {len(catalog)} genuine Crunchyroll anime titles.")
    pipeline = RecommenderPipeline(catalog_path)

    # Representative test sessions with sample ratings and situational constraints
    test_sessions = [
        {
            "genre": "shonen",
            "ratings": [{"anime_id": 1, "rating": 5.0}, {"anime_id": 64, "rating": 5.0}], # Naruto, MHA
            "constraints": {"max_episodes": 100, "min_rating": 4.0, "required_genres": ["action"]},
            "mood": "exciting"
        },
        {
            "genre": "romance",
            "ratings": [{"anime_id": 11, "rating": 5.0}, {"anime_id": 5, "rating": 4.5}], # Clannad, Skip Beat
            "constraints": {"max_episodes": 26, "min_rating": 4.0, "required_genres": ["romance"]},
            "mood": "chill"
        },
        {
            "genre": "thriller",
            "ratings": [{"anime_id": 180, "rating": 5.0}, {"anime_id": 57, "rating": 4.5}], # FMA, Re:Zero
            "constraints": {"max_episodes": 64, "min_rating": 4.2, "required_genres": ["thriller"]},
            "mood": "dark"
        },
        {
            "genre": "comedy",
            "ratings": [{"anime_id": 9, "rating": 5.0}, {"anime_id": 90, "rating": 4.5}], # Gintama, Bodacious
            "constraints": {"max_episodes": 30, "min_rating": 3.8, "required_genres": ["comedy"]},
            "mood": "chill"
        },
    ]

    models = [
        "Popularity Baseline",
        "Content-Based CBF",
        "Knowledge-Based KBR",
        "1+1 Hybrid (CBF+KBR)"
    ]

    benchmark_results = {}

    for model_name in models:
        all_recommended_ids = set()
        precisions = []
        recalls = []
        diversities = []

        for session in test_sessions:
            target_genre = session["genre"]
            min_r = session["constraints"]["min_rating"]

            relevant_catalog_ids = {
                a["anime_id"] for a in catalog
                if target_genre in [g.lower() for g in a["genres"]] and a["rate"] >= min_r
            }

            rec_items = []

            if "Popularity" in model_name:
                rec_items = pipeline.get_popular(top_k=10)

            elif "Content-Based" in model_name:
                res = pipeline.get_personalized_cbf(session_ratings=session["ratings"], top_k=10)
                rec_items = res.get("recommendations", [])

            elif "Knowledge-Based" in model_name:
                res = pipeline.get_knowledge_based(constraints=session["constraints"], mood=session["mood"], top_k=10)
                rec_items = res.get("recommendations", [])

            elif "1+1 Hybrid" in model_name:
                res = pipeline.get_hybrid(
                    session_ratings=session["ratings"],
                    constraints=session["constraints"],
                    mood=session["mood"],
                    top_k=10
                )
                rec_items = res.get("recommendations", [])

            rec_ids = [r["anime_id"] for r in rec_items]
            all_recommended_ids.update(rec_ids)

            hits = len(set(rec_ids).intersection(relevant_catalog_ids))
            precisions.append(hits / 10.0 if rec_ids else 0.0)
            recalls.append(hits / len(relevant_catalog_ids) if relevant_catalog_ids else 0.0)

            if len(rec_items) > 1:
                pairs = 0
                div_sum = 0.0
                for i in range(len(rec_items)):
                    for j in range(i + 1, len(rec_items)):
                        v1 = catalog_map[rec_items[i]["anime_id"]]["genre_vector"]
                        v2 = catalog_map[rec_items[j]["anime_id"]]["genre_vector"]
                        div_sum += (1.0 - cosine_similarity(v1, v2))
                        pairs += 1
                diversities.append(div_sum / pairs if pairs > 0 else 0.0)

        benchmark_results[model_name] = {
            "Precision@10": round(sum(precisions) / len(precisions) if precisions else 0.0, 4),
            "Recall@10": round(sum(recalls) / len(recalls) if recalls else 0.0, 4),
            "Intra-List Diversity": round(sum(diversities) / len(diversities) if diversities else 0.0, 4),
            "Catalog Coverage": f"{round((len(all_recommended_ids) / len(catalog)) * 100, 1)}%"
        }

    print("\n" + "=" * 90)
    print(f"{'Recommendation Paradigm':<32} | {'Precision@10':<12} | {'Recall@10':<10} | {'Diversity':<10} | {'Coverage':<10}")
    print("-" * 90)
    for name, m in benchmark_results.items():
        print(f"{name:<32} | {m['Precision@10']:<12.4f} | {m['Recall@10']:<10.4f} | {m['Intra-List Diversity']:<10.4f} | {m['Catalog Coverage']:<10}")
    print("=" * 90)
    print("\nBenchmark Evaluation completed successfully.\n")
    return benchmark_results

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    catalog_file = os.path.join(base_dir, "data", "processed", "anime_catalog.json")
    run_evaluation_benchmarks(catalog_file)
