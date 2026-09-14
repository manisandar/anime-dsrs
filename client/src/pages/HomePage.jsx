import React, { useState, useEffect } from 'react';
import { Sparkles, TrendingUp, Sliders, ArrowRight, Star, Compass, RefreshCw } from 'lucide-react';
import AnimeCard from '../components/AnimeCard';
import { api } from '../services/api';

export default function HomePage({
  onSelectAnime,
  sessionRatings = [],
  onRate,
  onNavigate,
  theme
}) {
  const [popularAnime, setPopularAnime] = useState([]);
  const [personalizedAnime, setPersonalizedAnime] = useState([]);
  const [userProfileMeta, setUserProfileMeta] = useState(null);
  const [loadingPopular, setLoadingPopular] = useState(true);
  const [loadingPersonalized, setLoadingPersonalized] = useState(false);

  // 1. Load Popular Right Now (Popularity-Based Recommendation)
  useEffect(() => {
    setLoadingPopular(true);
    api.getPopularRecommendations({ topK: 12 })
      .then((res) => {
        if (res.success && res.data) {
          setPopularAnime(res.data);
        }
      })
      .catch((err) => console.warn('Could not load popular anime:', err))
      .finally(() => setLoadingPopular(false));
  }, []);

  // 2. Load Personalized Recommendations (Content-Based Filtering) when ratings exist
  useEffect(() => {
    if (sessionRatings.length === 0) {
      setPersonalizedAnime([]);
      setUserProfileMeta(null);
      return;
    }

    setLoadingPersonalized(true);
    api.getPersonalizedCBF({ sessionRatings, topK: 12 })
      .then((res) => {
        if (res.success && res.data) {
          setPersonalizedAnime(res.data.recommendations || []);
          setUserProfileMeta(res.data);
        }
      })
      .catch((err) => console.warn('Could not load personalized CBF:', err))
      .finally(() => setLoadingPersonalized(false));
  }, [sessionRatings]);

  return (
    <div className="home-page-container">

      {/* COLD START ONBOARDING BANNER (0 RATINGS) */}
      {sessionRatings.length === 0 && (
        <section className="cold-start-banner glass-panel">
          <div className="cold-start-info">
            <div className="cold-start-icon-wrap">
              <Sparkles size={20} />
            </div>
            <div>
              <h3 className="cold-start-title">Select a Reference Anime for Content-Based Filtering</h3>
              <p className="cold-start-subtitle">
                Content-Based Filtering uses <strong>CountVectorizer</strong> on anime genres and ranks the catalog using <strong>Cosine Similarity</strong> against your selected reference anime.
              </p>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <button
              className="btn-outline"
              onClick={() => onRate && onRate(1, 5)}
              title="Set Naruto Shippuuden as reference anime"
            >
              <span>Try Naruto (Action/Fantasy)</span>
            </button>
            <button
              className="btn-primary"
              onClick={() => onNavigate('browse_find')}
            >
              <span>Browse Catalog</span>
              <ArrowRight size={14} />
            </button>
          </div>
        </section>
      )}

      {/* SECTION 1: RECOMMENDED FOR YOU (PURE CONTENT-BASED FILTERING) */}
      {sessionRatings.length > 0 && (
        <section className="home-stream-section">
          <div className="stream-header-row">
            <div>
              <div className="stream-category-label">Content-Based Filtering (CountVectorizer + Cosine Similarity)</div>
              <h2 className="stream-title">Similar to Your Reference Anime</h2>
              <p className="stream-subtitle">
                {userProfileMeta?.reference_anime ? (
                  <>
                    Reference Anime: <strong style={{ color: 'var(--accent-indigo)' }}>{userProfileMeta.reference_anime.title}</strong>
                    {userProfileMeta.reference_anime.genres && (
                      <span style={{ marginLeft: '8px', opacity: 0.85 }}>
                        [{userProfileMeta.reference_anime.genres.join(', ')}]
                      </span>
                    )}
                  </>
                ) : (
                  `Ranked by exact 29-genre cosine similarity against your latest selected anime.`
                )}
              </p>
            </div>

            {userProfileMeta?.preferred_genres && (
              <div className="taste-chips-row">
                {Object.keys(userProfileMeta.preferred_genres).slice(0, 5).map((genre) => (
                  <span key={genre} className="taste-chip">
                    {genre}
                  </span>
                ))}
              </div>
            )}
          </div>

          {loadingPersonalized ? (
            <div className="stream-loading-placeholder">
              <RefreshCw size={18} className="spin" />
              <span>Computing CountVectorizer & Cosine Similarity rankings...</span>
            </div>
          ) : (
            <div className="cards-grid">
              {personalizedAnime.map((anime) => (
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
          )}
        </section>
      )}

      {/* SECTION 2: POPULAR RIGHT NOW (POPULARITY-BASED RECOMMENDATION) */}
      <section className="home-stream-section">
        <div className="stream-header-row">
          <div>
            <div className="stream-category-label">Popularity-Based Recommendation</div>
            <h2 className="stream-title">Popular Right Now</h2>
            <p className="stream-subtitle">
              High-confidence consensus rankings computed using Bayesian rating smoothing.
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
              />
            ))}
          </div>
        )}
      </section>

      {/* SECTION 3: SMART MATCH BANNER */}
      <section className="smart-match-cta-section glass-panel">
        <div className="cta-left-pane">
          <div className="cta-kicker">1+1 Hybrid Recommendation</div>
          <h2 className="cta-heading">Ready to find your exact match?</h2>
          <p className="cta-desc">
            Combine your personal taste profile with situation-specific rules like episode commitments, minimum score thresholds, and viewing mood.
          </p>
        </div>
        <button
          className="btn-primary cta-btn"
          onClick={() => onNavigate('smart_match')}
        >
          <Sliders size={16} />
          <span>Launch Smart Match</span>
        </button>
      </section>
    </div>
  );
}
