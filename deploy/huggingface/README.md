---
title: ANIVIBE Recommender Engine
emoji: 🚀
colorFrom: red
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
---

# ANIVIBE — Academic Decision Support & Recommender Microservice

Free Gradio + FastAPI backend microservice powering the ANIVIBE Decision Support and Recommendation System.

### Recommendation Paradigms Available via REST API
1. **Popularity-Based Recommendation**: Bayesian rating consensus ranking (`/api/recommendations/popular`)
2. **Content-Based Filtering (Item-to-Item)**: Cosine similarity on 29-genre binary vectors (`/api/anime/{id}/similar`)
3. **Content-Based Filtering (Personalized)**: Real-time user taste profiling from session ratings (`/api/recommendations/cbf`)
4. **Knowledge-Based Recommendation (KBR)**: Explicit situational constraint filtering (`/api/recommendations/kbr`)
5. **1+1 Hybrid Recommendation (Smart Match)**: Linear combination of 50% Personal Taste + 50% Constraint Fit (`/api/recommendations/hybrid`)

### API Documentation
Interactive OpenAPI / Swagger documentation is available at `/docs`.
