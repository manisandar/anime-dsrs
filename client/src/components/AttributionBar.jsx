import React from 'react';

export default function AttributionBar({ attribution }) {
  if (!attribution) return null;

  const cb = attribution.content_based_pct || 0;
  const kb = attribution.knowledge_based_pct || 0;

  return (
    <div className="attribution-container">
      <div className="attribution-label">
        <span>Recommendation Match</span>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px' }}>
          {cb > 0 ? (
            <>
              <span style={{ color: 'var(--attr-taste)' }}>Taste {cb}% </span>
              <span style={{ color: 'var(--attr-filter)' }}>• Filters {kb}%</span>
            </>
          ) : (
            <span style={{ color: 'var(--attr-filter)' }}>Filters {kb}%</span>
          )}
        </span>
      </div>

      <div
        className="attribution-bar"
        title={cb > 0 ? `Taste Similarity: ${cb}%, Constraint & Mood Alignment: ${kb}%` : `Constraint & Mood Alignment: ${kb}%`}
      >
        {cb > 0 && <div className="attr-segment segment-cb" style={{ width: `${cb}%` }} />}
        <div className="attr-segment segment-kb" style={{ width: `${kb}%` }} />
      </div>
    </div>
  );
}
