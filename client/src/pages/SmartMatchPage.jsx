import React, { useState, useEffect } from 'react';
import { Sliders, Sparkles, Star, Check, ArrowRight, Compass, RefreshCw, AlertCircle, Info } from 'lucide-react';
import AnimeCard from '../components/AnimeCard';
import { api } from '../services/api';

const ALL_GENRES = [
  'action', 'adventure', 'comedy', 'drama', 'fantasy', 'horror',
  'isekai', 'mecha', 'mystery', 'romance', 'sci-fi', 'shonen',
  'slice of life', 'sports', 'supernatural', 'thriller'
];

const MOODS = [
  { id: 'exciting', label: 'Exciting', desc: 'Action, Shonen, Tournament' },
  { id: 'chill', label: 'Chill', desc: 'Slice of Life, Comedy, Romance' },
  { id: 'dark', label: 'Dark', desc: 'Psychological, Thriller, Mystery' },
  { id: 'emotional', label: 'Emotional', desc: 'Drama, Romance' },
];

export default function SmartMatchPage({
  onSelectAnime,
  sessionRatings = [],
  onRate,
  onNavigate
}) {
  // Situation Constraints
  const [maxEpisodes, setMaxEpisodes] = useState(50);
  const [minRating, setMinRating] = useState(3.8);
  const [requiredGenres, setRequiredGenres] = useState([]);
  const [excludedGenres, setExcludedGenres] = useState([]);
  const [selectedMood, setSelectedMood] = useState('exciting');

  // Hybrid Data State
  const [hybridResults, setHybridResults] = useState([]);
  const [userTasteProfile, setUserTasteProfile] = useState(null);
  const [totalMatches, setTotalMatches] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Compute Hybrid Recommendations
  const executeHybridMatch = async () => {
    if (sessionRatings.length === 0) return;

    setLoading(true);
    setError(null);

    try {
      const response = await api.getHybridRecommendations({
        sessionRatings,
        constraints: {
          max_episodes: parseInt(maxEpisodes),
          min_rating: parseFloat(minRating),
          required_genres: requiredGenres,
          excluded_genres: excludedGenres,
        },
        mood: selectedMood,
        topK: 18,
      });

      if (response.success && response.data) {
        setHybridResults(response.data.recommendations || []);
        setUserTasteProfile(response.data.preferred_genres || null);
        setTotalMatches(response.data.total_matches || 0);
      }
    } catch (err) {
      console.warn('Hybrid execution error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Run automatically when ratings or constraints change
  useEffect(() => {
    if (sessionRatings.length > 0) {
      executeHybridMatch();
    }
  }, [sessionRatings]);

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

  // =========================================================================
  // COLD-START CASE: USER HAS ZERO RATINGS
  // =========================================================================
  if (sessionRatings.length === 0) {
    return (
      <div className="smart-match-cold-start glass-panel">
        <div className="cold-start-content-box">
          <div className="cold-start-icon-badge">
            <Sliders size={28} />
          </div>

          <h2 className="cold-start-heading">Personalize Smart Match</h2>
          
          <p className="cold-start-text">
            Smart Match is a <strong>1+1 Hybrid Recommender</strong> combining your Content-Based taste profile (50%) with situational requirements (50%). Because you have not rated any anime yet, an authentic taste profile cannot be computed.
          </p>

          <div className="cold-start-actions-row">
            <button
              className="btn-primary"
              onClick={() => onNavigate('browse_find')}
              id="btn-cold-start-rate"
            >
              <Star size={15} />
              <span>Start Rating in Catalog</span>
            </button>

            <button
              className="btn-secondary"
              onClick={() => onNavigate('browse_find', { mode: 'kbr' })}
              id="btn-cold-start-kbr"
            >
              <Compass size={15} />
              <span>Continue with Requirements Only</span>
            </button>
          </div>

          <div className="cold-start-footnote">
            <Info size={14} />
            <span>Rating as few as 1 or 2 anime will immediately unlock your personalized 1+1 Hybrid feed.</span>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // ACTIVE USER: 1+1 HYBRID RECOMMENDATION FEED
  // =========================================================================
  return (
    <div className="smart-match-page">
      <div className="decision-grid">
        {/* LEFT COLUMN: TASTE PROFILE SUMMARY + CURRENT REQUIREMENTS FORM */}
        <aside className="glass-panel control-panel">
          {/* SECTION 1: TASTE PROFILE (CONTENT-BASED) */}
          <div className="taste-profile-panel">
            <div className="section-header">
              <span className="section-title">
                <Sparkles size={16} />
                Your Taste Profile (CBF)
              </span>
            </div>
            <p className="panel-hint">
              Learned from your {sessionRatings.length} in-session ratings.
            </p>

            {userTasteProfile && Object.keys(userTasteProfile).length > 0 ? (
              <div className="taste-breakdown-list">
                {Object.entries(userTasteProfile).slice(0, 5).map(([genre, score]) => (
                  <div key={genre} className="taste-bar-item">
                    <div className="taste-bar-label">
                      <span>{genre}</span>
                      <span>{score} pts</span>
                    </div>
                    <div className="taste-track">
                      <div
                        className="taste-fill"
                        style={{ width: `${Math.min(100, Math.round((score / 6.0) * 100))}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="taste-pending-note">
                Taste profile vector is active. Rate more anime to increase genre specificity.
              </div>
            )}
          </div>

          <div className="panel-divider" />

          {/* SECTION 2: SITUATION REQUIREMENTS (KNOWLEDGE-BASED) */}
          <div className="situation-requirements-panel">
            <div className="section-header">
              <span className="section-title">
                <Sliders size={16} />
                What Do You Want Right Now? (KBR)
              </span>
            </div>

            {/* Episode Limit */}
            <div className="control-group">
              <div className="control-label-row">
                <span>Max Episodes</span>
                <span className="control-value">≤ {maxEpisodes} eps</span>
              </div>
              <input
                type="range"
                min="6"
                max="100"
                step="2"
                value={maxEpisodes}
                onChange={(e) => setMaxEpisodes(e.target.value)}
              />
              <div className="preset-pill-row">
                {[12, 26, 50, 100].map((num) => (
                  <button
                    key={num}
                    type="button"
                    className={`pill-btn ${maxEpisodes === num ? 'active' : ''}`}
                    onClick={() => setMaxEpisodes(num)}
                  >
                    {num === 100 ? 'Any' : `${num} eps`}
                  </button>
                ))}
              </div>
            </div>

            {/* Minimum Quality */}
            <div className="control-group">
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
              />
            </div>

            {/* Viewing Mood */}
            <div className="control-group">
              <div className="control-label-row">
                <span>Viewing Mood</span>
              </div>
              <div className="mood-select-grid">
                {MOODS.map((m) => (
                  <button
                    key={m.id}
                    type="button"
                    className={`mood-card-btn ${selectedMood === m.id ? 'active' : ''}`}
                    onClick={() => setSelectedMood(m.id)}
                  >
                    <div className="mood-title">{m.label}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Must Include Genres */}
            <div className="control-group">
              <div className="control-label-row">
                <span>Must Include</span>
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

            {/* Avoid Genres */}
            <div className="control-group">
              <div className="control-label-row">
                <span>Avoid</span>
                {excludedGenres.length > 0 && (
                  <span className="count-badge-danger">{excludedGenres.length} avoided</span>
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

            <button
              className="btn-primary"
              onClick={executeHybridMatch}
              disabled={loading}
              id="btn-compute-smart-match"
            >
              {loading ? <RefreshCw size={15} className="spin" /> : <Sliders size={15} />}
              <span>{loading ? 'Synthesizing 1+1 Hybrid...' : 'Generate Smart Match'}</span>
            </button>
          </div>
        </aside>

        {/* RIGHT COLUMN: 1+1 HYBRID RESULTS FEED */}
        <main className="results-container">
          <div className="results-header-banner">
            <div>
              <h2 style={{ fontSize: '18px', fontWeight: 700 }}>
                1+1 Hybrid Match Results
              </h2>
              <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                50% Personal Taste (Content-Based) + 50% Requirement Fit (Knowledge-Based)
              </p>
            </div>

            <div className="results-badge">
              <Sliders size={13} />
              <span>{totalMatches} Total Matches</span>
            </div>
          </div>

          {error && (
            <div className="error-banner">
              <AlertCircle size={18} />
              <span>Service note: {error}. Check backend server on port 5001.</span>
            </div>
          )}

          {loading ? (
            <div className="stream-loading-placeholder">
              <RefreshCw size={20} className="spin" />
              <span>Synthesizing hybrid match scores...</span>
            </div>
          ) : hybridResults.length === 0 ? (
            <div className="empty-state-panel glass-panel">
              <AlertCircle size={24} />
              <h3>No hybrid candidates found</h3>
              <p>Try easing your episode length or rating requirements to match more titles from your taste profile.</p>
            </div>
          ) : (
            <div className="cards-grid">
              {hybridResults.map((anime) => (
                <AnimeCard
                  key={anime.anime_id}
                  anime={anime}
                  onClick={() => onSelectAnime && onSelectAnime(anime)}
                  onRate={onRate}
                  userRating={(sessionRatings.find((r) => r.anime_id === anime.anime_id)?.rating) || 0}
                  showAttribution={true}
                  showRules={true}
                />
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
