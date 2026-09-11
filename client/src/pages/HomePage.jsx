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
              <Star size={20} />
            </div>
            <div>
              <h3 className="cold-start-title">Personalize Your Recommendations</h3>
              <p className="cold-start-subtitle">
                Rate anime anywhere in the catalog to generate your Content-Based preference profile. Positive ratings boost favored genres; lower ratings filter them out.
              </p>
            </div>
          </div>
          <button
            className="btn-outline"
            onClick={() => onNavigate('browse_find')}
          >
            <span>Start Rating</span>
            <ArrowRight size={14} />
          </button>
        </section>
      )}

      {/* SECTION 1: RECOMMENDED FOR YOU (PERSONALIZED CONTENT-BASED FILTERING) */}
      {sessionRatings.length > 0 && (
        <section className="home-stream-section">
          <div className="stream-header-row">
            <div>
              <div className="stream-category-label">Content-Based Filtering</div>
              <h2 className="stream-title">Recommended For You</h2>
              <p className="stream-subtitle">
                Calculated from your {sessionRatings.length} in-session ratings across 29 genre vectors.
              </p>
            </div>
            
            {userProfileMeta?.preferred_genres && (
              <div className="taste-chips-row">
                {Object.entries(userProfileMeta.preferred_genres).slice(0, 4).map(([genre, wt]) => (
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
              <span>Updating personalized matches...</span>
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
