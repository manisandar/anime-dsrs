#!/usr/bin/env bash
set -e

# ==============================================================================
# ANIVIBE Automated Deployment Script for Hugging Face Spaces (Static SDK)
# ==============================================================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "🚀 [1/3] Building latest ANIVIBE Client..."
cd "$ROOT_DIR/client"
npm run build

echo "📦 [2/3] Bundling static files into deploy/huggingface_static/..."
mkdir -p "$ROOT_DIR/deploy/huggingface_static"
cp -r "$ROOT_DIR/client/dist/"* "$ROOT_DIR/deploy/huggingface_static/"

# Ensure README.md with static space metadata is present
cat << 'EOF' > "$ROOT_DIR/deploy/huggingface_static/README.md"
---
title: ANIVIBE Anime DSRS
emoji: 🎬
colorFrom: indigo
colorTo: purple
sdk: static
pinned: false
license: mit
---

# ANIVIBE — Anime Decision Support & Recommendation System
Academic Recommendation Platform | Assumption University CSX/ITX 4207
EOF

echo "☁️ [3/3] Uploading updates to Hugging Face Space (minkhanttin/anivibe)..."
cd "$ROOT_DIR"
hf upload --repo-type space minkhanttin/anivibe deploy/huggingface_static . --commit-message "Update ANIVIBE static deployment"

echo "✅ Deployment completed! Live at: https://minkhanttin-anivibe.static.hf.space"
