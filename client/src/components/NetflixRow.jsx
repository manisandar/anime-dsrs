import React, { useRef, useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, RefreshCw } from 'lucide-react';
import AnimeCard from './AnimeCard';

export default function NetflixRow({
  title,
  categoryLabel,
  subtitle,
  items = [],
  loading = false,
  onSelectAnime,
  onRate,
  sessionRatings = [],
  emptyMessage = 'No matching titles found in catalog.'
}) {
  const scrollRef = useRef(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);

  const checkScroll = () => {
    const el = scrollRef.current;
    if (!el) return;
    setCanScrollLeft(el.scrollLeft > 10);
    setCanScrollRight(el.scrollLeft + el.clientWidth < el.scrollWidth - 10);
  };

  useEffect(() => {
    checkScroll();
    const el = scrollRef.current;
    if (!el) return;

    el.addEventListener('scroll', checkScroll, { passive: true });
    window.addEventListener('resize', checkScroll);

    return () => {
      el.removeEventListener('scroll', checkScroll);
      window.removeEventListener('resize', checkScroll);
    };
  }, [items]);

  const handleScroll = (direction) => {
    const el = scrollRef.current;
    if (!el) return;

    const scrollAmount = Math.max(300, el.clientWidth * 0.75);
    el.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth'
    });
  };

  return (
    <div className="netflix-row-section">
      <div className="netflix-row-header">
        <div className="netflix-row-title-block">
          {categoryLabel && (
            <div className="stream-category-label">{categoryLabel}</div>
          )}
          <h2 className="section-heading">{title}</h2>
          {subtitle && <p className="section-subheading">{subtitle}</p>}
        </div>

        {/* Carousel Arrow Controls */}
        {items.length > 0 && !loading && (
          <div className="netflix-row-controls">
            <button
              className={`netflix-nav-btn ${!canScrollLeft ? 'disabled' : ''}`}
              onClick={() => handleScroll('left')}
              disabled={!canScrollLeft}
              aria-label="Scroll left"
              title="Previous"
            >
              <ChevronLeft size={20} />
            </button>

            <button
              className={`netflix-nav-btn ${!canScrollRight ? 'disabled' : ''}`}
              onClick={() => handleScroll('right')}
              disabled={!canScrollRight}
              aria-label="Scroll right"
              title="Next"
            >
              <ChevronRight size={20} />
            </button>
          </div>
        )}
      </div>

      {loading ? (
        <div className="stream-loading-placeholder">
          <RefreshCw size={18} className="spin" />
          <span>Loading recommendations...</span>
        </div>
      ) : items.length > 0 ? (
        <div className="netflix-row-container">
          {/* Left Hover Paddle */}
          {canScrollLeft && (
            <button
              className="netflix-side-paddle paddle-left"
              onClick={() => handleScroll('left')}
              aria-label="Scroll left"
            >
              <ChevronLeft size={26} />
            </button>
          )}

          {/* Single Row Horizontal Track */}
          <div className="netflix-row-track" ref={scrollRef}>
            {items.map((anime) => (
              <div key={anime.anime_id} className="netflix-card-wrapper">
                <AnimeCard
                  anime={anime}
                  onClick={() => onSelectAnime && onSelectAnime(anime)}
                  onRate={onRate}
                  userRating={(sessionRatings.find((r) => r.anime_id === anime.anime_id)?.rating) || 0}
                  showAttribution={false}
                />
              </div>
            ))}
          </div>

          {/* Right Hover Paddle */}
          {canScrollRight && (
            <button
              className="netflix-side-paddle paddle-right"
              onClick={() => handleScroll('right')}
              aria-label="Scroll right"
            >
              <ChevronRight size={26} />
            </button>
          )}
        </div>
      ) : (
        <div className="stream-loading-placeholder">
          <span>{emptyMessage}</span>
        </div>
      )}
    </div>
  );
}
