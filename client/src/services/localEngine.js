/**
 * Pure Client-Side Academic Recommender Engine for ANIVIBE.
 * CSX/ITX 4207: Decision Support and Recommendation System, Assumption University.
 * 
 * Provides 100% offline, zero-dependency, free static execution of all paradigms:
 * 1. Consensus Popularity (Highest Average Rating from Highest Votes)
 * 2. 29-Genre Cosine Similarity Content-Based Filtering
 *    - Item-to-Item ("More Like This" on Anime Detail Page)
 * 3. 70/40 Hybrid Recommendation
 *    - 70% Knowledge-Based Constraint Scoring + 40% CBR Multi-Anime Profile Match
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

function getGenreVector(anime) {
  if (anime && Array.isArray(anime.genre_vector) && anime.genre_vector.length > 0) {
    return anime.genre_vector;
  }
  const vec = new Array(GENRE_LIST.length).fill(0);
  if (anime && Array.isArray(anime.genres)) {
    const set = new Set(anime.genres.map((g) => String(g).toLowerCase().trim()));
    GENRE_LIST.forEach((g, idx) => {
      if (set.has(g.toLowerCase())) vec[idx] = 1;
    });
  }
  return vec;
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
    } else if (sort === 'episodes') {
      sorted.sort((a, b) => (Number(a.episodes) || 0) - (Number(b.episodes) || 0));
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

  // 4. Popularity-Based Recommendations: Highest Average Rating from Highest Votes (No Bayesian)
  async getPopularRecommendations({ topK = 18, poolSize = 100 } = {}) {
    await this.ensureCatalog();

    // 1. Select the pool of highest-voted anime across the community
    const highestVoted = [...cachedCatalog]
      .sort((a, b) => (Number(b.votes) || 0) - (Number(a.votes) || 0))
      .slice(0, Math.max(poolSize, Number(topK) * 4));

    // 2. From these highest-voted titles, choose the ones with highest average rating (tie-breaking by total votes)
    highestVoted.sort((a, b) => {
      const rateDiff = (Number(b.rate) || 0) - (Number(a.rate) || 0);
      if (Math.abs(rateDiff) > 0.0001) return rateDiff;
      return (Number(b.votes) || 0) - (Number(a.votes) || 0);
    });

    return {
      success: true,
      data: highestVoted.slice(0, Number(topK) || 18)
    };
  },

  // 5. Content-Based Item Similarity: "More Like This"
  // Core Method: CountVectorizer (29 Genres) + Cosine Similarity against Selected Viewing Anime
  async getSimilarAnime(id, limit = 16) {
    await this.ensureCatalog();
    const target = catalogMap.get(Number(id));
    if (!target) {
      return { success: false, target_id: id, similar: [] };
    }

    const targetVec = getGenreVector(target);
    const scored = [];

    for (const item of cachedCatalog) {
      if (Number(item.anime_id) === Number(target.anime_id)) continue;
      const sim = cosineSimilarity(targetVec, getGenreVector(item));
      if (sim > 0.0) {
        scored.push({
          ...item,
          similarity: Number(sim.toFixed(3)),
          similarity_score: Number(sim.toFixed(3)),
          match_percentage: Math.min(99, Math.round(sim * 100))
        });
      }
    }

    scored.sort((a, b) => b.similarity - a.similarity);
    const topSimilar = scored.slice(0, Number(limit) || 16);

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

  // 10. Hybrid Recommendation: Combined 70% KBR + 40% CBR Multi-Anime User Profile
  // The system uses the content vectors of all selected/rated anime to construct a single user content profile.
  // The user profile is compared with the genre vector of every anime using Cosine Similarity.
  async getHybridRecommendations({
    sessionRatings = [],
    constraints = {},
    mood = null,
    search = '',
    genre = '',
    sortBy = 'hybrid',
    page = 1,
    limit = 18,
    topK = 18
  } = {}) {
    await this.ensureCatalog();

    const dim = 29;
    const userProfileVector = new Array(dim).fill(0.0);
    let ratedCount = 0;
    const preferredGenres = {};

    if (sessionRatings && sessionRatings.length > 0) {
      for (const r of sessionRatings) {
        const anime = catalogMap.get(Number(r.anime_id));
        if (anime && anime.genre_vector) {
          ratedCount++;
          for (let i = 0; i < dim; i++) {
            userProfileVector[i] += anime.genre_vector[i] || 0.0;
          }
          if (anime.genres) {
            for (const g of anime.genres) {
              preferredGenres[g] = (preferredGenres[g] || 0) + 1;
            }
          }
        }
      }
    }

    const hasProfile = ratedCount > 0;
    const candidates = [];
    const searchLower = search ? search.toLowerCase().trim() : '';
    const genreLower = genre ? genre.toLowerCase().trim() : '';

    for (const anime of cachedCatalog) {
      // Optional text search filter
      if (searchLower) {
        const matchTitle = anime.title?.toLowerCase().includes(searchLower);
        const matchGenre = (anime.genres || []).some((g) => g.toLowerCase().includes(searchLower));
        if (!matchTitle && !matchGenre) continue;
      }

      // Optional genre category filter
      if (genreLower) {
        const hasG = (anime.genres || []).some((g) => g.toLowerCase() === genreLower);
        if (!hasG) continue;
      }

      // 1. Evaluate Knowledge-Based Rules (KBR - 70% Weight)
      const { hardPassed, rules, fitScore } = this.evaluateKbrRules(anime, constraints, mood);
      if (!hardPassed) continue;

      // 2. Evaluate Content-Based Score using Single User Profile Vector across ALL rated anime (CBR - 40% Weight)
      let cbfScore = 0.0;
      if (hasProfile) {
        cbfScore = cosineSimilarity(userProfileVector, getGenreVector(anime));
      }

      // 3. 70/40 Hybrid Fusion Score: 0.70 * KBR + 0.40 * CBR
      const hybridScore = Number((0.70 * fitScore + 0.40 * cbfScore).toFixed(4));
      const matchPercentage = Math.min(99, Math.max(15, Math.round((hybridScore / 1.10) * 100)));

      candidates.push({
        ...anime,
        hybrid_score: hybridScore,
        match_percentage: matchPercentage,
        kbr_score: Number(fitScore.toFixed(3)),
        cbf_score: Number(cbfScore.toFixed(3)),
        kbr_match_pct: Math.min(99, Math.round(fitScore * 100)),
        cbf_match_pct: hasProfile ? Math.min(99, Math.round(cbfScore * 100)) : 0,
        rule_evaluations: rules
      });
    }

    // Sorting
    if (sortBy === 'votes') {
      candidates.sort((a, b) => (Number(b.votes) || 0) - (Number(a.votes) || 0));
    } else if (sortBy === 'rate') {
      candidates.sort((a, b) => (Number(b.rate) || 0) - (Number(a.rate) || 0));
    } else if (sortBy === 'episodes') {
      candidates.sort((a, b) => (Number(a.episodes) || 0) - (Number(b.episodes) || 0));
    } else {
      // Default: hybrid match score descending
      candidates.sort((a, b) => b.hybrid_score - a.hybrid_score);
    }

    const totalMatches = candidates.length;
    const pageNum = Math.max(1, Number(page) || 1);
    const limitNum = Math.max(1, Number(limit) || Number(topK) || 18);
    const offset = (pageNum - 1) * limitNum;
    const paginated = candidates.slice(offset, offset + limitNum);

    return {
      success: true,
      data: {
        cold_start: !hasProfile,
        has_user_profile: hasProfile,
        ratings_count: ratedCount,
        preferred_genres: preferredGenres,
        total_matches: totalMatches,
        page: pageNum,
        totalPages: Math.ceil(totalMatches / limitNum) || 1,
        recommendations: paginated,
        results: paginated
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
