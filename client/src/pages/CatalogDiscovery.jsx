import React, { useState, useEffect } from 'react';
import { Search, Filter, ArrowUpDown, ChevronLeft, ChevronRight, RefreshCw } from 'lucide-react';
import AnimeCard from '../components/AnimeCard';
import { api } from '../services/api';

const GENRES_LIST = [
  '', 'action', 'adventure', 'comedy', 'drama', 'fantasy', 'horror',
  'isekai', 'mecha', 'mystery', 'romance', 'sci-fi', 'shonen',
  'slice of life', 'sports', 'supernatural', 'thriller'
];

export default function CatalogDiscovery({ onSelectAnime, activeUser }) {
  const [animeList, setAnimeList] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [genre, setGenre] = useState('');
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('votes');
  const [loading, setLoading] = useState(false);
  const [userRatings, setUserRatings] = useState({});

  const loadCatalog = async () => {
    setLoading(true);
    try {
      const data = await api.getCatalog({
        page,
        limit: 18,
        genre,
        search,
        sort: sortBy,
      });
      setAnimeList(data.results || []);
      setTotalPages(data.totalPages || 1);
      setTotalCount(data.total || 0);
    } catch (err) {
      console.warn('Failed to load catalog:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCatalog();
  }, [page, genre, sortBy]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    loadCatalog();
  };

  const handleRate = async (animeId, rating) => {
    setUserRatings((prev) => ({ ...prev, [animeId]: rating }));
    try {
      await api.submitRating({
        userId: activeUser.id || 999,
        animeId,
        rating
      });
    } catch (err) {
      console.warn('Rating submission error:', err);
    }
  };

  return (
    <div>
      {/* Search and Filters Bar */}
      <div className="glass-panel" style={{ padding: '16px 20px', marginBottom: '24px' }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'center' }}>
          {/* Search Input */}
          <div style={{ flex: '1 1 280px', position: 'relative' }}>
            <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: '12px', top: '12px' }} />
            <input
              type="text"
              placeholder="Search by title..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="modern-input"
              id="input-catalog-search"
            />
          </div>

          {/* Genre Filter */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Filter size={15} color="var(--text-muted)" />
            <select
              value={genre}
              onChange={(e) => { setGenre(e.target.value); setPage(1); }}
              className="modern-select"
              id="select-catalog-genre"
            >
              <option value="">All Genres</option>
              {GENRES_LIST.filter(Boolean).map((g) => (
                <option key={g} value={g}>{g.charAt(0).toUpperCase() + g.slice(1)}</option>
              ))}
            </select>
          </div>

          {/* Sort By */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ArrowUpDown size={15} color="var(--text-muted)" />
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
            Filter
          </button>
        </form>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px', fontSize: '12px', color: 'var(--text-secondary)' }}>
          <span>{totalCount} anime titles available • Page {page} of {totalPages}</span>
          {loading && (
            <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-red)' }}>
              <RefreshCw size={12} className="spin" /> Updating...
            </span>
          )}
        </div>
      </div>

      {/* Cards Grid - Each card is fully clickable! */}
      <div className="cards-grid">
        {animeList.map((anime) => (
          <AnimeCard
            key={anime.anime_id}
            anime={anime}
            userRating={userRatings[anime.anime_id] || 0}
            onRate={handleRate}
            onClick={() => onSelectAnime && onSelectAnime(anime)}
            showAttribution={false}
          />
        ))}
      </div>

      {/* Pagination Controls */}
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '14px', marginTop: '36px' }}>
        <button
          className="btn-card-action"
          style={{ width: 'auto', padding: '10px 18px', opacity: page <= 1 ? 0.5 : 1 }}
          disabled={page <= 1}
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          id="btn-pagination-prev"
        >
          <ChevronLeft size={16} /> Previous
        </button>

        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '13px', color: 'var(--text-secondary)' }}>
          {page} / {totalPages}
        </span>

        <button
          className="btn-card-action"
          style={{ width: 'auto', padding: '10px 18px', opacity: page >= totalPages ? 0.5 : 1 }}
          disabled={page >= totalPages}
          onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
          id="btn-pagination-next"
        >
          Next <ChevronRight size={16} />
        </button>
      </div>
    </div>
  );
}
