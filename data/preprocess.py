#!/usr/bin/env python3
"""
Data preprocessing and user-interaction bridge builder for Anime-DSRS.
Processes:
1. anime-dsrs/data/raw/crunchyroll_anime.csv (1,255 rows, 41 columns)
Produces:
1. anime-dsrs/data/processed/anime_catalog.json (Normalized catalog with unique IDs)
2. anime-dsrs/data/processed/anime_catalog.csv
3. anime-dsrs/data/processed/genre_profiles.json (29 genre dimensions per anime)
4. anime-dsrs/data/processed/user_ratings.csv (Seeded ratings matrix across 500 benchmark users + 5 course personas)
"""

import csv
import json
import math
import os
import random

RAW_CSV = "anime-dsrs/data/raw/crunchyroll_anime.csv"
PROCESSED_DIR = "anime-dsrs/data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

GENRE_COLS = [
    'genre_action', 'genre_adventure', 'genre_comedy', 'genre_drama', 'genre_family',
    'genre_fantasy', 'genre_food', 'genre_harem', 'genre_historical', 'genre_horror',
    'genre_idols', 'genre_isekai', 'genre_jdrama', 'genre_magical girls', 'genre_martial arts',
    'genre_mecha', 'genre_music', 'genre_mystery', 'genre_post-apocalyptic', 'genre_romance',
    'genre_sci-fi', 'genre_seinen', 'genre_sgdrama', 'genre_shojo', 'genre_shonen',
    'genre_slice of life', 'genre_sports', 'genre_supernatural', 'genre_thriller'
]

clean_catalog = []
genre_names = [col.replace('genre_', '') for col in GENRE_COLS]

print(f"Loading raw anime data from {RAW_CSV}...")
with open(RAW_CSV, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader, start=1):
        title = row['anime'].strip()
        episodes_raw = row['episodes'].strip()
        votes_raw = row['votes'].strip()
        rate_raw = row['rate'].strip()

        try:
            episodes = int(float(episodes_raw)) if episodes_raw else 12
            if episodes <= 0:
                episodes = 12  # fallback default
        except ValueError:
            episodes = 12

        try:
            votes = int(float(votes_raw)) if votes_raw else 0
        except ValueError:
            votes = 0

        try:
            rate = round(float(rate_raw), 2) if rate_raw else 3.50
        except ValueError:
            rate = 3.50

        # Known genre fallbacks for major legacy titles that lacked tags on crawler date
        TITLE_FALLBACKS = {
            'Naruto Shippuuden': ['action', 'adventure', 'shonen', 'martial arts', 'fantasy'],
            'Naruto': ['action', 'adventure', 'shonen', 'martial arts', 'fantasy'],
            'BLEACH': ['action', 'adventure', 'shonen', 'supernatural'],
            'Hunter x Hunter': ['action', 'adventure', 'shonen', 'fantasy'],
            'Fate/Zero': ['action', 'fantasy', 'supernatural', 'thriller'],
            "JoJo's Bizarre Adventure": ['action', 'adventure', 'supernatural', 'shonen'],
            'Gintama': ['action', 'comedy', 'sci-fi', 'shonen', 'historical'],
            'Durarara!!': ['action', 'mystery', 'supernatural'],
            'Blue Exorcist': ['action', 'fantasy', 'supernatural', 'shonen'],
            'Shugo Chara': ['comedy', 'fantasy', 'magical girls', 'shojo'],
            'REBORN!': ['action', 'comedy', 'shonen', 'supernatural'],
            'Chihayafuru': ['drama', 'sports', 'slice of life', 'romance'],
            'Time of Eve': ['sci-fi', 'slice of life', 'drama'],
            'Hayate the Combat Butler! (S1 e S2)': ['comedy', 'romance', 'harem'],
            'Linebarrels of Iron': ['action', 'mecha', 'sci-fi']
        }

        # Extract active genres list
        active_genres = []
        genre_vector = []
        for col in GENRE_COLS:
            genre_key = col.replace('genre_', '')
            raw_v = row.get(col, 0)
            val = int(float(raw_v)) if raw_v else 0
            # Check fallback if needed
            if val == 0 and title in TITLE_FALLBACKS and genre_key in TITLE_FALLBACKS[title]:
                val = 1
            genre_vector.append(val)
            if val == 1:
                active_genres.append(genre_key)

        item = {
            "anime_id": idx,
            "title": title,
            "anime_url": row.get('anime_url', ''),
            "anime_img": row.get('anime_img', ''),
            "episodes": episodes,
            "votes": votes,
            "rate": rate,
            "rate_1": int(row.get('rate_1', 0) or 0),
            "rate_2": int(row.get('rate_2', 0) or 0),
            "rate_3": int(row.get('rate_3', 0) or 0),
            "rate_4": int(row.get('rate_4', 0) or 0),
            "rate_5": int(row.get('rate_5', 0) or 0),
            "genres": active_genres,
            "genre_vector": genre_vector
        }
        clean_catalog.append(item)

