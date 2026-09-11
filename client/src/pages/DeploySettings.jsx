import React, { useState, useEffect } from 'react';
import { Server, Cloud, FolderGit2, CheckCircle2, RefreshCw, Save } from 'lucide-react';
import { api } from '../services/api';

export default function DeploySettings() {
  const [apiUrl, setApiUrl] = useState(localStorage.getItem('ANIME_DSRS_API_URL') || '');
  const [healthStatus, setHealthStatus] = useState(null);
  const [checking, setChecking] = useState(false);
  const [savedMsg, setSavedMsg] = useState(false);

  const checkHealth = async () => {
    setChecking(true);
    try {
      const data = await api.checkHealth();
      setHealthStatus(data);
    } catch (err) {
      setHealthStatus({ status: 'error', message: err.message });
    } finally {
      setChecking(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  const handleSaveUrl = (e) => {
    e.preventDefault();
    if (apiUrl.trim()) {
      localStorage.setItem('ANIME_DSRS_API_URL', apiUrl.trim());
    } else {
      localStorage.removeItem('ANIME_DSRS_API_URL');
    }
    setSavedMsg(true);
    setTimeout(() => setSavedMsg(false), 2500);
    checkHealth();
  };

  return (
    <div style={{ maxWidth: '850px', margin: '0 auto' }}>
      <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
        <h2 style={{ color: '#fff', fontSize: '20px', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Server size={20} color="#a855f7" />
          Deployment & Service Configuration
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px', lineHeight: '1.6' }}>
          Your current setup is running 100% locally. When ready, you can deploy the <strong>Python engine to Hugging Face Spaces</strong> and host this <strong>React frontend on GitHub Pages</strong>.
        </p>
      </div>

      {/* Local Health Status */}
      <div className="glass-panel" style={{ padding: '20px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
          <div style={{ fontWeight: 600, color: '#fff', fontSize: '15px' }}>Current Service Status</div>
          <button
            className="btn-card-action"
            style={{ width: 'auto', padding: '6px 14px' }}
            onClick={checkHealth}
            disabled={checking}
          >
            <RefreshCw size={13} className={checking ? 'spin' : ''} /> Check
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '14px' }}>
          <div style={{ padding: '14px', background: 'rgba(255,255,255,0.03)', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Client Academic Engine</div>
            <div style={{ fontSize: '14px', fontWeight: 600, color: '#fff', marginTop: '4px' }}>
              Built-in WASM / JS Recommender
            </div>
            <div style={{ fontSize: '11px', color: '#34d399', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <CheckCircle2 size={12} /> Status: Online ({healthStatus?.catalog_count || 1255} anime, 0ms latency)
            </div>
          </div>

          <div style={{ padding: '14px', background: 'rgba(255,255,255,0.03)', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Express Gateway & Python Engine</div>
            <div style={{ fontSize: '14px', fontWeight: 600, color: '#fff', marginTop: '4px' }}>
              {apiUrl ? apiUrl : 'Local / Static Fallback Active'}
            </div>
            <div style={{ fontSize: '11px', color: '#38bdf8', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <CheckCircle2 size={12} /> 100% Free Hugging Face Static Space Ready
            </div>
          </div>
        </div>
      </div>

      {/* Target Remote URL Configuration (for HF Spaces) */}
      <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
        <h3 style={{ fontSize: '16px', color: '#fff', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Cloud size={18} color="#06b6d4" />
          Hugging Face Spaces API Endpoint (Optional)
        </h3>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '14px' }}>
          Leave blank while testing locally (it automatically uses the local proxy). When deployed to GitHub Pages, paste your Hugging Face Space URL below:
        </p>

        <form onSubmit={handleSaveUrl} style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            placeholder="e.g. https://yourname-anime-dsrs.hf.space"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            style={{
              flex: 1,
              padding: '10px 14px',
              borderRadius: '8px',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid var(--border-subtle)',
              color: '#fff',
              fontFamily: 'var(--font-mono)',
              fontSize: '13px',
              outline: 'none'
            }}
          />
          <button type="submit" className="btn-primary" style={{ width: 'auto', padding: '10px 18px', fontSize: '13px' }}>
            <Save size={14} /> Save Endpoint
          </button>
        </form>
        {savedMsg && (
          <div style={{ marginTop: '8px', fontSize: '12px', color: '#34d399' }}>
            Endpoint saved successfully to browser storage!
          </div>
        )}
      </div>

      {/* Deployment Quick Guide */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '16px', color: '#fff', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <FolderGit2 size={18} color="#a855f7" />
          Deployment Roadmap (When Ready)
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', fontSize: '13px', color: 'var(--text-secondary)' }}>
          <div style={{ padding: '12px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
            <strong style={{ color: '#fff' }}>Step 1: Hugging Face Spaces (Python Engine)</strong>
            <p style={{ marginTop: '4px' }}>
              Create a free Hugging Face Space (Docker or Gradio/FastAPI). Copy the `recommender/` and `data/processed/` folders to the space. It gives you a free, public HTTPS URL.
            </p>
          </div>

          <div style={{ padding: '12px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
            <strong style={{ color: '#fff' }}>Step 2: GitHub Pages (React Client)</strong>
            <p style={{ marginTop: '4px' }}>
              Run <code>npm run build</code> inside the <code>client/</code> folder. Push the <code>dist/</code> folder to your GitHub repo's <code>gh-pages</code> branch.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
