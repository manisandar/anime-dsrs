const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const fs = require('fs');
const path = require('path');
const http = require('http');

const app = express();
const PORT = process.env.PORT || 5001;
const RECOMMENDER_URL = process.env.RECOMMENDER_URL || 'http://127.0.0.1:8000';

app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Load clean anime catalog
const CATALOG_PATH = path.join(__dirname, '../../data/processed/anime_catalog.json');
let animeCatalog = [];

try {
  const rawData = fs.readFileSync(CATALOG_PATH, 'utf-8');
  animeCatalog = JSON.parse(rawData);
  console.log(`[Express Gateway] Loaded ${animeCatalog.length} anime titles.`);
} catch (err) {
  console.error('[Express Gateway] Error reading anime catalog:', err.message);
}

// In-memory active user ratings store (simulates database session persistence)
const userRatingsStore = new Map();

// Helper to make HTTP requests to Python Recommender Service
function queryRecommender(endpoint, payload = null, method = 'POST') {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, RECOMMENDER_URL);
    const options = {
      method: method,
      headers: {}
    };

    let postData = null;
    if (payload && method !== 'GET') {
      postData = JSON.stringify(payload);
      options.headers['Content-Type'] = 'application/json';
      options.headers['Content-Length'] = Buffer.byteLength(postData);
    }

    const req = http.request(url, options, (res) => {
      let body = '';
      res.on('data', (chunk) => (body += chunk));
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          reject(new Error(`Recommender response parsing failed: ${body}`));
        }
      });
    });

    req.on('error', (err) => reject(err));
    if (postData) req.write(postData);
    req.end();
  });
}

// ----------------------------------------------------------------------
// REST API ENDPOINTS
// ----------------------------------------------------------------------

// 1. Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'online',
    gateway: 'anime-dsrs-node-express',
    recommender_target: RECOMMENDER_URL,
    catalog_count: animeCatalog.length,
  });
});

// 2. Catalog browsing with pagination, genre search, and sorting
app.get('/api/anime', (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const genre = req.query.genre ? req.query.genre.toLowerCase() : null;
  const search = req.query.search ? req.query.search.toLowerCase() : null;
  const sortBy = req.query.sort || 'votes'; // 'votes' | 'rate' | 'episodes'

  let filtered = animeCatalog;

  if (genre) {
    filtered = filtered.filter((item) =>
      item.genres.some((g) => g.toLowerCase() === genre)
    );
  }

  if (search) {
    filtered = filtered.filter((item) =>
      item.title.toLowerCase().includes(search)
    );
  }

  if (sortBy === 'rate') {
    filtered.sort((a, b) => b.rate - a.rate);
  } else if (sortBy === 'episodes') {
    filtered.sort((a, b) => b.episodes - a.episodes);
  } else {
    filtered.sort((a, b) => b.votes - a.votes);
  }

  const total = filtered.length;
  const start = (page - 1) * limit;
  const results = filtered.slice(start, start + limit);

  res.json({
    page,
    limit,
    total,
    totalPages: Math.ceil(total / limit),
    results,
  });
});

// 2.5 Batch anime details lookup (for session ratings, favorites, etc.)
app.post('/api/anime/batch', (req, res) => {
  const ids = Array.isArray(req.body.ids) ? req.body.ids.map((id) => parseInt(id)) : [];
  const idSet = new Set(ids);
  const matched = animeCatalog.filter((a) => idSet.has(a.anime_id));
  
  // Preserve order if requested
  const orderMap = new Map();
  ids.forEach((id, idx) => orderMap.set(id, idx));
  matched.sort((a, b) => (orderMap.get(a.anime_id) ?? 0) - (orderMap.get(b.anime_id) ?? 0));

  res.json({ success: true, data: matched });
});

// 3. Single anime detail lookup
app.get('/api/anime/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const anime = animeCatalog.find((a) => a.anime_id === id);
  if (!anime) {
    return res.status(404).json({ error: 'Anime not found' });
  }
  res.json(anime);
});

