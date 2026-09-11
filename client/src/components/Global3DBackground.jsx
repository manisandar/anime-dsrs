import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function Global3DBackground({ theme = 'dark' }) {
  const mountRef = useRef(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    let animationFrameId;
    let isPageVisible = true;

    // 1. Scene & Camera
    const scene = new THREE.Scene();
    let width = window.innerWidth;
    let height = window.innerHeight;

    const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    camera.position.z = 32;

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance',
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0); // Full transparency
    container.appendChild(renderer.domElement);

    // 2. Color Scheme based on theme
    const isDark = theme === 'dark';
    const primaryColor = isDark ? 0xe50914 : 0x2563eb;
    const secondaryColor = isDark ? 0x9333ea : 0x6366f1;
    const accentColor = isDark ? 0x38bdf8 : 0x0ea5e9;

    // 3. Floating 3D Geometric Structure (Geodesic Polyhedron Wireframe & Rings)
    const group = new THREE.Group();
    scene.add(group);

    // Outer Geodesic Sphere
    const geoIcosa = new THREE.IcosahedronGeometry(14, 2);
    const matIcosa = new THREE.MeshBasicMaterial({
      color: secondaryColor,
      wireframe: true,
      transparent: true,
      opacity: isDark ? 0.08 : 0.05,
    });
    const icosaMesh = new THREE.Mesh(geoIcosa, matIcosa);
    group.add(icosaMesh);

    // Central Orbital Ring 1
    const geoRing1 = new THREE.TorusGeometry(18, 0.25, 12, 100);
    const matRing1 = new THREE.MeshBasicMaterial({
      color: primaryColor,
      wireframe: true,
      transparent: true,
      opacity: isDark ? 0.14 : 0.08,
    });
    const ring1 = new THREE.Mesh(geoRing1, matRing1);
    ring1.rotation.x = Math.PI * 0.35;
    group.add(ring1);

    // Central Orbital Ring 2 (Cross angle)
    const geoRing2 = new THREE.TorusGeometry(22, 0.2, 12, 120);
    const matRing2 = new THREE.MeshBasicMaterial({
      color: accentColor,
      wireframe: true,
      transparent: true,
      opacity: isDark ? 0.09 : 0.05,
    });
    const ring2 = new THREE.Mesh(geoRing2, matRing2);
    ring2.rotation.y = Math.PI * 0.4;
    ring2.rotation.x = Math.PI * 0.15;
    group.add(ring2);

    // 4. Interactive Particle Constellation System
    const particleCount = 380;
    const particleGeo = new THREE.BufferGeometry();
    const origPositions = new Float32Array(particleCount * 3);
    const currentPositions = new Float32Array(particleCount * 3);
    const velocities = new Float32Array(particleCount * 3);
    const particleColors = new Float32Array(particleCount * 3);

    const c1 = new THREE.Color(primaryColor);
    const c2 = new THREE.Color(secondaryColor);
    const c3 = new THREE.Color(accentColor);

    for (let i = 0; i < particleCount; i++) {
      const x = (Math.random() - 0.5) * 65;
      const y = (Math.random() - 0.5) * 45;
      const z = (Math.random() - 0.5) * 40;

      origPositions[i * 3] = x;
      origPositions[i * 3 + 1] = y;
      origPositions[i * 3 + 2] = z;

      currentPositions[i * 3] = x;
      currentPositions[i * 3 + 1] = y;
      currentPositions[i * 3 + 2] = z;

      velocities[i * 3] = 0;
      velocities[i * 3 + 1] = 0;
      velocities[i * 3 + 2] = 0;

      // Color variation across nodes
      const rand = Math.random();
      const col = rand < 0.45 ? c1 : rand < 0.8 ? c2 : c3;
      particleColors[i * 3] = col.r;
      particleColors[i * 3 + 1] = col.g;
      particleColors[i * 3 + 2] = col.b;
    }

    particleGeo.setAttribute('position', new THREE.BufferAttribute(currentPositions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

    const particleMat = new THREE.PointsMaterial({
      size: isDark ? 0.45 : 0.38,
      vertexColors: true,
      transparent: true,
      opacity: isDark ? 0.82 : 0.55,
      blending: isDark ? THREE.AdditiveBlending : THREE.NormalBlending,
    });

    const particles = new THREE.Points(particleGeo, particleMat);
    group.add(particles);

    // 5. Dynamic Constellation Line Connections (Network Mesh)
    const maxLineSegments = 220;
    const linePositions = new Float32Array(maxLineSegments * 6);
    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));

    const lineMat = new THREE.LineBasicMaterial({
      color: secondaryColor,
      transparent: true,
      opacity: isDark ? 0.15 : 0.08,
      blending: isDark ? THREE.AdditiveBlending : THREE.NormalBlending,
    });
    const lineSegments = new THREE.LineSegments(lineGeo, lineMat);
    group.add(lineSegments);

    // 6. Interactive Click Ripple Waves (Shockwaves)
    // Stores up to 6 concurrent click shockwaves in 3D space
    const ripples = [];
    const maxRipples = 6;

    const onPointerDown = (e) => {
      // Map screen coords (0 to width/height) to normalized 3D plane at z = 0
      const normX = (e.clientX / window.innerWidth) * 2 - 1;
      const normY = -(e.clientY / window.innerHeight) * 2 + 1;

      // Unproject to find world coordinates at camera focal distance
      const vector = new THREE.Vector3(normX, normY, 0.5);
      vector.unproject(camera);
      const dir = vector.sub(camera.position).normalize();
      const distance = -camera.position.z / dir.z;
      const clickWorldPos = camera.position.clone().add(dir.multiplyScalar(distance));

      ripples.push({
        x: clickWorldPos.x,
        y: clickWorldPos.y,
        z: clickWorldPos.z,
        radius: 0,
        maxRadius: 35,
        speed: 28.0,
        strength: 8.5,
        opacity: 1.0,
        startTime: performance.now(),
      });

      if (ripples.length > maxRipples) {
        ripples.shift();
      }
    };

    window.addEventListener('pointerdown', onPointerDown, { passive: true });

    // 7. Mouse Movement Parallax
    let targetRotX = 0;
    let targetRotY = 0;
    let currentRotX = 0;
    let currentRotY = 0;

    const onMouseMove = (e) => {
      const nx = (e.clientX / window.innerWidth) - 0.5;
      const ny = (e.clientY / window.innerHeight) - 0.5;
      targetRotY = nx * 0.45;
      targetRotX = ny * 0.35;
    };

    window.addEventListener('mousemove', onMouseMove, { passive: true });

    // 8. Window Resize
    const onResize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };

    window.addEventListener('resize', onResize);

    // 9. Visibility Observer (Pause when tab is hidden to save CPU/GPU)
    const handleVisibilityChange = () => {
      isPageVisible = !document.hidden;
    };
    document.addEventListener('visibilitychange', handleVisibilityChange);

    // 10. Main Animation Loop with Physics Spring and Shockwave Propagation
    let lastTime = performance.now();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      if (!isPageVisible) return;

      const now = performance.now();
      const dt = Math.min((now - lastTime) * 0.001, 0.1);
      lastTime = now;

      // Smooth mouse parallax lerp
      currentRotX += (targetRotX - currentRotX) * 0.04;
      currentRotY += (targetRotY - currentRotY) * 0.04;

      // Ambient geometric rotation
      group.rotation.y += 0.0015;
      group.rotation.x = currentRotX * 0.8;
      group.rotation.z = currentRotY * 0.6;

      icosaMesh.rotation.x += 0.002;
      icosaMesh.rotation.y += 0.003;
      ring1.rotation.z += 0.004;
      ring2.rotation.z -= 0.003;

      // Update ripples
      for (let r = ripples.length - 1; r >= 0; r--) {
        const rip = ripples[r];
        rip.radius += rip.speed * dt;
        rip.opacity = Math.max(0, 1.0 - rip.radius / rip.maxRadius);
        if (rip.radius > rip.maxRadius) {
          ripples.splice(r, 1);
        }
      }

      // Physics update on particles (Spring restoration + Click shockwave displacement)
      const posArr = particleGeo.attributes.position.array;

      for (let i = 0; i < particleCount; i++) {
        const idx = i * 3;
        let px = posArr[idx];
        let py = posArr[idx + 1];
        let pz = posArr[idx + 2];

        const ox = origPositions[idx];
        const oy = origPositions[idx + 1];
        const oz = origPositions[idx + 2];

        // 1. Spring force back to equilibrium
        let fx = (ox - px) * 2.8;
        let fy = (oy - py) * 2.8;
        let fz = (oz - pz) * 2.8;

        // 2. Shockwave impulse from all active ripples
        for (let r = 0; r < ripples.length; r++) {
          const rip = ripples[r];
          const dx = px - rip.x;
          const dy = py - rip.y;
          const dz = pz - rip.z;
          const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

          // Wave shell thickness of 4 units
          const waveDist = Math.abs(dist - rip.radius);
          if (waveDist < 4.0 && dist > 0.01) {
            const factor = (1.0 - waveDist / 4.0) * rip.opacity * rip.strength;
            const invDist = 1.0 / dist;
            fx += dx * invDist * factor * 14.0;
            fy += dy * invDist * factor * 14.0;
            fz += dz * invDist * factor * 14.0;
          }
        }

        // Apply velocity with damping
        velocities[idx] = (velocities[idx] + fx * dt) * 0.88;
        velocities[idx + 1] = (velocities[idx + 1] + fy * dt) * 0.88;
        velocities[idx + 2] = (velocities[idx + 2] + fz * dt) * 0.88;

        posArr[idx] += velocities[idx] * dt;
        posArr[idx + 1] += velocities[idx + 1] * dt;
        posArr[idx + 2] += velocities[idx + 2] * dt;
      }
      particleGeo.attributes.position.needsUpdate = true;

      // Update Constellation dynamic lines between nearby points
      let lineIdx = 0;
      const lineArray = lineGeo.attributes.position.array;
      const connectionDistSq = 45; // connect if distance < ~6.7 units

      for (let i = 0; i < 70 && lineIdx < maxLineSegments * 6; i++) {
        const i3 = i * 3;
        for (let j = i + 1; j < 70 && lineIdx < maxLineSegments * 6; j++) {
          const j3 = j * 3;
          const dx = posArr[i3] - posArr[j3];
          const dy = posArr[i3 + 1] - posArr[j3 + 1];
          const dz = posArr[i3 + 2] - posArr[j3 + 2];
          const distSq = dx * dx + dy * dy + dz * dz;

          if (distSq < connectionDistSq) {
            lineArray[lineIdx++] = posArr[i3];
            lineArray[lineIdx++] = posArr[i3 + 1];
            lineArray[lineIdx++] = posArr[i3 + 2];
            lineArray[lineIdx++] = posArr[j3];
            lineArray[lineIdx++] = posArr[j3 + 1];
            lineArray[lineIdx++] = posArr[j3 + 2];
          }
        }
      }
      // Fill remaining line slots with zeros
      while (lineIdx < maxLineSegments * 6) {
        lineArray[lineIdx++] = 0;
      }
      lineGeo.attributes.position.needsUpdate = true;

      renderer.render(scene, camera);
    };

    animate();

    // 11. Cleanup
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('pointerdown', onPointerDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('resize', onResize);
      document.removeEventListener('visibilitychange', handleVisibilityChange);

      geoIcosa.dispose();
      matIcosa.dispose();
      geoRing1.dispose();
      matRing1.dispose();
      geoRing2.dispose();
      matRing2.dispose();
      particleGeo.dispose();
      particleMat.dispose();
      lineGeo.dispose();
      lineMat.dispose();
      renderer.dispose();

      if (renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [theme]);

  return (
    <div
      ref={mountRef}
      className="global-3d-background-canvas"
      aria-hidden="true"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: 0,
        pointerEvents: 'none',
        overflow: 'hidden',
      }}
    />
  );
}
