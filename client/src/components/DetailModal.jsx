import React, { useEffect, useState } from 'react';
import { X, Star, ExternalLink, Sparkles, Sliders, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

export default function DetailModal({ anime, onClose, onSelectSimilar }) {
  const [similarAnime, setSimilarAnime] = useState([]);
  const [loadingSimilar, setLoadingSimilar] = useState(false);

  useEffect(() => {
    if (!anime) return;
    let isMounted = true;
    setLoadingSimilar(true);

    api.getSimilarAnime(anime.anime_id, 4)
      .then((data) => {
        const items = data?.similar || data?.data?.similar || (Array.isArray(data?.data) ? data.data : []);
        if (isMounted && Array.isArray(items)) {
          setSimilarAnime(items);
        }
      })
      .catch((err) => console.warn('Could not fetch similar anime:', err))
      .finally(() => {
        if (isMounted) setLoadingSimilar(false);
      });

    return () => { isMounted = false; };
  }, [anime]);

  if (!anime) return null;

  // Rating star histogram percentages
  const totalStarVotes = (anime.rate_1 || 0) + (anime.rate_2 || 0) + (anime.rate_3 || 0) + (anime.rate_4 || 0) + (anime.rate_5 || 0) || 1;
  const starBars = [5, 4, 3, 2, 1].map((star) => {
    const count = anime[`rate_${star}`] || 0;
    const pct = Math.round((count / totalStarVotes) * 100);
    return { star, count, pct };
  });

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose} id="modal-close-btn">
          <X size={18} />
        </button>

        <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
          {anime.anime_img && (
            <img
              src={anime.anime_img}
              alt={anime.title}
              style={{ width: '110px', height: '150px', objectFit: 'cover', borderRadius: '10px' }}
            />
          )}
          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
              <span className="section-tag">ID: #{anime.anime_id}</span>
              {anime.match_percentage && (
                <span className="switching-mode-badge mode-experienced">
                  <Sparkles size={11} /> {anime.match_percentage}% Utility Fit
                </span>
              )}
            </div>
            <h2 style={{ fontSize: '20px', color: '#fff', marginBottom: '8px' }}>{anime.title}</h2>
            <div style={{ display: 'flex', gap: '12px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              <span style={{ color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Star size={13} fill="#fbbf24" stroke="none" /> {anime.rate} / 5.0
              </span>
              <span>•</span>
              <span>{anime.episodes} Total Episodes</span>
              <span>•</span>
              <span>{anime.votes?.toLocaleString()} Votes</span>
            </div>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '10px' }}>
              {(anime.genres || []).map((g) => (
                <span key={g} className="genre-tag">{g}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Mathematical Component Breakdown (Ch 10 & 14) */}
        {anime.component_scores && (
          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '12px', marginBottom: '20px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '13px', fontWeight: 600, color: '#e2e8f0', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Sliders size={14} color="#a855f7" />
              1+1 Hybrid Mathematical Scoring (Chapter 10)
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px', textAlign: 'center' }}>
              <div style={{ padding: '10px', background: 'rgba(168,85,247,0.1)', borderRadius: '8px', border: '1px solid rgba(168,85,247,0.3)' }}>
                <div style={{ fontSize: '11px', color: '#d8b4fe' }}>Content-Based Sim [Ch 3/4]</div>
                <div style={{ fontSize: '18px', fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#fff' }}>
                  {anime.component_scores.content_based}
                </div>
                <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Cosine Genre Match</div>
              </div>

              <div style={{ padding: '10px', background: 'rgba(6,182,212,0.1)', borderRadius: '8px', border: '1px solid rgba(6,182,212,0.3)' }}>
                <div style={{ fontSize: '11px', color: '#67e8f9' }}>Knowledge-Based [Ch 7]</div>
                <div style={{ fontSize: '18px', fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#fff' }}>
                  {anime.component_scores.knowledge_based}
                </div>
                <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>CBR Multi-Attribute</div>
              </div>

              <div style={{ padding: '10px', background: 'rgba(245,158,11,0.1)', borderRadius: '8px', border: '1px solid rgba(245,158,11,0.3)' }}>
                <div style={{ fontSize: '11px', color: '#fde68a' }}>Popularity Prior [Ch 2]</div>
                <div style={{ fontSize: '18px', fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#fff' }}>
                  {anime.component_scores.popularity}
                </div>
                <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Bayesian Smoothed</div>
              </div>
            </div>
          </div>
        )}

        {/* Rating Distribution Histogram */}
        <div style={{ marginBottom: '20px' }}>
          <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '8px' }}>
            Crunchyroll Community Rating Histogram ({totalStarVotes.toLocaleString()} Ratings)
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {starBars.map(({ star, count, pct }) => (
              <div key={star} style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px' }}>
                <span style={{ width: '45px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{star} ★</span>
                <div style={{ flex: 1, height: '8px', background: 'rgba(255,255,255,0.08)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: '#fbbf24' }} />
                </div>
                <span style={{ width: '35px', textAlign: 'right', fontFamily: 'var(--font-mono)', color: 'var(--text-secondary)' }}>{pct}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Content-Based Similar Anime (Chapter 3/4 Cosine Similarity) */}
        <div>
          <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Sparkles size={14} color="#a855f7" />
            Most Similar Titles via 29-Genre Cosine Similarity (Ch 3/4)
          </div>

          {loadingSimilar ? (
            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Calculating vector dot-products...</div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(130px, 1fr))', gap: '10px' }}>
              {similarAnime.map((sim) => (
                <div
                  key={sim.anime_id}
                  onClick={() => onSelectSimilar && onSelectSimilar(sim)}
                  style={{
                    background: 'rgba(255,255,255,0.03)',
                    padding: '8px',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    border: '1px solid var(--border-subtle)',
                    transition: 'all 0.15s ease'
                  }}
                  title={`Cosine Similarity: ${sim.similarity}`}
                >
                  <img
                    src={sim.anime_img}
                    alt={sim.title}
                    style={{ width: '100%', height: '80px', objectFit: 'cover', borderRadius: '6px', marginBottom: '6px' }}
                    onError={(e) => { e.target.style.display = 'none'; }}
                  />
                  <div style={{ fontSize: '12px', fontWeight: 500, color: '#fff', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {sim.title}
                  </div>
                  <div style={{ fontSize: '10px', color: '#c084fc', fontFamily: 'var(--font-mono)' }}>
                    {Math.round(sim.similarity * 100)}% Sim
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
