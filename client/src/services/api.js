/**
 * Centralized API Service for Anime-DSRS.
 * Communicates with Express Gateway (/api) or direct Python service.
 * Automatically falls back to pure client-side localEngine for 100% Free
 * Static deployment on Hugging Face Spaces (sdk: static) or GitHub Pages / Vercel.
 */

import { localEngine } from './localEngine';

const getApiBase = () => {
  if (import.meta.env?.VITE_API_URL) {
    return import.meta.env.VITE_API_URL.replace(/\/$/, '');
  }
  const customUrl = localStorage.getItem('ANIME_DSRS_API_URL');
  if (customUrl) return customUrl.replace(/\/$/, '');
  return '/api';
};

// Helper: Try remote network request with timeout, seamlessly fall back to local client engine if offline/unavailable
async function tryRemoteOrLocal(remoteFn, localFn) {
  try {
    return await remoteFn();
  } catch (err) {
    // Only log if not in silent mode
    return await localFn();
  }
}

export const api = {
  // 1. Health Check
  async checkHealth() {
    return tryRemoteOrLocal(
      async () => {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 2500);
        const res = await fetch(`${getApiBase()}/health`, { signal: ctrl.signal });
        clearTimeout(tid);
        if (!res.ok) throw new Error(`Health check failed (${res.status})`);
        return res.json();
      },
      () => localEngine.checkHealth()
    );
  },

  // 2. Paginated Catalog Browsing
  async getCatalog({ page = 1, limit = 18, genre = '', search = '', sort = 'votes' } = {}) {
    return tryRemoteOrLocal(
      async () => {
        const params = new URLSearchParams({ page, limit, sort });
        if (genre) params.append('genre', genre);
        if (search) params.append('search', search);

        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 3000);
        const res = await fetch(`${getApiBase()}/anime?${params.toString()}`, { signal: ctrl.signal });
        clearTimeout(tid);
        if (!res.ok) throw new Error('Failed to load anime catalog');
        return res.json();
      },
      () => localEngine.getCatalog({ page, limit, genre, search, sort })
    );
  },

  // 3. Single Anime Details
  async getAnimeById(id) {
    return tryRemoteOrLocal(
      async () => {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 3000);
        const res = await fetch(`${getApiBase()}/anime/${id}`, { signal: ctrl.signal });
        clearTimeout(tid);
        if (!res.ok) throw new Error('Failed to fetch anime details');
        const json = await res.json();
        return json.data || json;
      },
      async () => {
        const res = await localEngine.getAnimeById(id);
        return res.data || res;
      }
    );
  },

  // 3.5 Batch Anime Details
  async getAnimeBatch(ids = []) {
    if (!ids.length) return { success: true, data: [] };
    return tryRemoteOrLocal(
      async () => {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 3000);
        const res = await fetch(`${getApiBase()}/anime/batch`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ids }),
          signal: ctrl.signal
        });
        clearTimeout(tid);
        if (!res.ok) throw new Error('Failed to fetch batch anime details');
        return res.json();
      },
      () => localEngine.getAnimeBatch(ids)
    );
  },

  // 4. Content-Based Item Similarity: "More Like This"
  async getSimilarAnime(id, limit = 8) {
    return tryRemoteOrLocal(
      async () => {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 3000);
        const res = await fetch(`${getApiBase()}/anime/${id}/similar?limit=${limit}`, { signal: ctrl.signal });
        clearTimeout(tid);
        if (!res.ok) throw new Error('Failed to fetch similar anime');
        const json = await res.json();
        const similar = json?.data?.similar || json?.similar || [];
        return { ...json, similar };
      },
      () => localEngine.getSimilarAnime(id, limit)
    );
  },

  // 5. Popularity-Based Recommendations: "Popular Right Now"
  async getPopularRecommendations({ topK = 18 } = {}) {
    return tryRemoteOrLocal(
      async () => {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 3000);
        const res = await fetch(`${getApiBase()}/recommendations/popular?top_k=${topK}`, { signal: ctrl.signal });
        clearTimeout(tid);
        if (!res.ok) throw new Error('Failed to load popular anime');
        return res.json();
      },
      () => localEngine.getPopularRecommendations({ topK })
    );
  },

  // 6. Personalized Content-Based Filtering: "Recommended For You"
  async getPersonalizedCBF({ sessionRatings = [], topK = 12 }) {
    return tryRemoteOrLocal(
      async () => {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 3000);
        const res = await fetch(`${getApiBase()}/recommendations/cbf`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_ratings: sessionRatings,
            top_k: topK,
          }),
          signal: ctrl.signal
        });
        clearTimeout(tid);
        if (!res.ok) throw new Error('Failed to compute personalized recommendations');
        return res.json();
      },
      () => localEngine.getPersonalizedCBF({ sessionRatings, topK })
    );
  },

  // 7. Knowledge-Based Recommendation: "Find What Fits"
  async getKnowledgeBased({ constraints = {}, mood = null, topK = 18 }) {
    return tryRemoteOrLocal(
      async () => {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 3000);
        const res = await fetch(`${getApiBase()}/recommendations/kbr`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            constraints,
            mood,
            top_k: topK,
          }),
          signal: ctrl.signal
        });
        clearTimeout(tid);
        if (!res.ok) throw new Error('Failed to evaluate knowledge-based recommendations');
        return res.json();
      },
      () => localEngine.getKnowledgeBased({ constraints, mood, topK })
    );
  },

  // 8. 1+1 Hybrid Recommendation: "Smart Match"
  async getHybridRecommendations({ sessionRatings = [], constraints = {}, mood = null, topK = 18 }) {
    return tryRemoteOrLocal(
      async () => {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 3000);
        const res = await fetch(`${getApiBase()}/recommendations/hybrid`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_ratings: sessionRatings,
            constraints,
            mood,
            top_k: topK,
          }),
          signal: ctrl.signal
        });
        clearTimeout(tid);
        if (!res.ok) throw new Error('Hybrid recommendation request failed');
        return res.json();
      },
      () => localEngine.getHybridRecommendations({ sessionRatings, constraints, mood, topK })
    );
  },

  // 9. Submit User Rating
  async submitRating({ userId = 1, animeId, rating }) {
    return tryRemoteOrLocal(
      async () => {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 2000);
        const res = await fetch(`${getApiBase()}/ratings`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userId, anime_id: animeId, rating }),
          signal: ctrl.signal
        });
        clearTimeout(tid);
        if (!res.ok) throw new Error('Failed to submit rating');
        return res.json();
      },
      () => localEngine.submitRating({ userId, animeId, rating })
    );
  },

  // 10. Get User Ratings History
  async getUserRatings(userId = 1) {
    return tryRemoteOrLocal(
      async () => {
        const ctrl = new AbortController();
        const tid = setTimeout(() => ctrl.abort(), 2000);
        const res = await fetch(`${getApiBase()}/users/${userId}/ratings`, { signal: ctrl.signal });
        clearTimeout(tid);
        if (!res.ok) throw new Error('Failed to fetch user rating history');
        return res.json();
      },
      () => localEngine.getUserRatings(userId)
    );
  },
};