// 4. Content-Based Item Similarity (Cosine Similarity on 29 Genres)
app.get('/api/anime/:id/similar', async (req, res) => {
  const id = parseInt(req.params.id);
  const topK = parseInt(req.query.limit) || 6;

  try {
    const data = await queryRecommender('/similar', { anime_id: id, top_k: topK });
    res.json(data);
  } catch (err) {
    res.status(502).json({
      error: 'Recommender microservice connection error',
      details: err.message,
    });
  }
});

// 5. Popularity-Based Recommendations (Cold-start and independent popular feed)
app.get('/api/recommendations/popular', async (req, res) => {
  try {
    const response = await queryRecommender('/popular', null, 'GET');
    res.json(response);
  } catch (err) {
    // Fallback directly from local catalog sorted by votes/rate
    const top = [...animeCatalog].sort((a, b) => b.votes - a.votes).slice(0, 18);
    res.json({ success: true, data: top });
  }
});

// 6. Personalized Content-Based Filtering (Derived from user's session ratings)
app.post('/api/recommendations/cbf', async (req, res) => {
  const sessionRatings = req.body.session_ratings || req.body.sessionRatings || [];
  const topK = req.body.top_k || req.body.topK || 12;

  try {
    const response = await queryRecommender('/recommend/cbf', {
      session_ratings: sessionRatings,
      top_k: topK,
    });
    res.json(response);
  } catch (err) {
    res.status(502).json({
      error: 'Recommender microservice connection error',
      details: err.message,
    });
  }
});

// 7. Knowledge-Based Recommendation (Constraint Satisfaction & Explainable Rules)
app.post('/api/recommendations/kbr', async (req, res) => {
  const constraints = req.body.constraints || {};
  const mood = req.body.mood || null;
  const topK = req.body.top_k || req.body.topK || 12;

  try {
    const response = await queryRecommender('/recommend/kbr', {
      constraints,
      mood,
      top_k: topK,
    });
    res.json(response);
  } catch (err) {
    res.status(502).json({
      error: 'Recommender microservice connection error',
      details: err.message,
    });
  }
});

// 8. 1+1 Hybrid Recommendation: Smart Match (50% CBF Taste + 50% KBR Requirements)
app.post('/api/recommendations/hybrid', async (req, res) => {
  const sessionRatings = req.body.session_ratings || req.body.sessionRatings || [];
  const constraints = req.body.constraints || {};
  const mood = req.body.mood || req.body.context || null;
  const topK = req.body.top_k || req.body.topK || 12;

  try {
    const payload = {
      session_ratings: sessionRatings,
      constraints: constraints,
      mood: mood,
      top_k: topK,
    };

    const response = await queryRecommender('/recommend/hybrid', payload);
    res.json(response);
  } catch (err) {
    res.status(502).json({
      error: 'Recommender microservice connection error',
      details: err.message,
    });
  }
});

// 6. Submit user rating (updates user profile for Content-Based Filtering)
app.post('/api/ratings', (req, res) => {
  const { user_id, anime_id, rating } = req.body;
  if (!user_id || !anime_id || typeof rating !== 'number') {
    return res.status(400).json({ error: 'Missing user_id, anime_id, or rating' });
  }

  if (!userRatingsStore.has(user_id)) {
    userRatingsStore.set(user_id, []);
  }

  const list = userRatingsStore.get(user_id);
  const existingIdx = list.findIndex((r) => r.anime_id === anime_id);

  if (existingIdx >= 0) {
    list[existingIdx].rating = rating;
  } else {
    list.push({ anime_id, rating });
  }

  res.json({
    success: true,
    user_id,
    rated_count: list.length,
    ratings: list,
  });
});

// 7. Get user rating history
app.get('/api/users/:id/ratings', (req, res) => {
  const userId = parseInt(req.params.id);
  const ratings = userRatingsStore.get(userId) || [];
  const populated = ratings.map((r) => ({
    ...r,
    anime: animeCatalog.find((a) => a.anime_id === r.anime_id) || null,
  }));
  res.json({ user_id: userId, count: populated.length, ratings: populated });
});

app.listen(PORT, () => {
  console.log(`[Express Gateway] Server listening on http://127.0.0.1:${PORT}`);
});
