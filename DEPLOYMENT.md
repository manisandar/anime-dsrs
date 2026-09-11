# ANIVIBE Deployment Guide: 100% Free Hosting

Because you are using the **free version** of Hugging Face Spaces (where Docker is paid/restricted and **Static is 100% free**), ANIVIBE has been equipped with a pure client-side academic recommender engine (`localEngine.js`).

This means the entire system — **Bayesian Popularity, 29-Genre Cosine Similarity CBF, Knowledge-Based Constraints, and 1+1 Hybrid Fusion** — runs directly in the browser with **0ms latency, zero backend servers, zero maintenance, and 100% free hosting forever**.

---

## 🌟 METHOD 1: Hugging Face Spaces (Static SDK — 100% Free Forever)

All production-ready files have already been built and packaged inside the folder:
```
deploy/huggingface_static/
```

### Step 1: Create a Static Space on Hugging Face
1. Log in to [Hugging Face](https://huggingface.co/).
2. In the top-right corner, click your profile avatar and select **"New Space"** (or go directly to [huggingface.co/new-space](https://huggingface.co/new-space)).
3. Configure the Space:
   - **Space name**: e.g. `anivibe-anime` (or any name you like)
   - **License**: `mit`
   - **Space SDK**: Choose **Static** (HTML / JavaScript) 👈 *This is 100% Free with no hardware fees or credit cards*
   - **Visibility**: **Public**
4. Click **"Create Space"**.

### Step 2: Upload Files
#### Option A: Drag & Drop via Web Browser (Easiest - 1 minute)
1. On your new Hugging Face Space page, click the **"Files"** tab.
2. Click **"Add file"** ➔ **"Upload files"**.
3. From your computer, open `deploy/huggingface_static/` and drag all files into the upload box:
   - `README.md` (Contains the Hugging Face static metadata)
   - `index.html`
   - `anime_catalog.json` (The 1,255 anime catalog)
   - `favicon.svg`
   - `icons.svg`
   - The `assets/` folder (Contains all compiled CSS and JavaScript)
4. Scroll down and click **"Commit changes to main"**.
5. Hugging Face will immediately serve the site! You will receive a live URL:
   ```
   https://YOUR_HF_USERNAME-anivibe-anime.hf.space
   ```

#### Option B: Via Terminal / Git Command Line
```bash
# 1. Clone your empty Hugging Face Static Space
git clone https://huggingface.co/spaces/YOUR_HF_USERNAME/anivibe-anime

# 2. Copy the static files into your space repository
cp -r deploy/huggingface_static/* anivibe-anime/

# 3. Commit and push
cd anivibe-anime
git add .
git commit -m "Deploy ANIVIBE 100% Free Static Recommender"
git push
```

---

## 🚀 METHOD 2: Deploy Frontend to Vercel (100% Free)

If you prefer Vercel or want both Hugging Face and Vercel:

### Step 1: Push Project to GitHub
1. Create a repository on [GitHub](https://github.com/new) named `anime-dsrs`.
2. In your local terminal:
```bash
git add .
git commit -m "ANIVIBE Decision Support & Recommendation System"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/anime-dsrs.git
git push -u origin main
```

### Step 2: Connect to Vercel
1. Log in to [Vercel](https://vercel.com/) with GitHub.
2. Click **"Add New..."** ➔ **"Project"**.
3. Import your `anime-dsrs` repository.
4. Set the build settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click **Edit** and choose `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Click **"Deploy"**.
6. Vercel will build and give you a free `.vercel.app` URL in ~20 seconds!

---

## ⚡ How the 100% Free Architecture Works
```
┌─────────────────────────────────────────────────────────────┐
│       Hugging Face Static Space or Vercel (100% Free)       │
│                                                             │
│  ┌─────────────────────────┐   ┌─────────────────────────┐  │
│  │     React UI Bundle     │   │   anime_catalog.json    │  │
│  │   (Vite + Lucide Icons) │   │     (1,255 Records)     │  │
│  └────────────┬────────────┘   └────────────┬────────────┘  │
│               │                             │               │
│               ▼                             ▼               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Academic Client Engine (localEngine.js)        │  │
│  │                                                       │  │
│  │  1. Popularity: Bayesian Weighted Rating              │  │
│  │  2. Content-Based: 29-Genre Cosine Similarity         │  │
│  │  3. Knowledge-Based: Constraint & Mood Rules          │  │
│  │  4. 1+1 Hybrid: 50% CBF Taste + 50% KBR Fit           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

- **Zero backend server costs**: No paid Python or Docker instances required.
- **Zero API rate limits or downtime**: Evaluates all math directly in the user's browser in < 3 milliseconds.
- **Offline / Local Storage**: User ratings and session history persist directly in the browser's `localStorage`.
- **Hybrid fallback**: If you ever want to connect a live Express or Python backend later, just set `ANIME_DSRS_API_URL` or `VITE_API_URL`; the app will automatically use it and smoothly fallback to the static engine if offline.
