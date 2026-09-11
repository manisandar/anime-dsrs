import React from 'react';
import { Home, Compass, Sliders, Sun, Moon, Star } from 'lucide-react';

export default function Navbar({
  activeTab,
  setActiveTab,
  theme,
  toggleTheme,
  sessionRatingsCount = 0,
  onOpenRatedModal,
}) {
  return (
    <header className="navbar">
      <div className="nav-brand" onClick={() => setActiveTab('home')}>
        <div className="brand-icon">
          <span className="brand-glyph">V</span>
        </div>
        <div className="brand-text-block">
          <span className="brand-title">ANIVIBE</span>
          <span className="brand-sub">Decision Support & Recommender</span>
        </div>
      </div>

      <nav className="nav-links">
        <button
          className={`nav-btn ${activeTab === 'home' ? 'active' : ''}`}
          onClick={() => setActiveTab('home')}
          id="nav-btn-home"
        >
          <Home size={15} />
          <span>Home</span>
        </button>

        <button
          className={`nav-btn ${activeTab === 'browse_find' ? 'active' : ''}`}
          onClick={() => setActiveTab('browse_find')}
          id="nav-btn-browse-find"
        >
          <Compass size={15} />
          <span>Browse & Find</span>
        </button>

        <button
          className={`nav-btn ${activeTab === 'smart_match' ? 'active' : ''}`}
          onClick={() => setActiveTab('smart_match')}
          id="nav-btn-smart-match"
        >
          <Sliders size={15} />
          <span>Smart Match</span>
        </button>
      </nav>

      <div className="nav-actions">
        {/* Interactive Session Ratings Button */}
        <button
          className={`session-ratings-pill ${sessionRatingsCount > 0 ? 'has-ratings' : ''}`}
          onClick={onOpenRatedModal}
          title="View & manage your rated anime"
          id="btn-rated-anime"
          aria-label="View rated anime"
        >
          <Star size={13} className={sessionRatingsCount > 0 ? 'star-active' : ''} />
          <span>{sessionRatingsCount} Rated</span>
        </button>

        {/* Theme Switcher */}
        <button
          className="theme-toggle-btn"
          onClick={toggleTheme}
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
          id="btn-theme-toggle"
        >
          {theme === 'dark' ? (
            <>
              <Sun size={15} />
              <span className="theme-toggle-label">Light</span>
            </>
          ) : (
            <>
              <Moon size={15} />
              <span className="theme-toggle-label">Dark</span>
            </>
          )}
        </button>
      </div>
    </header>
  );
}
