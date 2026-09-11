import React, { useState, useEffect } from 'react';
import { Search, Filter, ArrowUpDown, ChevronLeft, ChevronRight, Sliders, RefreshCw, Check, Compass, AlertCircle } from 'lucide-react';
import AnimeCard from '../components/AnimeCard';
import { api } from '../services/api';

const ALL_GENRES = [
  'action', 'adventure', 'comedy', 'drama', 'fantasy', 'horror',
  'isekai', 'mecha', 'mystery', 'romance', 'sci-fi', 'shonen',
  'slice of life', 'sports', 'supernatural', 'thriller'
];

const MOODS = [
  { id: 'exciting', label: 'Exciting', desc: 'Action, Shonen, Tournament, Super Power' },
  { id: 'chill', label: 'Chill', desc: 'Slice of Life, Comedy, Romance' },
  { id: 'dark', label: 'Dark', desc: 'Psychological, Thriller, Horror, Mystery' },
  { id: 'emotional', label: 'Emotional', desc: 'Drama, Romance, Slice of Life' },
];

export default function BrowseAndFindPage({ onSelectAnime, sessionRatings = [], onRate, initialMode = 'browse' }) {
  const [activeMode, setActiveMode] = useState(initialMode); // 'browse' | 'kbr'

  // --- BROWSE MODE STATE ---
  const [catalogList, setCatalogList] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [browseGenre, setBrowseGenre] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('votes');
  const [loadingBrowse, setLoadingBrowse] = useState(false);

  // --- KBR MODE STATE ---
  const [maxEpisodes, setMaxEpisodes] = useState(26);
  const [minRating, setMinRating] = useState(4.0);
  const [requiredGenres, setRequiredGenres] = useState([]);
  const [excludedGenres, setExcludedGenres] = useState([]);
  const [selectedMood, setSelectedMood] = useState('exciting');
  const [kbrResults, setKbrResults] = useState([]);
  const [kbrTotalMatches, setKbrTotalMatches] = useState(0);
  const [loadingKbr, setLoadingKbr] = useState(false);
  const [kbrSearched, setKbrSearched] = useState(false);

  // 1. Fetch Catalog for Browse Mode
  const loadCatalog = async () => {
    setLoadingBrowse(true);
    try {
      const data = await api.getCatalog({
        page,
        limit: 18,
        genre: browseGenre,
        search: searchQuery,
        sort: sortBy,
      });
      setCatalogList(data.results || []);
      setTotalPages(data.totalPages || 1);
      setTotalCount(data.total || 0);
    } catch (err) {
      console.warn('Failed to load catalog:', err);
    } finally {
      setLoadingBrowse(false);
    }
  };

  useEffect(() => {
    if (activeMode === 'browse') {
      loadCatalog();
    }
  }, [page, browseGenre, sortBy, activeMode]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    loadCatalog();
  };

  // 2. Fetch Knowledge-Based Recommendations
  const executeKBR = async () => {
    setLoadingKbr(true);
    setKbrSearched(true);
    try {
      const response = await api.getKnowledgeBased({
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
        setKbrResults(response.data.recommendations || []);
        setKbrTotalMatches(response.data.total_matches || 0);
      }
    } catch (err) {
      console.warn('KBR execution error:', err);
    } finally {
      setLoadingKbr(false);
    }
  };

  // Run initial KBR if switching into KBR mode for the first time
  useEffect(() => {
    if (activeMode === 'kbr' && !kbrSearched) {
      executeKBR();
    }
  }, [activeMode]);

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

  return (
    <div className="browse-find-page">
      {/* MODE SELECTOR HEADER */}
      <div className="mode-toggle-bar glass-panel">
        <div className="mode-tabs">
          <button
            type="button"
            className={`mode-tab-btn ${activeMode === 'browse' ? 'active' : ''}`}
            onClick={() => setActiveMode('browse')}
            id="tab-browse-catalog"
          >
            <Compass size={16} />
            <span>Browse Catalog</span>
          </button>

          <button
            type="button"
            className={`mode-tab-btn ${activeMode === 'kbr' ? 'active' : ''}`}
            onClick={() => setActiveMode('kbr')}
            id="tab-find-what-fits"
          >
            <Sliders size={16} />
            <span>Find What Fits (Knowledge-Based)</span>
          </button>
        </div>

        <div className="mode-desc">
          {activeMode === 'browse'
            ? 'Standard catalog exploration, searching, and sorting.'
            : 'Explicit situation-specific constraint solving & domain rule evaluation.'}
        </div>
      </div>

      {/* ========================================================= */}
      {/* MODE 1: BROWSE CATALOG                                    */}
      {/* ========================================================= */}
      {activeMode === 'browse' && (
        <section className="browse-section">
          {/* Controls Bar */}
          <div className="glass-panel" style={{ padding: '16px 20px', marginBottom: '24px' }}>
            <form onSubmit={handleSearchSubmit} className="catalog-filters-form">
              {/* Search Input */}
              <div className="search-input-wrap">
                <Search size={15} className="search-icon" />
                <input
                  type="text"
                  placeholder="Search catalog by title..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="modern-input"
                  id="input-catalog-search"
                />
              </div>

              {/* Genre Selector */}
              <div className="filter-select-wrap">
                <Filter size={14} />
                <select
                  value={browseGenre}
                  onChange={(e) => { setBrowseGenre(e.target.value); setPage(1); }}
                  className="modern-select"
                  id="select-catalog-genre"
                >
                  <option value="">All Genres</option>
                  {ALL_GENRES.map((g) => (
                    <option key={g} value={g}>{g.charAt(0).toUpperCase() + g.slice(1)}</option>
                  ))}
                </select>
              </div>

              {/* Sort Order */}
              <div className="filter-select-wrap">
                <ArrowUpDown size={14} />
                <select
                  value={sortBy}
                  onChange={(e) => { setSortBy(e.target.value); setPage(1); }}
                  className="modern-select"
                  id="select-catalog-sort"
                >
                  <option value="votes">Most Popular (Votes)</option>
                  <option value="rate">Highest Rated</option>
                  <option value="episodes">Episode Count</option>
                </select>
              </div>

              <button
                type="submit"
                className="btn-primary"
                style={{ width: 'auto', padding: '10px 20px', fontSize: '13px' }}
              >
                Apply
              </button>
            </form>

            <div className="catalog-stats-row">
              <span>{totalCount.toLocaleString()} titles available • Page {page} of {totalPages}</span>
              {loadingBrowse && (
                <span className="loading-tag">
                  <RefreshCw size={12} className="spin" /> Updating...
                </span>
              )}
            </div>
          </div>

          {/* Cards Grid */}
          <div className="cards-grid">
            {catalogList.map((anime) => (
              <AnimeCard
                key={anime.anime_id}
                anime={anime}
                onClick={() => onSelectAnime && onSelectAnime(anime)}
                onRate={onRate}
                userRating={(sessionRatings.find((r) => r.anime_id === anime.anime_id)?.rating) || 0}
                showAttribution={false}
              />
            ))}
          </div>

          {/* Pagination */}
          <div className="pagination-controls">
            <button
              className="btn-card-action"
              disabled={page <= 1}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              id="btn-pagination-prev"
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
              id="btn-pagination-next"
            >
              <span>Next</span>
              <ChevronRight size={16} />
            </button>
          </div>
        </section>
      )}

      {/* ========================================================= */}
      {/* MODE 2: FIND WHAT FITS (KNOWLEDGE-BASED RECOMMENDATION)   */}
      {/* ========================================================= */}
      {activeMode === 'kbr' && (
        <section className="kbr-section">
          <div className="decision-grid">
            {/* LEFT COLUMN: KBR RULE & CONSTRAINT FORM */}
            <aside className="glass-panel control-panel">
              <div className="section-header">
                <span className="section-title">
                  <Sliders size={16} />
                  Situation Requirements
                </span>
              </div>
              <p className="panel-hint">
                Knowledge-Based Recommendation evaluates explicit domain rules and hard constraints. Zero user history required.
              </p>

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

              {/* 3. Viewing Mood */}
              <div className="control-group">
                <div className="control-label-row">
                  <span>Viewing Mood (Domain Mapping)</span>
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
                      <div className="mood-desc">{m.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* 4. Must Include Genres */}
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

              {/* 5. Avoid Genres */}
              <div className="control-group">
                <div className="control-label-row">
                  <span>Avoid Genres</span>
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
                onClick={executeKBR}
                disabled={loadingKbr}
                id="btn-execute-kbr"
              >
                {loadingKbr ? <RefreshCw size={15} className="spin" /> : <Sliders size={15} />}
                <span>{loadingKbr ? 'Solving Constraints...' : 'Find Anime'}</span>
              </button>
            </aside>

            {/* RIGHT COLUMN: KBR RESULTS STREAM WITH EXPLAINABLE ACCORDION */}
            <main className="results-container">
              <div className="results-header-banner">
                <div>
                  <h2 style={{ fontSize: '18px', fontWeight: 700 }}>
                    Knowledge-Based Recommendation
                  </h2>
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                    Ranked by constraint satisfaction and domain rule alignment.
                  </p>
                </div>

                <div className="results-badge">
                  <Sliders size={13} />
                  <span>{kbrTotalMatches} Matches</span>
                </div>
              </div>

              {loadingKbr ? (
                <div className="stream-loading-placeholder">
                  <RefreshCw size={20} className="spin" />
                  <span>Evaluating knowledge-based rules...</span>
                </div>
              ) : kbrResults.length === 0 ? (
                <div className="empty-state-panel glass-panel">
                  <AlertCircle size={24} />
                  <h3>No matches found</h3>
                  <p>Try easing your minimum rating or episode constraints to widen the solution space.</p>
                </div>
              ) : (
                <div className="cards-grid">
                  {kbrResults.map((anime) => (
                    <AnimeCard
                      key={anime.anime_id}
                      anime={anime}
                      onClick={() => onSelectAnime && onSelectAnime(anime)}
                      onRate={onRate}
                      userRating={(sessionRatings.find((r) => r.anime_id === anime.anime_id)?.rating) || 0}
                      showAttribution={false}
                      showRules={true}
                    />
                  ))}
                </div>
              )}
            </main>
          </div>
        </section>
      )}
    </div>
  );
}
