import React, { useState, useEffect } from 'react';
import { Filter, Clock, Sparkles, RefreshCw, AlertCircle, Check, Compass, X } from 'lucide-react';
import AnimeCard from '../components/AnimeCard';
import { api } from '../services/api';

const ALL_GENRES = [
  'action', 'adventure', 'comedy', 'drama', 'fantasy', 'horror',
  'isekai', 'mecha', 'mystery', 'romance', 'sci-fi', 'shonen',
  'slice of life', 'sports', 'supernatural', 'thriller'
];

export default function DecisionCenter({ onSelectAnime, sessionRatings = [], onRate }) {
  // Anchor Anime for Content-Based Taste Matching
  const [anchorId, setAnchorId] = useState('');
  const [popularAnchors, setPopularAnchors] = useState([]);

  // Decision Constraints for Knowledge-Based Matching
  const [maxEpisodes, setMaxEpisodes] = useState(50);
  const [minRating, setMinRating] = useState(3.5);
  const [requiredGenres, setRequiredGenres] = useState([]);
  const [excludedGenres, setExcludedGenres] = useState([]);
  const [context, setContext] = useState('evening_chill');

  const [recommendations, setRecommendations] = useState([]);
  const [engineMeta, setEngineMeta] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load anchor anime suggestions
  useEffect(() => {
    api.getPopularAnchors()
      .then((data) => {
        if (data.anchors) setPopularAnchors(data.anchors);
      })
      .catch((err) => console.warn('Could not load anchors:', err));
  }, []);

  // Compute recommendations
  const computeRecommendations = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.getHybridRecommendations({
        anchorAnimeId: anchorId ? parseInt(anchorId) : null,
        sessionRatings: sessionRatings,
        constraints: {
          max_episodes: parseInt(maxEpisodes),
          min_rating: parseFloat(minRating),
          required_genres: requiredGenres,
          excluded_genres: excludedGenres,
        },
        context: context,
        topK: 12,
      });

      if (response.success && response.data) {
        setRecommendations(response.data.recommendations || []);
        setEngineMeta(response.data);
      } else {
        throw new Error('Failed to generate recommendations');
      }
    } catch (err) {
      console.error('Recommender error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Re-run whenever anchor or context changes
  useEffect(() => {
    computeRecommendations();
  }, [anchorId, context]);

  const toggleRequiredGenre = (genre) => {
    setExcludedGenres((prev) => prev.filter((g) => g !== genre));
    setRequiredGenres((prev) =>
      prev.includes(genre) ? prev.filter((g) => g !== genre) : [...prev, genre]
    );
  };

  const toggleExcludedGenre = (genre) => {
    setRequiredGenres((prev) => prev.filter((g) => g !== genre));
    setExcludedGenres((prev) =>
      prev.includes(genre) ? prev.filter((g) => g !== genre) : [...prev, genre]
    );
  };

  const selectedAnchorObj = popularAnchors.find((a) => a.anime_id === parseInt(anchorId));

  return (
    <div className="decision-grid">
      {/* LEFT COLUMN: ANCHOR + CONSTRAINT CONTROLS */}
      <aside className="glass-panel control-panel">
        {/* SECTION 1: ANCHOR ANIME (CONTENT-BASED TASTE MATCH) */}
        <div>
          <div className="section-header">
            <span className="section-title">
              <Sparkles size={16} color="var(--accent-red)" />
              1. Taste Anchor (Similar To)
            </span>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '10px' }}>
            Pick an anime you love to find titles with matching genres & storytelling:
          </p>

          <select
            value={anchorId}
            onChange={(e) => setAnchorId(e.target.value)}
            className="modern-select"
            id="select-anchor-anime"
          >
            <option value="">None (Recommend by filters only)</option>
            {popularAnchors.map((a) => (
              <option key={a.anime_id} value={a.anime_id}>
                {a.title} ({a.genres?.slice(0, 2).join(', ') || 'Anime'})
              </option>
            ))}
          </select>

          {/* Quick Anchor Chips */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '10px' }}>
            {popularAnchors.slice(0, 5).map((a) => (
              <button
                key={a.anime_id}
                type="button"
                className={`pill-btn ${anchorId === String(a.anime_id) ? 'active' : ''}`}
                onClick={() => setAnchorId(anchorId === String(a.anime_id) ? '' : String(a.anime_id))}
                style={{ fontSize: '11px' }}
              >
                {a.title.split(' ')[0]}
              </button>
            ))}
          </div>

          {selectedAnchorObj && (
            <div className="selected-anchor-badge">
              <span>Matching taste of: <strong>{selectedAnchorObj.title}</strong></span>
              <button onClick={() => setAnchorId('')} className="clear-anchor-btn" title="Clear Anchor">
                <X size={12} />
              </button>
            </div>
          )}
        </div>

        {/* SECTION 2: HARD CONSTRAINTS (KNOWLEDGE-BASED MATCH) */}
        <div>
          <div className="section-header">
            <span className="section-title">
              <Filter size={16} color="var(--accent-cyan)" />
              2. Decision Constraints
            </span>
          </div>

          {/* Episode Length */}
          <div className="control-group" style={{ marginBottom: '18px' }}>
            <div className="control-label-row">
              <span>Max Episodes</span>
              <span className="control-value">Up to {maxEpisodes} eps</span>
            </div>
            <input
              type="range"
              min="6"
              max="100"
              step="2"
              value={maxEpisodes}
              onChange={(e) => setMaxEpisodes(e.target.value)}
              id="slider-max-episodes"
            />
            <div style={{ display: 'flex', gap: '6px', marginTop: '6px' }}>
              {[12, 26, 50, 100].map((num) => (
                <button
                  key={num}
                  type="button"
                  className={`pill-btn ${maxEpisodes === num ? 'active' : ''}`}
                  onClick={() => setMaxEpisodes(num)}
                  style={{ flex: 1, padding: '4px 0', textAlign: 'center', fontSize: '11px' }}
                >
                  {num === 100 ? 'Any' : `${num} eps`}
                </button>
              ))}
            </div>
          </div>

          {/* Minimum Rating */}
          <div className="control-group" style={{ marginBottom: '18px' }}>
            <div className="control-label-row">
              <span>Minimum Rating</span>
              <span className="control-value">{minRating} ★ & up</span>
            </div>
            <input
              type="range"
              min="2.5"
              max="4.8"
              step="0.1"
              value={minRating}
              onChange={(e) => setMinRating(e.target.value)}
              id="slider-min-rating"
            />
          </div>

          {/* Preferred Genres */}
          <div className="control-group" style={{ marginBottom: '18px' }}>
            <div className="control-label-row">
              <span>Must Include Genres</span>
              {requiredGenres.length > 0 && (
                <span style={{ fontSize: '11px', color: 'var(--accent-red)' }}>
                  {requiredGenres.length} selected
                </span>
              )}
            </div>
            <div className="genre-pills">
              {ALL_GENRES.map((g) => (
                <button
                  key={g}
                  type="button"
                  className={`pill-btn ${requiredGenres.includes(g) ? 'active' : ''}`}
                  onClick={() => toggleRequiredGenre(g)}
                >
                  {requiredGenres.includes(g) && <Check size={11} style={{ marginRight: '3px' }} />}
                  {g}
                </button>
              ))}
            </div>
          </div>

          {/* Excluded Genres */}
          <div className="control-group">
            <div className="control-label-row">
              <span>Exclude Genres</span>
              {excludedGenres.length > 0 && (
                <span style={{ fontSize: '11px', color: '#f87171' }}>
                  {excludedGenres.length} blocked
                </span>
              )}
            </div>
            <div className="genre-pills">
              {ALL_GENRES.map((g) => (
                <button
                  key={g}
                  type="button"
                  className={`pill-btn ${excludedGenres.includes(g) ? 'excluded' : ''}`}
                  onClick={() => toggleExcludedGenre(g)}
                >
                  {excludedGenres.includes(g) && <span style={{ marginRight: '3px' }}>✕</span>}
                  {g}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* SECTION 3: VIEWING MOOD */}
        <div>
          <div className="section-header">
            <span className="section-title">
              <Clock size={16} color="var(--accent-amber)" />
              3. Viewing Mood & Session
            </span>
          </div>

          <select
            value={context}
            onChange={(e) => setContext(e.target.value)}
            className="modern-select"
            id="select-context"
          >
            <option value="morning_rush">☀️ Quick Break (Light / Comedy)</option>
            <option value="lunch_break">🍱 Lunch Break (Short 1-2 eps)</option>
            <option value="evening_chill">🛋️ Evening Chill (Standard 12-24 eps)</option>
            <option value="weekend_marathon">🍿 Weekend Binge (Long Epic Story)</option>
            <option value="late_night">🌙 Late Night (Psychological / Thriller)</option>
          </select>
        </div>

        <button
          className="btn-primary"
          onClick={computeRecommendations}
          disabled={loading}
          id="btn-compute-hybrid"
        >
          {loading ? <RefreshCw size={16} className="spin" /> : <Sparkles size={16} />}
          {loading ? 'Finding Matches...' : 'Find Matches'}
        </button>
      </aside>

      {/* RIGHT COLUMN: RECOMMENDATIONS STREAM */}
      <main className="results-container">
        <div className="results-header-banner">
          <div>
            <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--text-primary)' }}>
              {selectedAnchorObj
                ? `More Like "${selectedAnchorObj.title}"`
                : 'Top Recommended Anime For You'}
            </div>
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '2px' }}>
              {selectedAnchorObj
                ? '50% Genre Taste Similarity + 50% Constraint & Mood Alignment'
                : '100% Tailored to your active episode length, rating, and genre filters'}
            </div>
          </div>

          <div className="results-badge">
            <Sparkles size={13} color="var(--accent-red)" />
            <span>{recommendations.length} Matches</span>
          </div>
        </div>

        {error && (
          <div className="error-banner">
            <AlertCircle size={18} />
            <span>Connection note: {error}. Check backend server on port 5001.</span>
          </div>
        )}

        {/* Anime Cards Grid */}
        <div className="cards-grid">
          {recommendations.map((anime) => (
            <AnimeCard
              key={anime.anime_id}
              anime={anime}
              onRate={(id, star) => onRate && onRate(id, star)}
              onClick={() => onSelectAnime && onSelectAnime(anime)}
              showAttribution={true}
            />
          ))}
        </div>
      </main>
    </div>
  );
}
