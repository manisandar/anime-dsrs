import React, { useState } from 'react';
import { Star, Tv, ExternalLink } from 'lucide-react';

export default function AnimeCard({
  anime,
  onClick,
  onRate,
  userRating = 0,
  showAttribution = false,
  showMatchBadge = false
}) {
  const [imgError, setImgError] = useState(false);
  const [hoverRating, setHoverRating] = useState(0);

  const handleCardClick = (e) => {
    // Avoid triggering card navigation when rating or clicking external link
    if (e.target.closest('.star-btn') || e.target.closest('.ext-link')) {
      return;
    }
    if (onClick) onClick(anime);
  };

  return (
    <article
      className="anime-card clickable-card"
      onClick={handleCardClick}
      id={`anime-card-${anime.anime_id}`}
    >
      <div className="card-poster-wrapper">
        {!imgError && anime.anime_img ? (
          <img
            src={anime.anime_img}
            alt={anime.title}
            className="card-poster"
            loading="lazy"
            onError={() => setImgError(true)}
          />
        ) : (
          <div className="poster-fallback">
            <Tv size={32} />
            <span>{anime.genres?.[0] || 'Anime'}</span>
          </div>
        )}

      </div>

      <div className="card-content">
        <h3 className="card-title" title={anime.title}>
          {anime.title}
        </h3>

        <div className="card-meta-row">
          <div className="meta-rating">
            <Star size={13} fill="currentColor" />
            <span>{anime.rate}</span>
            <span className="meta-votes">
              ({anime.votes ? anime.votes.toLocaleString() : '0'})
            </span>
          </div>
          <span className="card-ep-count">
            {anime.episodes} eps
          </span>
        </div>

        <div className="card-genres">
          {(anime.genres || []).slice(0, 3).map((g) => (
            <span key={g} className="genre-tag">
              {g}
            </span>
          ))}
          {(anime.genres || []).length > 3 && (
            <span className="genre-tag genre-tag-more">
              +{anime.genres.length - 3}
            </span>
          )}
        </div>


        {/* Bottom Bar: Interactive Rating & Crunchyroll link */}
        <div className="card-footer-row">
          <div className="star-rating-row">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                type="button"
                className={`star-btn ${(hoverRating || userRating) >= star ? 'active' : ''}`}
                onMouseEnter={() => setHoverRating(star)}
                onMouseLeave={() => setHoverRating(0)}
                onClick={(e) => {
                  e.stopPropagation();
                  if (onRate) onRate(anime.anime_id, star);
                }}
                title={`Rate ${star} Stars`}
              >
                <Star size={13} fill={(hoverRating || userRating) >= star ? 'currentColor' : 'none'} />
              </button>
            ))}
          </div>

          {anime.anime_url && (
            <a
              href={anime.anime_url}
              target="_blank"
              rel="noopener noreferrer"
              className="ext-link"
              onClick={(e) => e.stopPropagation()}
              title="Watch on Crunchyroll"
            >
              <ExternalLink size={13} />
            </a>
          )}
        </div>
      </div>
    </article>
  );
}
