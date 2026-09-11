import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import BrowseAndFindPage from './pages/BrowseAndFindPage';
import SmartMatchPage from './pages/SmartMatchPage';
import AnimeDetailPage from './pages/AnimeDetailPage';
import Global3DBackground from './components/Global3DBackground';
import RatedAnimeModal from './components/RatedAnimeModal';
import { api } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('home'); // 'home' | 'browse_find' | 'smart_match'
  const [browseFindMode, setBrowseFindMode] = useState('browse'); // 'browse' | 'kbr'
  const [selectedAnime, setSelectedAnime] = useState(null);
  const [showRatedModal, setShowRatedModal] = useState(false);
  const [sessionRatings, setSessionRatings] = useState(() => {
    try {
      const saved = localStorage.getItem('ANIVIBE_SESSION_RATINGS');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });

  // Theme state: dark (default) or light
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('ANIVIBE_THEME') || 'dark';
  });

  useEffect(() => {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('ANIVIBE_THEME', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const handleRate = async (animeId, rating) => {
    setSessionRatings((prev) => {
      const existing = prev.find((r) => r.anime_id === animeId);
      const updated = existing
        ? prev.map((r) => (r.anime_id === animeId ? { ...r, rating } : r))
        : [...prev, { anime_id: animeId, rating }];
      try {
        localStorage.setItem('ANIVIBE_SESSION_RATINGS', JSON.stringify(updated));
      } catch (e) {}
      return updated;
    });

    try {
      await api.submitRating({
        userId: 1,
        animeId,
        rating
      });
    } catch (err) {
      console.warn('Rating submission note:', err);
    }
  };

  const handleRemoveRating = (animeId) => {
    setSessionRatings((prev) => {
      const updated = prev.filter((r) => r.anime_id !== animeId);
      try {
        localStorage.setItem('ANIVIBE_SESSION_RATINGS', JSON.stringify(updated));
      } catch (e) {}
      return updated;
    });
  };

  const handleClearRatings = () => {
    setSessionRatings([]);
    try {
      localStorage.removeItem('ANIVIBE_SESSION_RATINGS');
    } catch (e) {}
  };

  const handleNavigate = (tab, options = {}) => {
    setSelectedAnime(null);
    setActiveTab(tab);
    if (options.mode) {
      setBrowseFindMode(options.mode);
    } else {
      setBrowseFindMode('browse');
    }
  };

  return (
    <>
      {/* 3D INTERACTIVE STRUCTURE BEHIND ALL PAGES */}
      <Global3DBackground theme={theme} />

      <div className="app-container">
        <Navbar
          activeTab={activeTab}
          setActiveTab={(tab) => {
            setSelectedAnime(null);
            setActiveTab(tab);
            if (tab === 'browse_find') setBrowseFindMode('browse');
          }}
          theme={theme}
          toggleTheme={toggleTheme}
          sessionRatingsCount={sessionRatings.length}
          onOpenRatedModal={() => setShowRatedModal(true)}
        />

        {/* RENDER ACTIVE PAGE (EXACTLY 4 MAIN PAGES) */}
        {selectedAnime ? (
          <AnimeDetailPage
            anime={selectedAnime}
            onBack={() => setSelectedAnime(null)}
            onSelectAnime={(sim) => setSelectedAnime(sim)}
            sessionRatings={sessionRatings}
            onRate={handleRate}
          />
        ) : activeTab === 'home' ? (
          <HomePage
            onSelectAnime={(anime) => setSelectedAnime(anime)}
            sessionRatings={sessionRatings}
            onRate={handleRate}
            onNavigate={handleNavigate}
            theme={theme}
          />
        ) : activeTab === 'browse_find' ? (
          <BrowseAndFindPage
            key={browseFindMode}
            onSelectAnime={(anime) => setSelectedAnime(anime)}
            sessionRatings={sessionRatings}
            onRate={handleRate}
            initialMode={browseFindMode}
          />
        ) : (
          <SmartMatchPage
            onSelectAnime={(anime) => setSelectedAnime(anime)}
            sessionRatings={sessionRatings}
            onRate={handleRate}
            onNavigate={handleNavigate}
          />
        )}

        {/* RATED MOVIES / ANIME MODAL */}
        <RatedAnimeModal
          isOpen={showRatedModal}
          onClose={() => setShowRatedModal(false)}
          sessionRatings={sessionRatings}
          onRate={handleRate}
          onRemoveRating={handleRemoveRating}
          onClearRatings={handleClearRatings}
          onSelectAnime={(anime) => setSelectedAnime(anime)}
          onNavigate={handleNavigate}
        />
      </div>
    </>
  );
}
