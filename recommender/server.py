"""
ANIVIBE Python Recommender Microservice (Port 8000).
CSX/ITX 4207: Decision Support and Recommendation System, Assumption University.

REST Endpoints:
- GET  /health           : Microservice health check and paradigm metadata
- GET  /popular          : Popularity-Based Recommendations (Highest average rating from highest votes)
- POST /recommend/cbf    : Personalized Content-Based Filtering (Session ratings)
- POST /recommend/kbr    : Knowledge-Based Recommendations (Constraints & Rules)
- POST /recommend/hybrid : 70/40 Hybrid Recommendations (KBR + CBR Multi-Anime)
- POST /similar          : Item-to-Item Content-Based Filtering ("More Like This")
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import RecommenderPipeline

CATALOG_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/anime_catalog.json")
pipeline = RecommenderPipeline(CATALOG_PATH)

class RecommenderHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            res = {
                "status": "healthy",
                "service": "anivibe-recommender-engine",
                "paradigms": {
                    "popularity": "Highest average rating from highest votes consensus",
                    "cbf_item": "Item-to-Item Cosine Similarity on 29 Genres",
                    "cbf_user": "Personalized Taste Profile from Session Ratings",
                    "kbr": "Constraint Satisfaction & Domain Rules Reasoning",
                    "hybrid": "1+1 Hybrid: 50% CBF Taste + 50% KBR Requirements"
                },
                "catalog_size": len(pipeline.catalog)
            }
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        if self.path.startswith('/popular'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            results = pipeline.get_popular(top_k=18)
            self.wfile.write(json.dumps({"success": True, "data": results}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode('utf-8')) if body else {}

        # 1. Personalized Content-Based Filtering
        if self.path == '/recommend/cbf':
            session_ratings = payload.get("session_ratings", [])
            top_k = payload.get("top_k", 12)
            results = pipeline.get_personalized_cbf(session_ratings=session_ratings, top_k=top_k)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "data": results}).encode('utf-8'))
            return

        # 2. Knowledge-Based Recommendation (Find What Fits)
        if self.path == '/recommend/kbr':
            constraints = payload.get("constraints", {})
            mood = payload.get("mood")
            top_k = payload.get("top_k", 12)
            results = pipeline.get_knowledge_based(constraints=constraints, mood=mood, top_k=top_k)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "data": results}).encode('utf-8'))
            return

        # 3. 1+1 Hybrid Recommendation (Smart Match)
        if self.path in ['/recommend/hybrid', '/recommend']:
            session_ratings = payload.get("session_ratings", [])
            constraints = payload.get("constraints", {})
            mood = payload.get("mood") or payload.get("context")
            top_k = payload.get("top_k", 12)
            results = pipeline.get_hybrid(
                session_ratings=session_ratings,
                constraints=constraints,
                mood=mood,
                top_k=top_k
            )

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "data": results}).encode('utf-8'))
            return

        # 4. Item-to-Item Content-Based Filtering (More Like This)
        if self.path == '/similar':
            anime_id = payload.get("anime_id")
            top_k = payload.get("top_k", 8)
            if not anime_id:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing anime_id"}).encode('utf-8'))
                return

            results = pipeline.get_item_similar(anime_id=int(anime_id), top_k=top_k)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "data": results}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def run_server(port=8000):
    server = HTTPServer(('0.0.0.0', port), RecommenderHandler)
    print(f"[Python Recommender] Serving 4-paradigm engine on http://0.0.0.0:{port}")
    server.serve_forever()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
