import React, { useState } from 'react';
import { Star, Tv, Sparkles, ExternalLink, ChevronDown, ChevronUp, Check, X } from 'lucide-react';

export default function AnimeCard({
  anime,
  onClick,
  onRate,
  userRating = 0,
  showAttribution = true,
  showRules = false
}) {
  const [imgError, setImgError] = useState(false);
  const [hoverRating, setHoverRating] = useState(0);
  const [rulesOpen, setRulesOpen] = useState(false);

  const matchPercentage = anime.match_percentage || (anime.rate ? Math.round((anime.rate / 5) * 100) : null);

  const handleCardClick = (e) => {
    // Avoid triggering card navigation when rating or clicking external link or expanding rules
    if (
      e.target.closest('.star-btn') ||
      e.target.closest('.ext-link') ||
      e.target.closest('.rules-toggle-btn') ||
      e.target.closest('.rules-accordion-body')
    ) {
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

        {matchPercentage && (
          <div className="card-match-badge" title="Algorithm Match Score">
            <Sparkles size={11} />
            <span>{matchPercentage}% Match</span>
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

        {/* Dual Scores for 1+1 Hybrid */}
        {anime.cbf_match_pct !== undefined && anime.kbr_match_pct !== undefined && (
          <div className="dual-scores-pill">
            <span className="dual-taste">Taste {anime.cbf_match_pct}%</span>
            <span className="dual-sep">•</span>
            <span className="dual-fit">Fit {anime.kbr_match_pct}%</span>
          </div>
        )}

        {/* Expandable "Why does this match?" for KBR and Hybrid */}
        {anime.rule_evaluations && anime.rule_evaluations.length > 0 && (
          <div className="rules-accordion-container">
            <button
              type="button"
              className="rules-toggle-btn"
              onClick={(e) => {
                e.stopPropagation();
                setRulesOpen((prev) => !prev);
              }}
            >
              <span>Why does this match?</span>
              {rulesOpen ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
            </button>

            {rulesOpen && (
              <div className="rules-accordion-body" onClick={(e) => e.stopPropagation()}>
                <div className="rules-list">
                  {anime.rule_evaluations.map((r, idx) => (
                    <div key={idx} className={`rule-item ${r.passed ? 'rule-passed' : 'rule-failed'}`}>
                      <div className="rule-item-header">
                        {r.passed ? <Check size={11} className="rule-icon-pass" /> : <X size={11} className="rule-icon-fail" />}
                        <span className="rule-name">{r.rule}</span>
                        <span className="rule-status-badge">{r.passed ? 'PASS' : 'FAIL'}</span>
                      </div>
                      <div className="rule-details">
                        <span className="rule-target">Target: {r.target}</span>
                        <span className="rule-actual">Result: {r.actual}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

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
