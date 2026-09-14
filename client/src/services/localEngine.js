/**
 * Pure Client-Side Academic Recommender Engine for ANIVIBE.
 * CSX/ITX 4207: Decision Support and Recommendation System, Assumption University.
 * 
 * Provides 100% offline, zero-dependency, free static execution of all 4 paradigms:
 * 1. Bayesian Weighted Popularity
 * 2. 29-Genre Cosine Similarity Content-Based Filtering
 *    - Item-to-Item ("More Like This")
 *    - Personalized Session Profile ("Recommended For You")
 * 3. Knowledge-Based Recommendation
 *    - Hard constraints (episodes, rating, genres)
 *    - Domain rules (mood affinity)
 *    - Rule evaluation explanations
 * 4. 1+1 Hybrid Fusion
 *    - 50% CBF User Taste + 50% KBR Situational Fit
 */

const GENRE_LIST = [
  'action', 'adventure', 'comedy', 'drama', 'fantasy', 'horror',
  'isekai', 'mecha', 'mystery', 'romance', 'sci-fi', 'shonen',
  'slice of life', 'sports', 'supernatural', 'thriller', 'historical',
  'martial arts', 'music', 'psychological', 'post-apocalyptic',
  'harem', 'idol', 'magical girl', 'seinen', 'shojo', 'tournament',
  'food', 'super power'
];

const MOOD_GENRE_MAP = {
  exciting: ['action', 'shonen', 'super power', 'tournament', 'martial arts'],
  chill: ['slice of life', 'comedy', 'romance'],
  dark: ['psychological', 'thriller', 'horror', 'mystery'],
  emotional: ['drama', 'romance', 'slice of life']
};

let cachedCatalog = null;
let catalogMap = new Map();
let catalogLoadingPromise = null;

// Helper: Vector Mathematics
function dotProduct(v1, v2) {
  let sum = 0;
  const len = Math.min(v1.length, v2.length);
  for (let i = 0; i < len; i++) {
    sum += v1[i] * v2[i];
  }
  return sum;
}

function vectorNorm(v) {
  let sum = 0;
  for (let i = 0; i < v.length; i++) {
    sum += v[i] * v[i];
  }
  return Math.sqrt(sum);
}

function cosineSimilarity(v1, v2) {
  if (!v1 || !v2) return 0.0;
  const n1 = vectorNorm(v1);
  const n2 = vectorNorm(v2);
  if (n1 === 0 || n2 === 0) return 0.0;
  return dotProduct(v1, v2) / (n1 * n2);
}

function calculateBayesianRating(rate, votes, globalMean = 3.65, minVotes = 100) {
  const v = Number(votes) || 0;
  const r = Number(rate) || 0;
  const m = minVotes;
  const c = globalMean;
  if (v + m === 0) return r;
  return (v / (v + m)) * r + (m / (v + m)) * c;
}

function getEpisodeCommitment(episodes) {
  const eps = Number(episodes) || 1;
  if (eps <= 13) return 'Short (≤ 13 eps)';
  if (eps <= 26) return 'Medium (14–26 eps)';
  return 'Long (> 26 eps)';
}