print(f"Cleaned {len(clean_catalog)} anime records.")

# Save catalog JSON
with open(os.path.join(PROCESSED_DIR, "anime_catalog.json"), "w", encoding="utf-8") as f:
    json.dump(clean_catalog, f, indent=2)

# Save catalog CSV
with open(os.path.join(PROCESSED_DIR, "anime_catalog.csv"), "w", encoding="utf-8", newline='') as f:
    fieldnames = [
        "anime_id", "title", "anime_url", "anime_img", "episodes", "votes", "rate",
        "genres", "rate_1", "rate_2", "rate_3", "rate_4", "rate_5"
    ] + GENRE_COLS
    writer = csv.writer(f)
    writer.writerow(fieldnames)
    for a in clean_catalog:
        row = [
            a["anime_id"], a["title"], a["anime_url"], a["anime_img"],
            a["episodes"], a["votes"], a["rate"], "|".join(a["genres"]),
            a["rate_1"], a["rate_2"], a["rate_3"], a["rate_4"], a["rate_5"]
        ] + a["genre_vector"]
        writer.writerow(row)

# ============================================================
# SYNTHESIZE REALISTIC BENCHMARK USER INTERACTION MATRIX
# ============================================================
print("Synthesizing User-Item interaction matrix for CF and SVD models...")

random.seed(42)

ratings_rows = []
rating_id = 1

personas = {
    1: {"name": "Alice", "preferred": ["action", "shonen", "supernatural"], "disliked": ["romance", "slice of life"]},
    2: {"name": "Bob", "preferred": ["romance", "drama", "shojo"], "disliked": ["action", "mecha"]},
    3: {"name": "Carol", "preferred": ["sci-fi", "thriller", "mystery"], "disliked": ["food", "idols"]},
    4: {"name": "David", "preferred": ["action", "adventure", "fantasy"], "disliked": ["jdrama"]},
    5: {"name": "Emma", "preferred": ["slice of life", "comedy", "food"], "disliked": ["horror", "thriller"]}
}

for u_id, p_info in personas.items():
    rated_count = 0
    for anime in clean_catalog:
        match_pref = any(g in p_info["preferred"] for g in anime["genres"])
        match_dis = any(g in p_info["disliked"] for g in anime["genres"])
        if match_pref and random.random() < 0.35:
            score = random.choice([4.0, 4.5, 5.0])
            ratings_rows.append((rating_id, u_id, anime["anime_id"], score))
            rating_id += 1
            rated_count += 1
        elif match_dis and random.random() < 0.15:
            score = random.choice([1.0, 1.5, 2.0, 2.5])
            ratings_rows.append((rating_id, u_id, anime["anime_id"], score))
            rating_id += 1
            rated_count += 1
        if rated_count >= 30:
            break

for u_id in range(6, 501):
    cluster = random.choice(["action", "romance", "scifi", "comedy", "general"])
    sample_size = random.randint(15, 60)
    candidate_pool = [a for a in clean_catalog if a["votes"] > 500]
    chosen_anime = random.sample(candidate_pool, min(sample_size, len(candidate_pool)))
    for a in chosen_anime:
        base = a["rate"]
        noise = random.gauss(0, 0.6)
        r = round(max(1.0, min(5.0, base + noise)) * 2) / 2
        ratings_rows.append((rating_id, u_id, a["anime_id"], r))
        rating_id += 1

print(f"Generated {len(ratings_rows)} rating records across 500 users.")

with open(os.path.join(PROCESSED_DIR, "user_ratings.csv"), "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["rating_id", "user_id", "anime_id", "rating"])
    for r in ratings_rows:
        writer.writerow(r)

print("Data processing and interaction matrix generation completed successfully!")
