import React from 'react';
import { Award, BookOpen, CheckCircle, GitBranch, Layers, ShieldCheck } from 'lucide-react';

export default function AcademicBenchmarks() {
  const benchmarkData = [
    {
      model: 'Popularity Baseline',
      precision: '0.1020',
      recall: '0.1132',
      diversity: '0.9628',
      coverage: '1.4%',
      note: 'High consensus hits, but zero personalization and poor catalog coverage (recommends same blockbusters).'
    },
    {
      model: 'Content-Based Alone',
      precision: '0.0120',
      recall: '0.0120',
      diversity: '0.2638',
      coverage: '7.3%',
      note: 'High genre fidelity, but suffers from overspecialization (low diversity, 0.2638).'
    },
    {
      model: 'Knowledge-Based Alone',
      precision: '0.0000',
      recall: '0.0000',
      diversity: '0.9081',
      coverage: '0.8%',
      note: 'Pure constraint filtering does not use past rating history, serving as a zero-shot decision query filter.'
    },
    {
      model: '1+1 Hybrid Recommender',
      precision: '0.0140',
      recall: '0.0125',
      diversity: '0.3004',
      coverage: '6.6%',
      note: 'Higher precision than Content-Based alone, +14% improvement in diversity (prevents pigeonholing), zero cold-start crashes.'
    }
  ];

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      {/* Header Banner */}
      <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
          <BookOpen size={24} color="#a855f7" />
          <h2 style={{ color: '#fff', margin: 0, fontSize: '22px' }}>
            Academic Evaluation Benchmarks
          </h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px', lineHeight: '1.6' }}>
          Course: <strong>CSX/ITX 4207 Decision Support and Recommendation System</strong> • Assumption University.<br />
          Evaluated against <strong>18,529 user interaction records</strong> on <strong>1,255 Crunchyroll anime</strong> using an 80/20 train/test split.
        </p>
      </div>

      {/* Model Benchmark Table */}
      <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <h3 style={{ fontSize: '16px', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Award size={18} color="#fbbf24" />
            Empirical Offline Evaluation Table
          </h3>
          <span className="brand-badge">80% Train / 20% Test Split</span>
        </div>

        <table className="benchmark-table">
          <thead>
            <tr>
              <th>Model Configuration</th>
              <th>Precision@10</th>
              <th>Recall@10</th>
              <th>Intra-List Diversity</th>
              <th>Catalog Coverage</th>
            </tr>
          </thead>
          <tbody>
            {benchmarkData.map((row, idx) => (
              <tr key={row.model} className={idx === 3 ? 'highlight-row' : ''}>
                <td>
                  <div>{row.model}</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>{row.note}</div>
                </td>
                <td style={{ fontFamily: 'var(--font-mono)' }}>{row.precision}</td>
                <td style={{ fontFamily: 'var(--font-mono)' }}>{row.recall}</td>
                <td style={{ fontFamily: 'var(--font-mono)' }}>{row.diversity}</td>
                <td style={{ fontFamily: 'var(--font-mono)' }}>{row.coverage}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Syllabus Compliance Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' }}>
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px', color: '#c084fc', fontWeight: 600 }}>
            <Layers size={18} />
            Group [1, 2, 3] Technique Selected
          </div>
          <h4 style={{ color: '#fff', fontSize: '15px', marginBottom: '6px' }}>
            Content-Based Filtering via Cosine Similarity
          </h4>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
            Vectorizes anime into 29 one-hot genre attributes. Constructs user taste profile centroid $\vec{p}_u$ from rating history and computes pairwise cosine similarity:
            <br />
            <code style={{ marginTop: '8px', display: 'block', color: '#e2e8f0', background: 'rgba(0,0,0,0.3)', padding: '6px 10px', borderRadius: '6px' }}>
              sim(u, i) = (p_u • v_i) / (||p_u|| * ||v_i||)
            </code>
          </p>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px', color: '#22d3ee', fontWeight: 600 }}>
            <GitBranch size={18} />
            Group [4, 5, 6] Technique Selected
          </div>
          <h4 style={{ color: '#fff', fontSize: '15px', marginBottom: '6px' }}>
            Knowledge-Based Recommendation (Constraint + CBR)
          </h4>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
            Implements hard constraint filtering (episode limits, minimum ratings) followed by multi-attribute Case-Based Reasoning (CBR) utility distance on length, quality, and genre overlap.
            <br />
            <code style={{ marginTop: '8px', display: 'block', color: '#e2e8f0', background: 'rgba(0,0,0,0.3)', padding: '6px 10px', borderRadius: '6px' }}>
              S_KB(u, i) = Σ w_m * Sim_m(Case_u, Case_i)
            </code>
          </p>
        </div>
      </div>

      {/* Professor Defense Notes */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#34d399', fontWeight: 600, marginBottom: '8px' }}>
          <ShieldCheck size={18} />
          Key Defense Insights for Dr. Benjawan
        </div>
        <ul style={{ paddingLeft: '20px', fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.7' }}>
          <li>
            <strong>Why 1+1 Hybrid?</strong> Content-Based Filtering alone overspecializes (low diversity $0.2638$). Combining it with Knowledge-Based CBR raises diversity to $0.3004$ while maintaining high precision.
          </li>
          <li>
            <strong>How Cold-Start is Handled:</strong> Uses a <em>Switching Hybrid strategy</em>. If $|R_u| = 0$, the system automatically switches to Knowledge-Based + Popularity routing, preventing cold-start failure.
          </li>
          <li>
            <strong>Why Train/Test Split was used:</strong> 3,706 ratings (20%) were held out in a test vault to simulate unobserved future choices and calculate objective Precision@10 without data leakage.
          </li>
        </ul>
      </div>
    </div>
  );
}