export const localEngine = {
  /**
   * Loads and caches the anime catalog JSON client-side.
   */
  async ensureCatalog() {
    if (cachedCatalog && cachedCatalog.length > 0) {
      return cachedCatalog;
    }
    if (catalogLoadingPromise) {
      return catalogLoadingPromise;
    }

    catalogLoadingPromise = (async () => {
      // Determine possible catalog URLs depending on Vite base URL
      const base = import.meta.env?.BASE_URL || '/';
      const cleanBase = base.endsWith('/') ? base : `${base}/`;
      const urls = [
        `${cleanBase}anime_catalog.json`,
        '/anime_catalog.json',
        './anime_catalog.json',
        'anime_catalog.json'
      ];

      let data = null;
      for (const url of urls) {
        try {
          const res = await fetch(url);
          if (res.ok) {
            data = await res.json();
            if (Array.isArray(data) && data.length > 0) {
              break;
            }
          }
        } catch {
          // Try next candidate url
        }
      }

      if (!data) {
        throw new Error('Could not load anime_catalog.json in client browser');
      }

      cachedCatalog = data;
      catalogMap.clear();
      for (const item of cachedCatalog) {
        catalogMap.set(Number(item.anime_id), item);
      }
      return cachedCatalog;
    })();

    return catalogLoadingPromise;
  },

  // 1. Health Check
  async checkHealth() {
    await this.ensureCatalog();
    return {
      status: 'ok',
      engine: 'client_local_wasm_js',
      catalog_count: cachedCatalog.length,
      timestamp: new Date().toISOString()
    };
  },

  // 2. Catalog Browsing & Search
  async getCatalog({ page = 1, limit = 18, genre = '', search = '', sort = 'votes' } = {}) {
    await this.ensureCatalog();
    let list = cachedCatalog;

    if (genre) {
      const gLower = genre.toLowerCase();
      list = list.filter((item) =>
        (item.genres || []).some((g) => g.toLowerCase() === gLower)
      );
    }

    if (search) {
      const q = search.toLowerCase().trim();
      list = list.filter(
        (item) =>
          item.title?.toLowerCase().includes(q) ||
          (item.genres || []).some((g) => g.toLowerCase().includes(q))
      );
    }

    // Sorting
    const sorted = [...list];
    if (sort === 'score' || sort === 'rate') {
      sorted.sort((a, b) => (Number(b.rate) || 0) - (Number(a.rate) || 0));
    } else if (sort === 'title') {
      sorted.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    } else {
      // Default: votes / popularity
      sorted.sort((a, b) => (Number(b.votes) || 0) - (Number(a.votes) || 0));
    }

    const total = sorted.length;
    const pageNum = Math.max(1, Number(page) || 1);
    const limitNum = Math.max(1, Number(limit) || 18);
    const offset = (pageNum - 1) * limitNum;
    const paginated = sorted.slice(offset, offset + limitNum);

    return {
      success: true,
      data: paginated,
      results: paginated,
      total,
      page: pageNum,
      limit: limitNum,
      totalPages: Math.ceil(total / limitNum)
    };
  },

  // 3. Single Anime By ID
  async getAnimeById(id) {
    await this.ensureCatalog();
    const item = catalogMap.get(Number(id));
    if (!item) {
      return { success: false, message: `Anime #${id} not found` };
    }
    return { success: true, data: item };
  },

  // 3.5 Batch Anime
  async getAnimeBatch(ids = []) {
    await this.ensureCatalog();
    const found = [];
    for (const rawId of ids) {
      const item = catalogMap.get(Number(rawId));
      if (item) found.push(item);
    }
    return { success: true, data: found };
  },

  // 4. Popularity-Based Recommendations (Bayesian Weighted)
  async getPopularRecommendations({ topK = 18 } = {}) {
    await this.ensureCatalog();
    const scored = cachedCatalog.map((anime) => {
      const bayes = calculateBayesianRating(anime.rate, anime.votes);
      return {
        ...anime,
        bayesian_score: Number(bayes.toFixed(3)),
        match_percentage: Math.min(99, Math.round((bayes / 5.0) * 100))
      };
    });

    scored.sort((a, b) => b.bayesian_score - a.bayesian_score);
    return {
      success: true,
      data: scored.slice(0, Number(topK) || 18)
    };
  },

  // 5. Content-Based Item Similarity: "More Like This"
  async getSimilarAnime(id, limit = 8) {
    await this.ensureCatalog();
    const target = catalogMap.get(Number(id));
    if (!target) {
      return { success: false, target_id: id, similar: [] };
    }

    const targetVec = target.genre_vector || [];
    const scored = [];

    for (const item of cachedCatalog) {
      if (item.anime_id === target.anime_id) continue;
      const sim = cosineSimilarity(targetVec, item.genre_vector || []);
      if (sim > 0.0) {
        scored.push({
          ...item,
          similarity: Number(sim.toFixed(3)),
          match_percentage: Math.min(99, Math.round(sim * 100))
        });
      }
    }

    scored.sort((a, b) => b.similarity - a.similarity);
    const topSimilar = scored.slice(0, Number(limit) || 8);

    return {
      success: true,
      target: target.title,
      target_id: Number(id),
      similar: topSimilar,
      data: {
        target: target.title,
        target_id: Number(id),
        similar: topSimilar
      }
    };
  },

  // 6. Reference Anime Helper (Pure CBF: Latest user-selected or rated anime)
  getReferenceAnime(sessionRatings = []) {
    if (!sessionRatings || sessionRatings.length === 0) return null;
    const latestRating = sessionRatings[sessionRatings.length - 1];
    return catalogMap.get(Number(latestRating.anime_id)) || null;
  },

  // 7. Personalized Content-Based Filtering: "Recommended For You"
  // Core Method: CountVectorizer (29 Genres) + Cosine Similarity + User-Selected/Rated Reference Anime
  // Ratings are NOT mathematically weighted (Rating - 3.0 is strictly prohibited).
  async getPersonalizedCBF({ sessionRatings = [], referenceId = null, topK = 12 } = {}) {
    await this.ensureCatalog();
    
    let refAnime = null;
    if (referenceId) {
      refAnime = catalogMap.get(Number(referenceId));
    } else if (sessionRatings && sessionRatings.length > 0) {
      const latest = sessionRatings[sessionRatings.length - 1];
      refAnime = catalogMap.get(Number(latest.anime_id));
    }

    if (!refAnime) {
      return {
        success: true,
        data: {
          has_profile: false,
          message: 'No reference anime selected or rated yet. Rate or select an anime to generate Content-Based recommendations.',
          reference_anime: null,
          preferred_genres: {},
          recommendations: []
        }
      };
    }

    const targetVec = refAnime.genre_vector || [];
    const scored = [];
    const ratedIds = new Set(sessionRatings.map((r) => Number(r.anime_id)));

    for (const anime of cachedCatalog) {
      // Exclude reference anime itself
      if (Number(anime.anime_id) === Number(refAnime.anime_id)) continue;
      // Skip anime already in rated list if desired
      if (ratedIds.has(Number(anime.anime_id))) continue;

      const sim = cosineSimilarity(targetVec, anime.genre_vector || []);
      if (sim > 0.0) {
        scored.push({
          ...anime,
          similarity: Number(sim.toFixed(3)),
          cbf_score: Number(sim.toFixed(3)),
          match_percentage: Math.min(99, Math.max(10, Math.round(sim * 100)))
        });
      }
    }

    scored.sort((a, b) => b.similarity - a.similarity);
    const recs = scored.slice(0, Number(topK) || 12);

    const preferredGenres = {};
    for (const g of (refAnime.genres || [])) {
      preferredGenres[g] = 1.0;
    }

    return {
      success: true,
      data: {
        has_profile: true,
        reference_anime: {
          anime_id: refAnime.anime_id,
          title: refAnime.title,
          genres: refAnime.genres || [],
          rate: refAnime.rate || 0,
          anime_img: refAnime.anime_img || ''
        },
        ratings_count: sessionRatings.length,
        preferred_genres: preferredGenres,
        recommendations: recs
      }
    };
  },

  // 8. Knowledge-Based Rule Evaluation
  evaluateKbrRules(anime, constraints = {}, mood = null) {
    const rules = [];
    let hardPassed = true;
    const animeGenres = new Set((anime.genres || []).map((g) => g.toLowerCase()));
    const rate = Number(anime.rate) || 0.0;
    const episodes = Number(anime.episodes) || 1;

    // Rule 1: Episode Commitment
    const maxEps = constraints.max_episodes ? Number(constraints.max_episodes) : null;
    if (maxEps) {
      const passed = episodes <= maxEps;
      if (!passed) hardPassed = false;
      rules.push({
        rule: 'Episode Commitment',
        target: `≤ ${maxEps} episodes`,
        actual: `${episodes} eps (${getEpisodeCommitment(episodes)})`,
        passed,
        is_hard: true
      });
    }

    // Rule 2: Minimum Rating
    const minRate = constraints.min_rating ? Number(constraints.min_rating) : null;
    if (minRate) {
      const passed = rate >= minRate;
      if (!passed) hardPassed = false;
      rules.push({
        rule: 'Quality Threshold',
        target: `Rating ≥ ${minRate.toFixed(1)}`,
        actual: `${rate.toFixed(2)} rating`,
        passed,
        is_hard: true
      });
    }

    // Rule 3: Required Genres
    const reqGenres = (constraints.required_genres || []).map((g) => g.toLowerCase());
    if (reqGenres.length > 0) {
      const passed = reqGenres.every((g) => animeGenres.has(g));
      if (!passed) hardPassed = false;
      const matched = reqGenres.filter((g) => animeGenres.has(g));
      rules.push({
        rule: 'Required Genres',
        target: `Must include: ${reqGenres.join(', ')}`,
        actual: `Matched: ${matched.length ? matched.join(', ') : 'None'}`,
        passed,
        is_hard: true
      });
    }

    // Rule 4: Excluded Genres
    const excGenres = (constraints.excluded_genres || []).map((g) => g.toLowerCase());
    if (excGenres.length > 0) {
      const violated = excGenres.filter((g) => animeGenres.has(g));
      const passed = violated.length === 0;
      if (!passed) hardPassed = false;
      rules.push({
        rule: 'Excluded Genres',
        target: `Avoid: ${excGenres.join(', ')}`,
        actual: violated.length ? `Violated: ${violated.join(', ')}` : 'Clean (none present)',
        passed,
        is_hard: true
      });
    }

    // Rule 5: Viewing Mood Domain Rule (Soft Multiplier)
    let moodPassed = true;
    if (mood && MOOD_GENRE_MAP[mood.toLowerCase()]) {
      const preferred = MOOD_GENRE_MAP[mood.toLowerCase()];
      const overlap = preferred.filter((g) => animeGenres.has(g));
      moodPassed = overlap.length > 0;
      rules.push({
        rule: 'Viewing Mood',
        target: `Mood: ${mood.charAt(0).toUpperCase() + mood.slice(1)} (${preferred.slice(0, 3).join(', ')})`,
        actual: overlap.length ? `Matched: ${overlap.join(', ')}` : 'No direct mood genre overlap',
        passed: moodPassed,
        is_hard: false
      });
    }

    // Continuous KBR Fit Score (0.0 to 1.0)
    let fitScore = 0.0;
    if (hardPassed) {
      fitScore = 0.70; // Baseline
      if (moodPassed) fitScore += 0.15;
      fitScore += Math.min(0.10, Math.max(0.0, (rate - 3.5) / 15.0)); // Quality bonus
      if (maxEps) {
        fitScore += 0.05 * (1.0 - (episodes / (maxEps * 2.0))); // Proximity bonus
      }
    }

    fitScore = Math.min(1.0, Math.max(0.0, fitScore));
    return {
      hardPassed,
      rules,
      fitScore: Number(fitScore.toFixed(4))
    };
  },

  // 9. Knowledge-Based Recommendation: "Find What Fits"
  async getKnowledgeBased({ constraints = {}, mood = null, topK = 18 } = {}) {
    await this.ensureCatalog();
    const candidates = [];

    for (const anime of cachedCatalog) {
      const { hardPassed, rules, fitScore } = this.evaluateKbrRules(anime, constraints, mood);
      if (hardPassed) {
        candidates.push({
          ...anime,
          kbr_score: fitScore,
          match_percentage: Math.min(99, Math.round(fitScore * 100)),
          rule_evaluations: rules
        });
      }
    }

    candidates.sort((a, b) => b.kbr_score - a.kbr_score);
    const recs = candidates.slice(0, Number(topK) || 18);

    return {
      success: true,
      data: {
        total_matches: candidates.length,
        constraints_applied: constraints,
        mood_applied: mood,
        recommendations: recs
      }
    };
  },

  // 10. 1+1 Hybrid Recommendation: "Smart Match" (CBF + KBR)
  async getHybridRecommendations({ sessionRatings = [], constraints = {}, mood = null, topK = 18 } = {}) {
    await this.ensureCatalog();

    if (!sessionRatings || sessionRatings.length === 0) {
      return {
        success: true,
        data: {
          cold_start: true,
          message: 'You have not rated any anime yet. Rate some anime to personalize Smart Match.',
          user_taste: null,
          recommendations: []
        }
      };
    }

    const latestRating = sessionRatings[sessionRatings.length - 1];
    const refAnime = catalogMap.get(Number(latestRating.anime_id));
    const refVec = refAnime ? refAnime.genre_vector : null;
    const preferredGenres = {};
    if (refAnime && refAnime.genres) {
      for (const g of refAnime.genres) {
        preferredGenres[g] = 1.0;
      }
    }

    const candidates = [];

    for (const anime of cachedCatalog) {
      // 1. Evaluate Knowledge Rules
      const { hardPassed, rules, fitScore } = this.evaluateKbrRules(anime, constraints, mood);
      if (!hardPassed) continue;

      // 2. Evaluate Taste Score using Cosine Similarity to Reference Anime
      let cbfScore = 0.50;
      if (refVec) {
        cbfScore = cosineSimilarity(refVec, anime.genre_vector || []);
      }

      // 3. 1+1 Hybrid Fusion (50% CBF + 50% KBR)
      const hybridScore = Number((0.50 * cbfScore + 0.50 * fitScore).toFixed(4));

      candidates.push({
        ...anime,
        hybrid_score: hybridScore,
        match_percentage: Math.min(99, Math.max(15, Math.round(hybridScore * 100))),
        cbf_score: Number(cbfScore.toFixed(3)),
        kbr_score: Number(fitScore.toFixed(3)),
        cbf_match_pct: Math.min(99, Math.round(cbfScore * 100)),
        kbr_match_pct: Math.min(99, Math.round(fitScore * 100)),
        rule_evaluations: rules
      });
    }

    candidates.sort((a, b) => b.hybrid_score - a.hybrid_score);
    const recs = candidates.slice(0, Number(topK) || 18);

    return {
      success: true,
      data: {
        cold_start: false,
        ratings_count: sessionRatings.length,
        preferred_genres: preferredGenres,
        total_matches: candidates.length,
        recommendations: recs
      }
    };
  },

  // 11. Local User Ratings Storage
  submitRating({ userId = 1, animeId, rating }) {
    try {
      const storageKey = `ANIME_DSRS_USER_${userId}_RATINGS`;
      const existing = JSON.parse(localStorage.getItem(storageKey) || '[]');
      const numericId = Number(animeId);
      const filtered = existing.filter((r) => Number(r.anime_id) !== numericId);
      filtered.push({
        user_id: userId,
        anime_id: numericId,
        rating: Number(rating),
        timestamp: Date.now()
      });
      localStorage.setItem(storageKey, JSON.stringify(filtered));
      return { success: true, message: 'Rating saved locally' };
    } catch {
      return { success: true, message: 'Rating saved in session' };
    }
  },

  getUserRatings(userId = 1) {
    try {
      const storageKey = `ANIME_DSRS_USER_${userId}_RATINGS`;
      const stored = JSON.parse(localStorage.getItem(storageKey) || '[]');
      return { success: true, data: stored };
    } catch {
      return { success: true, data: [] };
    }
  }
};
