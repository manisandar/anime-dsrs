import React from 'react';

/**
 * Simple, clear, static background for ANIVIBE.
 * Replaces moving 3D objects/particles with a clean, high-clarity static ambient aesthetic.
 */
export default function Global3DBackground({ theme = 'dark' }) {
  const isDark = theme === 'dark';

  return (
    <div
      className="global-static-backdrop"
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: -1,
        pointerEvents: 'none',
        background: isDark
          ? 'radial-gradient(ellipse at 50% 0%, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.95) 75%, #0b0f19 100%)'
          : 'radial-gradient(ellipse at 50% 0%, rgba(241, 245, 249, 0.8) 0%, rgba(248, 250, 252, 0.98) 75%, #f8fafc 100%)',
        transition: 'background 0.3s ease'
      }}
    />
  );
}
