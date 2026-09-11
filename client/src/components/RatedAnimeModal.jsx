import React, { useState, useEffect } from 'react';
import { Star, X, Trash2, RotateCcw, ExternalLink, Film, Sparkles } from 'lucide-react';
import { api } from '../services/api';

export default function RatedAnimeModal({
  isOpen,
  onClose,
  sessionRatings = [],
  onRate,
  onRemoveRating,
  onClearRatings,
  onSelectAnime,
  onNavigate
}) {
  const [ratedAnimeDetails, setRatedAnimeDetails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hoveredStars, setHoveredStars] = useState({}); // { [animeId]: starNumber }
  const [confirmClear, setConfirmClear] = useState(false);

  // Load details for all rated anime
  useEffect(() => {
    if (!isOpen) return;

    if (sessionRatings.length === 0) {
      setRatedAnimeDetails([]);
      return;
    }

    const ids = sessionRatings.map((r) => r.anime_id);
    setLoading(true);

    api.getAnimeBatch(ids)
      .then((res) => {
        if (res.success && res.data) {
          setRatedAnimeDetails(res.data);
        }
      })
      .catch((err) => {
        console.warn('Could not load rated anime details:', err);
      })
      .finally(() => setLoading(false));
  }, [isOpen, sessionRatings]);

  if (!isOpen) return null;

  // Build lookup map for ratings
  const ratingMap = new Map();
  sessionRatings.forEach((r) => ratingMap.set(r.anime_id, r.rating));

  return (
    <div className="modal-backdrop-liquid" onClick={onClose} role="dialog" aria-modal="true">
      <div
        className="rated-modal-content glass-liquid-panel"
        onClick={(e) => e.stopPropagation()}
      >
        {/* MODAL HEADER */}
        <div className="rated-modal-header">
          <div className="rated-modal-title-wrap">
            <div className="rated-modal-icon-badge">
              <Star size={18} className="star-active" />
            </div>
            <div>
              <div className="rated-modal-title-row">
                <h2 className="rated-modal-title">Your Rated Anime</h2>
                <span className="rated-count-pill">
                  {sessionRatings.length} {sessionRatings.length === 1 ? 'Title' : 'Titles'}
                </span>
              </div>
              <p className="rated-modal-subtitle">
                These ratings mathematically shape your personal Content-Based taste vector in real-time.
              </p>
            </div>
          </div>

          <button
            className="rated-modal-close-btn"
            onClick={onClose}
            aria-label="Close modal"
            id="btn-close-rated-modal"
          >
            <X size={18} />
          </button>
        </div>

        {/* MODAL BODY */}
        <div className="rated-modal-body">
          {sessionRatings.length === 0 ? (
            <div className="rated-modal-empty">
              <div className="empty-icon-circle">
                <Film size={32} />
              </div>
              <h3 className="empty-title">No Anime Rated Yet</h3>
              <p className="empty-desc">
                Rate titles across the catalog or in recommendation streams. Each 1-5 star rating updates your genre preferences instantly for personalized suggestions.
              </p>
              {onNavigate && (
                <button
                  className="btn-primary"
                  onClick={() => {
                    onClose();
                    onNavigate('browse_find');
                  }}
                  id="btn-rated-empty-browse"
                >
                  <Sparkles size={15} />
                  <span>Explore Catalog & Rate</span>
                </button>
              )}
            </div>
          ) : (
            <div className="rated-items-list">
              {loading && ratedAnimeDetails.length === 0 ? (
                <div className="rated-modal-loading">
                  <span>Loading rated titles...</span>
                </div>
              ) : (
                ratedAnimeDetails.map((anime) => {
                  const currentRating = ratingMap.get(anime.anime_id) || 0;
                  const hoveredStar = hoveredStars[anime.anime_id] || 0;
                  const displayRating = hoveredStar || currentRating;

                  return (
                    <div key={anime.anime_id} className="rated-item-card">
                      {/* POSTER THUMBNAIL */}
                      <div
                        className="rated-item-thumb-wrap"
                        onClick={() => {
                          onClose();
                          if (onSelectAnime) onSelectAnime(anime);
                        }}
                      >
                        <img
                          src={anime.anime_img || 'https://via.placeholder.com/120x160?text=Anime'}
                          alt={anime.title}
                          className="rated-item-thumb"
                          loading="lazy"
                          onError={(e) => {
                            e.currentTarget.src = 'https://via.placeholder.com/120x160?text=Anime';
                          }}
                        />
                        <div className="thumb-hover-overlay">
                          <ExternalLink size={14} />
                        </div>
                      </div>

                      {/* ITEM DETAILS */}
                      <div className="rated-item-info">
                        <h4
                          className="rated-item-title"
                          onClick={() => {
                            onClose();
                            if (onSelectAnime) onSelectAnime(anime);
                          }}
                        >
                          {anime.title}
                        </h4>

                        <div className="rated-item-meta">
                          {anime.episodes && (
                            <span className="meta-tag">{anime.episodes} eps</span>
                          )}
                          {anime.rate && (
                            <span className="meta-tag meta-tag-score">
                              MAL {anime.rate.toFixed(1)}
                            </span>
                          )}
                          {anime.genres && anime.genres.slice(0, 3).map((g) => (
                            <span key={g} className="meta-genre-chip">
                              {g}
                            </span>
                          ))}
                        </div>

                        {/* LIVE 5-STAR RATING COMPONENT */}
                        <div className="rated-stars-control-row">
                          <span className="rating-control-label">Your Score:</span>
                          <div
                            className="interactive-stars"
                            onMouseLeave={() =>
                              setHoveredStars((prev) => ({ ...prev, [anime.anime_id]: 0 }))
                            }
                          >
                            {[1, 2, 3, 4, 5].map((star) => (
                              <button
                                key={star}
                                className={`star-btn ${star <= displayRating ? 'active' : ''}`}
                                onMouseEnter={() =>
                                  setHoveredStars((prev) => ({
                                    ...prev,
                                    [anime.anime_id]: star,
                                  }))
                                }
                                onClick={() => {
                                  if (onRate) onRate(anime.anime_id, star);
                                }}
                                title={`Rate ${star} out of 5 stars`}
                                aria-label={`Rate ${star} stars`}
                              >
                                <Star
                                  size={16}
                                  fill={star <= displayRating ? '#f59e0b' : 'none'}
                                  color={star <= displayRating ? '#f59e0b' : '#64748b'}
                                />
                              </button>
                            ))}
                          </div>
                          <span className="rating-score-num">
                            {currentRating > 0 ? `${currentRating} / 5` : 'Not rated'}
                          </span>
                        </div>
                      </div>

                      {/* ACTION: REMOVE RATING */}
                      <div className="rated-item-actions">
                        <button
                          className="btn-remove-rating"
                          onClick={() => {
                            if (onRemoveRating) onRemoveRating(anime.anime_id);
                          }}
                          title="Remove this rating"
                          aria-label={`Remove rating for ${anime.title}`}
                        >
                          <Trash2 size={15} />
                        </button>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          )}
        </div>

        {/* MODAL FOOTER */}
        {sessionRatings.length > 0 && (
          <div className="rated-modal-footer">
            <div className="footer-left">
              {confirmClear ? (
                <div className="confirm-clear-row">
                  <span className="confirm-text">Clear all {sessionRatings.length} ratings?</span>
                  <button
                    className="btn-confirm-yes"
                    onClick={() => {
                      if (onClearRatings) onClearRatings();
                      setConfirmClear(false);
                    }}
                  >
                    Yes, Clear
                  </button>
                  <button
                    className="btn-confirm-no"
                    onClick={() => setConfirmClear(false)}
                  >
                    Cancel
                  </button>
                </div>
              ) : (
                <button
                  className="btn-clear-all"
                  onClick={() => setConfirmClear(true)}
                  id="btn-clear-all-ratings"
                >
                  <RotateCcw size={14} />
                  <span>Reset All Ratings</span>
                </button>
              )}
            </div>

            <button
              className="btn-secondary"
              onClick={onClose}
              id="btn-close-rated-modal-footer"
            >
              <span>Done</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
