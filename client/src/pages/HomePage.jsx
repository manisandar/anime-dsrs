import React, { useState, useEffect } from 'react';
import { Search, Filter, RefreshCw, ChevronLeft, ChevronRight, X } from 'lucide-react';
import AnimeCard from '../components/AnimeCard';
import { api } from '../services/api';

const ALL_GENRES = [
  'action', 'adventure', 'comedy', 'drama', 'fantasy', 'horror',
  'isekai', 'mecha', 'mystery', 'romance', 'sci-fi', 'shonen',
  'slice of life', 'sports', 'supernatural', 'thriller'
];

export default function HomePage({
  onSelectAnime,
  sessionRatings = [],
  onRate,
  onNavigate,
  theme
}) {
  // Popularity-based default stream
  const [popularAnime, setPopularAnime] = useState([]);
  const [loadingPopular, setLoadingPopular] = useState(true);

  // Search & Filter Box state
  const [searchQuery, setSearchQuery] = useState('');
  const [activeSearch, setActiveSearch] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');
  const [sortBy, setSortBy] = useState('votes');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [searchResults, setSearchResults] = useState([]);
  const [loadingSearch, setLoadingSearch] = useState(false);

  const isFiltering = Boolean(activeSearch.trim() || selectedGenre);

  // 1. Initial Load: Popular Right Now (Highest Average Rating from Highest Votes)
  useEffect(() => {
    setLoadingPopular(true);
    api.getPopularRecommendations({ topK: 18 })
      .then((res) => {
        if (res.success && res.data) {
          setPopularAnime(res.data);
        }
      })
      .catch((err) => console.warn('Could not load popular anime:', err))
      .finally(() => setLoadingPopular(false));
  }, []);

  // 2. Load Catalog Search / Filter Results
  const executeSearch = async (targetPage = page) => {
    setLoadingSearch(true);
    try {
      const res = await api.getCatalog({
        page: targetPage,
        limit: 18,
        genre: selectedGenre,
        search: activeSearch,
        sort: sortBy,
      });
      setSearchResults(res.results || res.data || []);
      setTotalPages(res.totalPages || 1);
      setTotalCount(res.total || 0);
    } catch (err) {
      console.warn('Catalog search error:', err);
    } finally {
      setLoadingSearch(false);
    }
  };

  useEffect(() => {
    if (isFiltering) {
      executeSearch(page);
    }
  }, [page, selectedGenre, sortBy, activeSearch]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    setActiveSearch(searchQuery);
  };

  const handleResetSearch = () => {
    setSearchQuery('');
    setActiveSearch('');
    setSelectedGenre('');
    setSortBy('votes');
    setPage(1);
  };

  return (
    <div className="home-page-container">
      {/* BROWSE CATALOG SEARCH & FILTER CONTROLS BAR */}
      <div className="glass-panel" style={{ padding: '16px 20px', marginBottom: '24px' }}>
        <form onSubmit={handleSearchSubmit} className="catalog-filters-form">
          {/* Search Input */}
          <div className="search-input-wrap">
            <Search size={15} className="search-icon" />
            <input
              type="text"
              placeholder="Search catalog by title or keyword..."
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
              value={selectedGenre}
              onChange={(e) => {
                setSelectedGenre(e.target.value);
                setPage(1);
              }}
              className="modern-select"
              id="select-catalog-genre"
            >
              <option value="">All Genres</option>
              {ALL_GENRES.map((g) => (
                <option key={g} value={g}>
                  {g.charAt(0).toUpperCase() + g.slice(1)}
                </option>
              ))}
            </select>
          </div>


          <button
            type="submit"
            className="btn-primary"
            style={{ width: 'auto', padding: '10px 20px', fontSize: '13px' }}
            id="btn-apply-home-search"
          >
            Search
          </button>

          {isFiltering && (
            <button
              type="button"
              className="btn-card-action"
              onClick={handleResetSearch}
              style={{ width: 'auto', padding: '10px 14px', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '4px' }}
              title="Reset search and show popular anime"
              id="btn-reset-home-search"
            >
              <X size={14} />
              <span>Reset</span>
            </button>
          )}
        </form>

        {isFiltering && (
          <div className="catalog-stats-row" style={{ marginTop: '12px' }}>
            <span>{totalCount.toLocaleString()} titles found • Page {page} of {totalPages}</span>
            {loadingSearch && (
              <span className="loading-tag">
                <RefreshCw size={12} className="spin" /> Searching...
              </span>
            )}
          </div>
        )}
      </div>

      {/* STREAM SECTION */}
      {isFiltering ? (
        /* CATALOG SEARCH RESULTS STREAM */
        <section className="home-stream-section">
          <div className="stream-header-row">
            <div>
              <div className="stream-category-label">Catalog Explorer</div>
              <h2 className="stream-title">
                {activeSearch ? `Results for "${activeSearch}"` : selectedGenre ? `${selectedGenre.charAt(0).toUpperCase() + selectedGenre.slice(1)} Anime` : 'Catalog Titles'}
              </h2>
              <p className="stream-subtitle">
                Filtered from the catalog database.
              </p>
            </div>
          </div>

          {loadingSearch ? (
            <div className="stream-loading-placeholder">
              <RefreshCw size={18} className="spin" />
              <span>Searching catalog...</span>
            </div>
          ) : searchResults.length === 0 ? (
            <div className="empty-state-panel glass-panel">
              <h3>No anime found matching your query</h3>
              <p>Try searching with another keyword or resetting genre filters.</p>
              <button className="btn-primary" onClick={handleResetSearch} style={{ width: 'auto', marginTop: '12px' }}>
                Show Popular Anime
              </button>
            </div>
          ) : (
            <>
              <div className="cards-grid">
                {searchResults.map((anime) => (
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
                  id="btn-home-prev"
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
                  id="btn-home-next"
                >
                  <span>Next</span>
                  <ChevronRight size={16} />
                </button>
              </div>
            </>
          )}
        </section>
      ) : (
        /* POPULAR RIGHT NOW (POPULARITY-BASED RECOMMENDATION ONLY) */
        <section className="home-stream-section">
          <div className="stream-header-row">
            <div>
              <div className="stream-category-label">Popularity-Based Recommendation</div>
              <h2 className="stream-title">Popular Right Now</h2>
              <p className="stream-subtitle">
                Top-rated anime selected from the most-voted titles across the community (highest average rating from highest votes).
              </p>
            </div>
          </div>

          {loadingPopular ? (
            <div className="stream-loading-placeholder">
              <RefreshCw size={18} className="spin" />
              <span>Loading popular titles...</span>
            </div>
          ) : (
            <div className="cards-grid">
              {popularAnime.map((anime) => (
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
          )}
        </section>
      )}
    </div>
  );
}
