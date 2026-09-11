import os
import json
import math
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import gradio as gr

# Import existing recommendation algorithms
from recommender.algorithms import (
    calculate_bayesian_rating,
    recommend_content_similar,
    build_user_content_profile,
    cosine_similarity,
    evaluate_kbr_rules
)
from recommender.pipeline import RecommendationPipeline

# 1. Create FastAPI application
app = FastAPI(
    title="ANIVIBE Recommender Engine",
    description="Academic Decision Support & Recommendation System microservice on Hugging Face Spaces",
    version="1.0.0"
)

# 2. Enable CORS for all external origins (Vercel, Netlify, localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load catalog data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "anime_catalog.json")

if not os.path.exists(DATA_PATH):
    DATA_PATH = os.path.join(BASE_DIR, "..", "..", "data", "processed", "anime_catalog.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    anime_catalog = json.load(f)

catalog_map = {a["anime_id"]: a for a in anime_catalog}
pipeline = RecommendationPipeline(anime_catalog)

# Request Models
class SessionRatingItem(BaseModel):
    anime_id: int
    rating: float

class CBFRequest(BaseModel):
    session_ratings: List[SessionRatingItem] = []
    top_k: int = 12

class KBRRequest(BaseModel):
    constraints: Dict[str, Any] = {}
    mood: Optional[str] = None
    top_k: int = 12

class HybridRequest(BaseModel):
    session_ratings: List[SessionRatingItem] = []
    constraints: Dict[str, Any] = {}
    mood: Optional[str] = None
    top_k: int = 12

class BatchRequest(BaseModel):
    ids: List[int] = []

class RatingSubmission(BaseModel):
    userId: int = 1
    animeId: int
    rating: float

# -------------------------------------------------------------
# REST API ENDPOINTS
# -------------------------------------------------------------
@app.get("/api/health")
@app.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "ANIVIBE Recommender Engine",
        "platform": "Hugging Face Spaces (Free Gradio SDK)",
        "catalog_size": len(anime_catalog),
        "docs_url": "/docs"
    }

@app.get("/api/anime")
@app.get("/anime")
def get_catalog(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    genre: Optional[str] = None,
    search: Optional[str] = None,
    sort: str = Query("votes", regex="^(votes|rate|episodes)$")
):
    filtered = anime_catalog
    if genre:
        g_lower = genre.lower()
        filtered = [a for a in filtered if any(g.lower() == g_lower for g in a.get("genres", []))]
    if search:
        s_lower = search.lower()
        filtered = [a for a in filtered if s_lower in a.get("title", "").lower()]

    if sort == "rate":
        filtered.sort(key=lambda x: x.get("rate", 0), reverse=True)
    elif sort == "episodes":
        filtered.sort(key=lambda x: x.get("episodes", 0), reverse=True)
    else:
        filtered.sort(key=lambda x: x.get("votes", 0), reverse=True)

    total = len(filtered)
    start = (page - 1) * limit
    results = filtered[start:start + limit]

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "totalPages": math.ceil(total / limit) if limit else 1,
        "results": results
    }

@app.get("/api/anime/{anime_id}")
@app.get("/anime/{anime_id}")
def get_anime_by_id(anime_id: int):
    anime = catalog_map.get(anime_id)
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    return anime

@app.post("/api/anime/batch")
@app.post("/anime/batch")
def get_anime_batch(req: BatchRequest):
    id_set = set(req.ids)
    matched = [a for a in anime_catalog if a["anime_id"] in id_set]
    order_map = {id_val: idx for idx, id_val in enumerate(req.ids)}
    matched.sort(key=lambda a: order_map.get(a["anime_id"], 0))
    return {"success": True, "data": matched}

@app.get("/api/anime/{anime_id}/similar")
@app.get("/anime/{anime_id}/similar")
def get_similar(anime_id: int, limit: int = Query(8, ge=1, le=50)):
    res = pipeline.get_item_similar(anime_id, top_k=limit)
    if "error" in res and res.get("similar") == []:
        raise HTTPException(status_code=404, detail="Anime not found")
    return {"success": True, "data": res, "similar": res.get("similar", [])}

