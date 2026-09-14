import React, { useEffect, useState } from 'react';
import { ArrowLeft, Star, ExternalLink, Sparkles, Tv, CheckCircle2 } from 'lucide-react';
import AnimeCard from '../components/AnimeCard';
import NetflixRow from '../components/NetflixRow';
import { api } from '../services/api';

export default function AnimeDetailPage({
  anime: initialAnime,
  onBack,
  onSelectAnime,
  sessionRatings = [],
  onRate
}) {
  const [anime, setAnime] = useState(initialAnime);
  const [similarAnime, setSimilarAnime] = useState([]);
  const [loadingSimilar, setLoadingSimilar] = useState(false);
  const [personalizedAnime, setPersonalizedAnime] = useState([]);
  const [loadingPersonalized, setLoadingPersonalized] = useState(false);
  const [userRating, setUserRating] = useState(0);
  const [ratedSuccess, setRatedSuccess] = useState(false);

  // Sync initialAnime into state and fetch complete record from catalog API to ensure rate_1..rate_5 and full details are loaded
  useEffect(() => {
    setAnime(initialAnime);
    if (!initialAnime?.anime_id) return;

    let isMounted = true;
    api.getAnimeById(initialAnime.anime_id)
      .then((fullData) => {
        if (isMounted && fullData) {
          setAnime((prev) => ({ ...prev, ...fullData }));
        }
      })
      .catch((err) => console.warn('Could not fetch full anime record:', err));

    return () => { isMounted = false; };
  }, [initialAnime?.anime_id]);

  // Sync existing user rating for this anime
  useEffect(() => {
    const existing = sessionRatings.find((r) => r.anime_id === anime?.anime_id);
    if (existing) {
      setUserRating(existing.rating);
    } else {
      setUserRating(0);
    }
  }, [anime?.anime_id, sessionRatings]);

  // Fetch Item-to-Item CBF: "More Like This"
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (!anime?.anime_id) return;

    let isMounted = true;
    setLoadingSimilar(true);

    api.getSimilarAnime(anime.anime_id, 8)
      .then((data) => {
        const items = data?.similar || data?.data?.similar || (Array.isArray(data?.data) ? data.data : []);
        if (isMounted && Array.isArray(items)) {
          setSimilarAnime(items);
        }
      })
      .catch((err) => console.warn('Failed to fetch similar anime:', err))
      .finally(() => {
        if (isMounted) setLoadingSimilar(false);
      });

    return () => { isMounted = false; };
  }, [anime?.anime_id]);

  // Fetch Personalized CBF: "Recommended For You" if ratings exist
  useEffect(() => {
    if (sessionRatings.length === 0) {
      setPersonalizedAnime([]);
      return;
    }

    let isMounted = true;
    setLoadingPersonalized(true);

    api.getPersonalizedCBF({ sessionRatings, topK: 6 })
      .then((res) => {
        if (isMounted && res.success && res.data) {
          // Filter out current anime from personalized list if present
          const filtered = (res.data.recommendations || []).filter(
            (item) => item.anime_id !== anime?.anime_id
          );
          setPersonalizedAnime(filtered);
        }
      })
      .catch((err) => console.warn('Failed to fetch personalized CBF:', err))
      .finally(() => {
        if (isMounted) setLoadingPersonalized(false);
      });

    return () => { isMounted = false; };
  }, [anime?.anime_id, sessionRatings]);

  if (!anime) return null;

  const matchPercentage = anime.match_percentage || (anime.rate ? Math.round((anime.rate / 5) * 100) : 85);

  const handleRate = async (stars) => {
    setUserRating(stars);
    if (onRate) onRate(anime.anime_id, stars);
    setRatedSuccess(true);
    setTimeout(() => setRatedSuccess(false), 2200);
  };

  // Rating histogram percentages calculation
  const totalVotes = (anime.rate_1 || 0) + (anime.rate_2 || 0) + (anime.rate_3 || 0) + (anime.rate_4 || 0) + (anime.rate_5 || 0);
  
  let starBars = [];
  if (totalVotes > 0) {
    starBars = [5, 4, 3, 2, 1].map((star) => {
      const count = anime[`rate_${star}`] || 0;
      const pct = Math.round((count / totalVotes) * 100);
      return { star, count, pct };
    });
  } else if (anime.votes > 0 && anime.rate > 0) {
    // Graceful fallback if dataset only contains aggregated mean rate and votes
    const mean = anime.rate;
    const weights = [5, 4, 3, 2, 1].map((star) => Math.max(0.01, Math.exp(-Math.pow(star - mean, 2) / 1.0)));
    const sumW = weights.reduce((a, b) => a + b, 0);
    starBars = [5, 4, 3, 2, 1].map((star, i) => {
      const pct = Math.round((weights[i] / sumW) * 100);
      const count = Math.round((weights[i] / sumW) * anime.votes);
      return { star, count, pct };
    });
  } else {
    starBars = [5, 4, 3, 2, 1].map((star) => ({ star, count: 0, pct: 0 }));
  }

  return (
    <div className="anime-detail-page">
      {/* Top Back Navigation */}
      <button className="back-btn" onClick={onBack} id="btn-back-to-browse">
        <ArrowLeft size={16} />
        <span>Back</span>
      </button>

      {/* Hero Showcase Section */}
      <div className="detail-hero">
        {/* Background Ambient Glow */}
        {anime.anime_img && (
          <div
            className="hero-backdrop-glow"
            style={{ backgroundImage: `url(${anime.anime_img})` }}
          />
        )}

        <div className="detail-hero-content">
          {/* Main Poster */}
          <div className="detail-poster-container">
            {anime.anime_img ? (
              <img
                src={anime.anime_img}
                alt={anime.title}
                className="detail-poster-img"
              />
            ) : (
              <div className="poster-fallback" style={{ height: '340px' }}>
                <Tv size={48} />
                <span>No Poster</span>
              </div>
            )}
          </div>

          {/* Metadata & Actions */}
          <div className="detail-info-pane">
            <div className="detail-badges-row">
              <span className="match-pill">
                <Sparkles size={12} />
                <span>{matchPercentage}% Match</span>
              </span>
              <span className="meta-pill">{anime.episodes} Episodes</span>
              <span className="meta-pill">TV Series</span>
            </div>

            <h1 className="detail-title">{anime.title}</h1>

            <div className="detail-meta-row">
              <div className="rating-pill">
                <Star size={14} fill="currentColor" />
                <span className="rating-num">{anime.rate}</span>
                <span className="rating-denom">/ 5.0</span>
              </div>
              <span className="votes-count">
                Based on {anime.votes ? anime.votes.toLocaleString() : '0'} viewer ratings
              </span>
            </div>

            {/* Genre Tags */}
            <div className="detail-genres-row">
              {(anime.genres || []).map((g) => (
                <span key={g} className="detail-genre-pill">
                  {g}
                </span>
              ))}
            </div>

            {/* Action Buttons */}
            <div className="detail-actions-row">
              {anime.anime_url && (
                <a
                  href={anime.anime_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-watch"
                >
                  <ExternalLink size={15} />
                  <span>Watch on Crunchyroll</span>
                </a>
              )}

              {/* Live Rating Widget */}
              <div className="interactive-rate-box">
                <span className="rate-prompt-label">Your Rating:</span>
                <div className="stars-wrapper">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      className={`star-rate-btn ${userRating >= star ? 'active' : ''}`}
                      onClick={() => handleRate(star)}
                      title={`Rate ${star} Stars`}
                    >
                      <Star size={18} fill={userRating >= star ? 'currentColor' : 'none'} />
                    </button>
                  ))}
                </div>
                {ratedSuccess && (
                  <span className="rate-saved-label">
                    <CheckCircle2 size={13} />
                    <span>Saved</span>
                  </span>
                )}
              </div>
            </div>

            {/* Dual score breakdown if present */}
            {anime.cbf_match_pct !== undefined && anime.kbr_match_pct !== undefined && (
              <div className="match-reason-card">
                <div className="reason-header">
                  <Sparkles size={14} />
                  <span>Smart Match Component Breakdown</span>
                </div>

                <div className="breakdown-bars-grid">
                  <div className="bar-group">
                    <div className="bar-label">
                      <span>Personal Taste (Content-Based)</span>
                      <span>{anime.cbf_match_pct}%</span>
                    </div>
                    <div className="progress-track">
                      <div
                        className="progress-fill fill-cb"
                        style={{ width: `${anime.cbf_match_pct}%` }}
                      />
                    </div>
                  </div>

                  <div className="bar-group">
                    <div className="bar-label">
                      <span>Requirement Fit (Knowledge-Based)</span>
                      <span>{anime.kbr_match_pct}%</span>
                    </div>
                    <div className="progress-track">
                      <div
                        className="progress-fill fill-kb"
                        style={{ width: `${anime.kbr_match_pct}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Viewer Rating Distribution INSIDE detail-hero */}
        <div className="hero-ratings-section">
          <div className="hero-ratings-header">
            <h3 className="hero-ratings-title">Viewer Rating Distribution</h3>
            <span className="hero-ratings-sub">
              Based on {anime.votes ? anime.votes.toLocaleString() : '0'} verified community ratings
            </span>
          </div>

          <div className="ratings-histogram-panel">
            {starBars.map(({ star, count, pct }) => (
              <div key={star} className="hist-row">
                <span className="hist-star-label">
                  <span>{star}</span>
                  <Star size={11} fill="#f59e0b" color="#f59e0b" />
                </span>
                <div className="hist-track">
                  <div className="hist-fill" style={{ width: `${pct}%` }} />
                </div>
                <span className="hist-pct-label">
                  {pct}%
                  {count > 0 && <span className="hist-count-sub"> ({count.toLocaleString()})</span>}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ============================================================ */}
      {/* SECTION 1: MORE LIKE THIS (NETFLIX-STYLE ROW WITH ARROWS)   */}
      {/* ============================================================ */}
      <NetflixRow
        title="More Like This"
        categoryLabel="Content-Based Filtering (CountVectorizer + Cosine Similarity)"
        subtitle={`Titles sharing closest genre vector cosine similarity with ${anime.title}.`}
        items={similarAnime}
        loading={loadingSimilar}
        onSelectAnime={onSelectAnime}
        onRate={onRate}
        sessionRatings={sessionRatings}
        emptyMessage="No closely matching titles found in the catalog."
      />

      {/* ============================================================ */}
      {/* SECTION 2: RECOMMENDED FOR YOU (NETFLIX-STYLE ROW WITH ARROWS) */}
      {/* ============================================================ */}
      {sessionRatings.length > 0 && (
        <NetflixRow
          title="Recommended For You"
          categoryLabel="Content-Based Filtering (Reference Anime Match)"
          subtitle={`Top-N recommendations matching your active reference anime.`}
          items={personalizedAnime}
          loading={loadingPersonalized}
          onSelectAnime={onSelectAnime}
          onRate={onRate}
          sessionRatings={sessionRatings}
          emptyMessage="Rate more titles to expand your personalized recommendation row."
        />
      )}
    </div>
  );
}
