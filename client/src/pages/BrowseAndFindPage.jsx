import React, { useState, useEffect } from 'react';
import { Sliders, RefreshCw, Check, ChevronLeft, ChevronRight, AlertCircle } from 'lucide-react';
import AnimeCard from '../components/AnimeCard';
import { api } from '../services/api';

const ALL_GENRES = [
  'action', 'adventure', 'comedy', 'drama', 'fantasy', 'horror',
  'isekai', 'mecha', 'mystery', 'romance', 'sci-fi', 'shonen',
  'slice of life', 'sports', 'supernatural', 'thriller'
];

export default function BrowseAndFindPage({
  onSelectAnime,
  sessionRatings = [],
  onRate
}) {
  // Constraints state (Constraint Box)
  const [maxEpisodes, setMaxEpisodes] = useState(26);
  const [minRating, setMinRating] = useState(4.0);
  const [requiredGenres, setRequiredGenres] = useState([]);

  // Results & Pagination state
  const [results, setResults] = useState([]);
  const [totalMatches, setTotalMatches] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);

  const executeHybrid = async (targetPage = page) => {
    setLoading(true);
    try {
      const response = await api.getHybridRecommendations({
        sessionRatings,
        constraints: {
          max_episodes: parseInt(maxEpisodes),
          min_rating: parseFloat(minRating),
          required_genres: requiredGenres,
        },
        page: targetPage,
        limit: 18,
      });

      if (response && response.data) {
        setResults(response.data.recommendations || response.data.results || []);
        setTotalMatches(response.data.total_matches || 0);
        setTotalPages(response.data.totalPages || 1);
      }
    } catch (err) {
      console.warn('Hybrid recommendation error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    executeHybrid(page);
  }, [page, sessionRatings]);

  const handleApplyConstraints = (e) => {
    if (e) e.preventDefault();
    setPage(1);
    executeHybrid(1);
  };

  const toggleRequiredGenre = (genre) => {
    setRequiredGenres((prev) =>
      prev.includes(genre) ? prev.filter((g) => g !== genre) : [...prev, genre]
    );
  };

  return (
    <div className="browse-find-page">
      <div className="decision-grid">
        {/* LEFT COLUMN: CONSTRAINT BOX & TASTE PROFILE */}
        <aside className="glass-panel control-panel">
          <div className="section-header">
            <span className="section-title">
              <Sliders size={16} />
              Situation Requirements
            </span>
          </div>

          {/* 1. Episode Commitment */}
          <div className="control-group">
            <div className="control-label-row">
              <span>Episode Commitment</span>
              <span className="control-value">≤ {maxEpisodes} eps</span>
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
            <div className="preset-pill-row">
              {[
                { num: 13, label: 'Short (≤ 13)' },
                { num: 26, label: 'Medium (≤ 26)' },
                { num: 50, label: 'Standard (≤ 50)' },
                { num: 100, label: 'Any' },
              ].map((preset) => (
                <button
                  key={preset.num}
                  type="button"
                  className={`pill-btn ${maxEpisodes === preset.num ? 'active' : ''}`}
                  onClick={() => setMaxEpisodes(preset.num)}
                >
                  {preset.label}
                </button>
              ))}
            </div>
          </div>

          {/* 2. Minimum Rating */}
          <div className="control-group">
            <div className="control-label-row">
              <span>Minimum Quality</span>
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

          {/* 3. Must Include Genres */}
          <div className="control-group">
            <div className="control-label-row">
              <span>Must Include Genres</span>
              {requiredGenres.length > 0 && (
                <span className="count-badge">{requiredGenres.length} selected</span>
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

          {/* Update Recommendations Button */}
          <button
            className="btn-primary"
            onClick={handleApplyConstraints}
            disabled={loading}
            id="btn-execute-hybrid"
          >
            {loading ? <RefreshCw size={15} className="spin" /> : <Sliders size={15} />}
            <span>{loading ? 'Solving Constraints...' : 'Update Recommendations'}</span>
          </button>

        </aside>

        {/* RIGHT COLUMN: HYBRID RECOMMENDATION RESULTS */}
        <main className="results-container">

          {loading ? (
            <div className="stream-loading-placeholder">
              <RefreshCw size={20} className="spin" />
              <span>Evaluating 70/40 Hybrid Recommendations...</span>
            </div>
          ) : results.length === 0 ? (
            <div className="empty-state-panel glass-panel">
              <AlertCircle size={24} />
              <h3>No matches found</h3>
              <p>Try easing your minimum rating or episode constraints to widen the solution space.</p>
            </div>
          ) : (
            <>
              <div className="cards-grid">
                {results.map((anime) => (
                  <AnimeCard
                    key={anime.anime_id}
                    anime={anime}
                    onClick={() => onSelectAnime && onSelectAnime(anime)}
                    onRate={onRate}
                    userRating={(sessionRatings.find((r) => r.anime_id === anime.anime_id)?.rating) || 0}
                    showAttribution={false}
                    showMatchBadge={false}
                  />
                ))}
              </div>

              {/* Pagination Controls */}
              <div className="pagination-controls" style={{ marginTop: '28px' }}>
                <button
                  className="btn-card-action"
                  disabled={page <= 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  id="btn-hybrid-prev"
                >
                  <ChevronLeft size={16} />
                  <span>Previous</span>
                </button>

                <span className="page-indicator">
                  {page} / {totalPages}
                </span>

                <button
                  className="btn-card-action"
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  id="btn-hybrid-next"
                >
                  <span>Next</span>
                  <ChevronRight size={16} />
                </button>
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
}
