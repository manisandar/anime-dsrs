# ANIVIBE — Anime Decision Support & Hybrid Recommendation System

**Academic Recommendation & Decision Intelligence Platform**  
*Assumption University — Vincent Mary School of Science and Technology*  
*Course: CSX/ITX 4207 Decision Support and Recommendation System*

---

## 🌐 Live System Links
- **Interactive Web Application**: [https://minkhanttin-anivibe.static.hf.space](https://minkhanttin-anivibe.static.hf.space)
- **Hugging Face Space**: [https://huggingface.co/spaces/minkhanttin/anivibe](https://huggingface.co/spaces/minkhanttin/anivibe)

---

## 📖 System Overview

ANIVIBE is an academic anime decision support and recommendation system designed to solve the *Paradox of Choice* in entertainment streaming. Built on a dataset of **1,255 Crunchyroll anime titles** and user preference matrices, it strictly separates and synthesizes 4 core academic recommendation paradigms:

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                         ANIVIBE RECOMMENDATION ARCHITECTURE                    │
├────────────────────────────────┬───────────────────────────────────────────────┤
│ Paradigm                       │ Implementation & Mathematical Model           │
├────────────────────────────────┼───────────────────────────────────────────────┤
│ 1. Popularity Baseline         │ Bayesian Weighted Rating (Chapter 3)          │
│ 2. Content-Based Filtering     │ 29-Genre Cosine Similarity & Profile (Ch 4)   │
│ 3. Knowledge-Based Recommender │ Multi-attribute Constraints & Mood Rules (Ch 7)│
│ 4. 1+1 Hybrid Recommender      │ 50% CBF Taste + 50% KBR Requirements (Ch 10)  │
└────────────────────────────────┴───────────────────────────────────────────────┘
```

---

## 🔬 The 4 Academic Recommendation Paradigms

### 1. Popularity-Based Baseline (Chapter 3)
Resolves low-sample bias using the **Bayesian Mean Consensus Rating Formula**:
$$WR = \left(\frac{v}{v + m}\right) R + \left(\frac{m}{v + m}\right) C$$
- $v$: Number of ratings/votes for the candidate anime
- $m$: Minimum vote threshold ($m = 100$)
- $R$: Average raw viewer rating
- $C$: Global mean rating across entire Crunchyroll catalog ($C = 3.65$)

### 2. Content-Based Filtering (Chapter 4)
- **Item-to-Item Similarity ("More Like This")**: Computes cosine similarity between 29-dimensional binary genre feature vectors:
  $$\text{Cosine Similarity}(u, v) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$
- **Personalized User Profile ("Recommended For You")**: Dynamically constructs a user preference vector from active 1–5 star session ratings:
  $$\mathbf{P} = \sum_{i \in \text{Rated}} (r_i - 3.0) \cdot \mathbf{g}_i$$
  Positive ratings ($4\text{--}5\star$) increase genre weights; negative ratings ($1\text{--}2\star$) penalize affinities.

### 3. Knowledge-Based Recommendation (Chapter 7)
Filters candidates through explicit hard constraint satisfaction and soft domain reasoning:
- **Hard Constraints**: Episode budget limit ($\le N$ eps), minimum quality threshold ($\text{Rating} \ge R_{min}$), and required/excluded genres.
- **Domain Knowledge Rules**: Viewing commitment categorization (Short $\le 13$, Medium $14\text{--}26$, Long $> 26$) and mood affinity multipliers (e.g., *Exciting*, *Chill*, *Dark*, *Emotional*).
- **Explainability**: Outputs human-readable evaluation verdicts for every rule.

### 4. 1+1 Hybrid Recommendation: "Smart Match" (Chapter 10)
Combines **User Taste Affinity** ($S_{\text{CBF}}$) with **Situational Requirement Fit** ($S_{\text{KBR}}$):
$$S_{\text{Hybrid}} = 0.50 \cdot S_{\text{CBF}} + 0.50 \cdot S_{\text{KBR}}$$
- Automatically detects cold-start states (0 ratings) and prompts user feedback.

---

## 📊 Academic Evaluation Benchmarks

Benchmarked across representative cold-start and experienced user profiles (`python3 recommender/evaluate.py`):

| Recommendation Paradigm | Precision@10 | Recall@10 | Intra-List Diversity | Catalog Coverage |
| :--- | :---: | :---: | :---: | :---: |
| **Popularity Baseline [Ch 3]** | 0.3000 | 0.0158 | 0.7801 | 0.8% |
| **Content-Based CBF [Ch 4]** | 0.5500 | 0.0380 | 0.1334 | 3.2% |
| **Knowledge-Based KBR [Ch 7]** | 0.7750 | 0.0933 | 0.5248 | 2.4% |
| **1+1 Hybrid (CBF + KBR) [Ch 10]** | **1.0000** | **0.1175** | 0.2017 | 3.2% |

---

## 📂 Repository Structure

```
anime-dsrs/
├── recommender/                  # Core Python Recommender Engine
│   ├── algorithms.py             # Math: Bayesian, Cosine, Profile Vector, KBR rules
│   ├── pipeline.py               # 4-paradigm unified pipeline
│   ├── evaluate.py               # Academic benchmark test suite
│   └── server.py                 # Pure Python REST microservice (Port 8000)
├── data/
│   └── processed/
│       ├── anime_catalog.json    # 1,255 preprocessed Crunchyroll anime records
│       └── user_ratings.csv      # User interaction dataset
├── client/                       # Interactive Frontend Web Application
│   ├── src/
│   │   ├── pages/                # Home, Detail, Browse, Smart Match, Decision Center
│   │   ├── components/           # NetflixRow carousel, AnimeCard, Star rating
│   │   └── services/
│   │       ├── localEngine.js    # Client-side academic engine for zero-latency execution
│   │       └── api.js            # Unified API service with automatic fallback
├── deploy/
│   ├── huggingface/              # Hugging Face FastAPI/Gradio bundle
│   └── huggingface_static/       # Production static build for Hugging Face Spaces
├── scripts/
│   └── deploy_to_hf.sh           # One-command build & push via HF CLI
├── DEPLOYMENT.md                 # Cloud deployment documentation
└── HANDOVER.md                   # Full system architecture specification
```

---

## 🚀 Running Locally

### 1. Run the Frontend (React + Vite)
```bash
cd client
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

### 2. Run Academic Benchmarks (Python)
```bash
python3 recommender/evaluate.py
```

### 3. Run Python Recommender Microservice
```bash
python3 recommender/server.py 8000
```