@app.get("/api/recommendations/popular")
@app.get("/recommendations/popular")
@app.get("/popular")
def get_popular(top_k: int = Query(12, ge=1, le=100)):
    data = pipeline.get_popular(top_k=top_k)
    return {"success": True, "data": data}

@app.post("/api/recommendations/cbf")
@app.post("/recommendations/cbf")
def get_personalized_cbf(req: CBFRequest):
    ratings = [r.dict() for r in req.session_ratings]
    data = pipeline.get_personalized_cbf(ratings, top_k=req.top_k)
    return {"success": True, "data": data}

@app.post("/api/recommendations/kbr")
@app.post("/recommendations/kbr")
def get_knowledge_based(req: KBRRequest):
    data = pipeline.get_knowledge_based(req.constraints, mood=req.mood, top_k=req.top_k)
    return {"success": True, "data": data}

@app.post("/api/recommendations/hybrid")
@app.post("/recommendations/hybrid")
def get_hybrid(req: HybridRequest):
    ratings = [r.dict() for r in req.session_ratings]
    data = pipeline.get_hybrid(ratings, req.constraints, mood=req.mood, top_k=req.top_k)
    return {"success": True, "data": data}

@app.post("/api/ratings")
@app.post("/ratings")
def submit_rating(req: RatingSubmission):
    return {
        "success": True,
        "message": f"Rating of {req.rating} received for anime {req.animeId}",
        "rating": req.dict()
    }

# -------------------------------------------------------------
# GRADIO INTERACTIVE DASHBOARD (100% Free Hugging Face Space UI)
# -------------------------------------------------------------
def test_popular(top_k):
    results = pipeline.get_popular(top_k=int(top_k))
    return [{"Title": a["title"], "Rating": a["rate"], "Votes": a["votes"], "Bayesian Score": a["bayesian_score"]} for a in results]

def test_similar(anime_title, top_k):
    match = next((a for a in anime_catalog if anime_title.lower() in a["title"].lower()), None)
    if not match:
        return f"Anime matching '{anime_title}' not found."
    res = pipeline.get_item_similar(match["anime_id"], top_k=int(top_k))
    return [{"Title": s["title"], "Similarity": f"{s['similarity'] * 100:.1f}%", "Episodes": s["episodes"]} for s in res.get("similar", [])]

with gr.Blocks(title="ANIVIBE Recommender Engine") as demo:
    gr.Markdown("# ANIVIBE — Academic Recommender Microservice")
    gr.Markdown(
        "**Status**: Online  |  **Catalog Size**: 1,255 Anime  |  **Vector Dimensions**: 29 Genres\n\n"
        "This Hugging Face Space provides live REST API endpoints with CORS enabled for the ANIVIBE Web Application.\n"
        "- OpenAPI / Swagger Docs: **[/docs](/docs)**\n"
        "- Popularity Endpoint: **[/api/recommendations/popular](/api/recommendations/popular)**\n"
        "- Catalog Endpoint: **[/api/anime](/api/anime)**"
    )

    with gr.Tab("Popular Recommendations"):
        top_k_slider = gr.Slider(minimum=3, maximum=20, value=6, step=1, label="Top K Titles")
        btn_pop = gr.Button("Fetch Popular Titles", variant="primary")
        out_pop = gr.Dataframe(label="Consensus Rankings")
        btn_pop.click(fn=test_popular, inputs=[top_k_slider], outputs=[out_pop])

    with gr.Tab("Item-to-Item Similarity"):
        anime_query = gr.Textbox(value="Naruto", label="Anime Title")
        sim_k_slider = gr.Slider(minimum=3, maximum=10, value=5, step=1, label="Top K Similar")
        btn_sim = gr.Button("Find Similar Titles", variant="primary")
        out_sim = gr.Dataframe(label="Most Similar Titles (29-Genre Cosine Similarity)")
        btn_sim.click(fn=test_similar, inputs=[anime_query, sim_k_slider], outputs=[out_sim])

# Mount Gradio onto the FastAPI app so both the web dashboard AND /api endpoints run together
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
