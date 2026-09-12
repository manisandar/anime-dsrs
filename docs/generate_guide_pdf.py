#!/usr/bin/env python3
"""
Generates an executive, highly readable PDF guide for ANIVIBE.
- Body font size minimum of 13.5px (clean, large, legible).
- Minimal words, punchy bullet points, no dense text or equations.
- Visually appealing alternating pastel background cards.
- Clear page-by-page structure with comfortable spacing.
"""

import os
import subprocess

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ANIVIBE — Decision Support & Recommender Systems Page Guide</title>
<style>
  @page {
    size: A4;
    margin: 14mm 16mm 14mm 16mm;
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    background: #ffffff;
    line-height: 1.6;
    font-size: 13.5px;
    margin: 0;
    padding: 0;
  }

  /* Document Header */
  .header {
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 12px;
    margin-bottom: 16px;
  }
  .header-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 3px 9px;
    border-radius: 5px;
    background: #ede9fe;
    color: #6d28d9;
    margin-bottom: 6px;
  }
  h1 {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 6px 0;
    letter-spacing: -0.4px;
  }
  .subtitle {
    font-size: 13.5px;
    color: #475569;
    margin: 0 0 10px 0;
  }
  .meta-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    font-size: 12px;
    color: #475569;
  }
  .meta-bar strong {
    color: #0f172a;
  }

  /* Page Break Rule */
  .page-break {
    page-break-before: always;
  }

  /* Section Title */
  .section-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1.5px solid #e2e8f0;
  }
  .section-title {
    font-size: 18px;
    font-weight: 800;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .route-pill {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 12px;
    background: #f1f5f9;
    padding: 3px 8px;
    border-radius: 5px;
    color: #334155;
    font-weight: 600;
  }
  .role-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .role-purple { background: #ede9fe; color: #6d28d9; }
  .role-blue   { background: #e0f2fe; color: #0369a1; }
  .role-amber  { background: #fef3c7; color: #b45309; }
  .role-green  { background: #dcfce7; color: #15803d; }

  /* User Goal Callout */
  .goal-callout {
    background: #f8fafc;
    border-left: 4px solid #94a3b8;
    padding: 8px 14px;
    margin-bottom: 14px;
    border-radius: 0 8px 8px 0;
    font-size: 13.5px;
    color: #334155;
  }
  .goal-callout strong {
    color: #0f172a;
  }

  /* Appealing Alternating Cards */
  .feature-card {
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 12px;
    page-break-inside: avoid;
  }
  
  /* Alternating Colors */
  .theme-violet {
    background: #faf5ff;
    border: 1px solid #e9d5ff;
  }
  .theme-sky {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
  }
  .theme-mint {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
  }
  .theme-amber {
    background: #fffbeb;
    border: 1px solid #fde68a;
  }
  .theme-rose {
    background: #fff1f2;
    border: 1px solid #fecdd3;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  .card-title {
    font-size: 15.5px;
    font-weight: 700;
    color: #0f172a;
  }
  .type-tag {
    font-size: 10.5px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
  }
  .tag-rec { background: #ede9fe; color: #6d28d9; }
  .tag-dec { background: #dbeafe; color: #1d4ed8; }
  .tag-both { background: #dcfce7; color: #15803d; }

  /* Compact Bullet Points */
  ul.points {
    margin: 0;
    padding-left: 20px;
  }
  ul.points li {
    margin-bottom: 5px;
    color: #334155;
    font-size: 13.5px;
  }
  ul.points li:last-child {
    margin-bottom: 0;
  }
  ul.points strong {
    color: #0f172a;
  }

  /* Summary Table */
  .summary-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    font-size: 12.5px;
    border-radius: 8px;
    overflow: hidden;
  }
  .summary-table th, .summary-table td {
    padding: 9px 12px;
    border: 1px solid #e2e8f0;
    text-align: left;
  }
  .summary-table th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
  }
  .summary-table tr:nth-child(even) td {
    background: #f8fafc;
  }

  /* Defense Summary Box */
  .defense-card {
    background: #f0fdf4;
    border: 1.5px solid #86efac;
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 14px;
  }
  .defense-title {
    font-size: 15px;
    font-weight: 800;
    color: #166534;
    margin-bottom: 6px;
  }
  .defense-card p {
    margin: 0;
    font-size: 13.5px;
    color: #1e3a24;
    line-height: 1.55;
  }

  /* Footer */
  .footer {
    border-top: 1px solid #e2e8f0;
    padding-top: 8px;
    margin-top: 16px;
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #94a3b8;
  }
</style>
</head>
<body>

  <!-- ==================== SHEET 1: HOME PAGE ==================== -->
  <div class="header">
    <div class="header-tag">Executive Systems Reference</div>
    <h1>ANIVIBE — Decision Support & Recommender Guide</h1>
    <div class="subtitle">Clean, Page-by-Page Architectural Breakdown (Zero Equations • Plain English)</div>
    <div class="meta-bar">
      <div><strong>Course:</strong> CSX/ITX 4207 Decision Support Systems</div>
      <div><strong>Institution:</strong> Assumption University</div>
      <div><strong>Live Demo:</strong> minkhanttin-anivibe.static.hf.space</div>
    </div>
  </div>

  <div class="section-banner">
    <div class="section-title">
      <span>1. Home Page</span>
      <span class="route-pill">/</span>
    </div>
    <span class="role-badge role-purple">Popularity & Personalization</span>
  </div>

  <div class="goal-callout">
    <strong>User Goal:</strong> Immediate discovery. Delivers safe recommendations for new visitors and an evolving, personalized feed for users who rate shows.
  </div>

  <!-- Card 1: Popular Right Now (Violet Tint) -->
  <div class="feature-card theme-violet">
    <div class="card-header">
      <span class="card-title">1. Popular Right Now</span>
      <span class="type-tag tag-rec">Popularity-Based Recommender</span>
    </div>
    <ul class="points">
      <li><strong>What it does:</strong> Ranks anime by combining high rating scores with total review volume so titles with thousands of votes outrank one-off 5-star reviews.</li>
      <li><strong>Why we use it:</strong> Solves the <em>Cold-Start problem</em>. When a new visitor has 0 ratings, the system provides verified, trusted community classics immediately.</li>
      <li><strong>User Benefit:</strong> Instant viewing without having to search or set preferences.</li>
    </ul>
  </div>

  <!-- Card 2: Recommended For You (Sky Blue Tint) -->
  <div class="feature-card theme-sky">
    <div class="card-header">
      <span class="card-title">2. Recommended For You</span>
      <span class="type-tag tag-rec">Content-Based Filtering</span>
    </div>
    <ul class="points">
      <li><strong>What it does:</strong> Learns your taste from your 1 to 5-star ratings. High ratings boost preferred genres; low ratings penalize unwanted themes.</li>
      <li><strong>Why we use it:</strong> Automatically curates unrated anime that match your individual personality.</li>
      <li><strong>User Benefit:</strong> Eliminates browsing fatigue by showing shows you are statistically likely to enjoy.</li>
    </ul>
  </div>

  <!-- Card 3: Decision Onboarding Banner (Mint Tint) -->
  <div class="feature-card theme-mint">
    <div class="card-header">
      <span class="card-title">3. Interactive Onboarding Banner</span>
      <span class="type-tag tag-dec">Decision Support Prompt</span>
    </div>
    <ul class="points">
      <li><strong>What it does:</strong> Prompts first-time visitors to rate their first 1–2 titles with quick-click stars.</li>
      <li><strong>Why we use it:</strong> Actively guides users to calibrate the recommendation engine.</li>
    </ul>
  </div>

  <div class="footer">
    <div>ANIVIBE Architectural Guide — Assumption University</div>
    <div>Page 1 of 4</div>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SHEET 2: DETAIL & BROWSE ==================== -->

  <!-- SECTION 2: ANIME DETAIL PAGE -->
  <div class="section-banner">
    <div class="section-title">
      <span>2. Anime Detail Page</span>
      <span class="route-pill">/anime/:id</span>
    </div>
    <span class="role-badge role-blue">Item Similarity & Evidence</span>
  </div>

  <div class="goal-callout">
    <strong>User Goal:</strong> Deciding whether a specific anime is worth your free time before committing hours or weeks to watch it.
  </div>

  <!-- Card 1: More Like This (Amber Tint) -->
  <div class="feature-card theme-amber">
    <div class="card-header">
      <span class="card-title">1. More Like This (Netflix-Style Carousel)</span>
      <span class="type-tag tag-rec">Item-to-Item Content Filtering</span>
    </div>
    <ul class="points">
      <li><strong>What it does:</strong> Analyzes the genre profile of the anime on screen and recommends the closest sister titles in the catalog.</li>
      <li><strong>Why we use it:</strong> Works independently of user rating history. If you loved this show, you can instantly find similar ones with one click.</li>
    </ul>
  </div>

  <!-- Card 2: Viewer Rating Distribution (Rose Tint) -->
  <div class="feature-card theme-rose">
    <div class="card-header">
      <span class="card-title">2. Viewer Rating Distribution Histogram</span>
      <span class="type-tag tag-dec">Community Consensus Support</span>
    </div>
    <ul class="points">
      <li><strong>What it does:</strong> Displays an amber bar breakdown showing the percentage of 5-star, 4-star, down to 1-star ratings.</li>
      <li><strong>Decision Support Value:</strong> An average rating (e.g. 4.1) hides controversy. The histogram reveals whether an anime is universally loved or polarizing.</li>
    </ul>
  </div>

  <!-- SECTION 3: BROWSE & FIND PAGE -->
  <div class="section-banner" style="margin-top: 16px;">
    <div class="section-title">
      <span>3. Browse & Find Page</span>
      <span class="route-pill">/browse</span>
    </div>
    <span class="role-badge role-green">Search & Rule Advisory</span>
  </div>

  <!-- Card 3: Mode A - Catalog Discovery (Sky Tint) -->
  <div class="feature-card theme-sky">
    <div class="card-header">
      <span class="card-title">Mode A: Catalog Discovery</span>
      <span class="type-tag tag-dec">Exploratory Decision Support</span>
    </div>
    <ul class="points">
      <li><strong>What it does:</strong> Live search, genre filter pills, and multi-criteria sorting (by community popularity, review score, or title).</li>
      <li><strong>Why we use it:</strong> Empowers self-guided browsing when users want to explore a single category.</li>
    </ul>
  </div>

  <!-- Card 4: Mode B - Find What Fits (Violet Tint) -->
  <div class="feature-card theme-violet">
    <div class="card-header">
      <span class="card-title">Mode B: Find What Fits</span>
      <span class="type-tag tag-rec">Knowledge-Based Recommender (KBR)</span>
    </div>
    <ul class="points">
      <li><strong>What it does:</strong> Acts as an expert advisor. You set your situational boundaries:
        <ul>
          <li><strong>Episode Ceiling:</strong> e.g. Maximum 26 episodes for a weekend binge.</li>
          <li><strong>Quality Threshold:</strong> e.g. Ratings &ge; 4.0 stars only.</li>
          <li><strong>Genre Constraints:</strong> Must include Mystery, strictly exclude Horror.</li>
          <li><strong>Emotional Mood:</strong> Exciting, Chill, Dark, or Emotional.</li>
        </ul>
      </li>
      <li><strong>Explainable Verdicts:</strong> Every card shows an itemized checklist of which rules passed.</li>
    </ul>
  </div>

  <div class="footer">
    <div>ANIVIBE Architectural Guide — Assumption University</div>
    <div>Page 2 of 4</div>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SHEET 3: SMART MATCH & DECISION CENTER ==================== -->

  <!-- SECTION 4: SMART MATCH PAGE -->
  <div class="section-banner">
    <div class="section-title">
      <span>4. Smart Match Page (Flagship)</span>
      <span class="route-pill">/smart-match</span>
    </div>
    <span class="role-badge role-purple">1+1 Hybrid Fusion</span>
  </div>

  <div class="goal-callout">
    <strong>User Goal:</strong> Solves the real-world dilemma: <em>"I want a show that fits my authentic personal taste, but also fits my available time and mood right now."</em>
  </div>

  <!-- Card 1: 1+1 Hybrid Recommender (Mint Tint) -->
  <div class="feature-card theme-mint">
    <div class="card-header">
      <span class="card-title">1+1 Hybrid Fusion Recommender</span>
      <span class="type-tag tag-both">Hybrid Recommender + Decision Support</span>
    </div>
    <ul class="points">
      <li><strong>What it does:</strong> Calculates two distinct scores and fuses them 50/50:
        <ul>
          <li><strong>50% Taste Score (Content-Based):</strong> Does this match your past rating preferences?</li>
          <li><strong>50% Fit Score (Knowledge-Based):</strong> Does this fit your current episode limit and mood?</li>
        </ul>
      </li>
      <li><strong>Why it's essential:</strong>
        Pure taste filtering might recommend a 500-episode show when you only have one evening free.
        Pure constraint filtering might find a short show in a genre you dislike.
        The 1+1 Hybrid guarantees you get a title you love <strong>and</strong> have time to finish.
      </li>
      <li><strong>Dual-Score Transparency:</strong> Result cards display separate <strong>Taste Match %</strong> and <strong>Requirement Fit %</strong> bars for complete clarity.</li>
    </ul>
  </div>

  <!-- SECTION 5: DECISION CENTER -->
  <div class="section-banner" style="margin-top: 18px;">
    <div class="section-title">
      <span>5. Decision Center</span>
      <span class="route-pill">/decision-center</span>
    </div>
    <span class="role-badge role-amber">Comparative Decision Analysis</span>
  </div>

  <div class="goal-callout">
    <strong>User Goal:</strong> Resolves final indecision when torn between 2 or 3 finalist anime.
  </div>

  <!-- Card 2: Side-by-Side Matrix (Amber Tint) -->
  <div class="feature-card theme-amber">
    <div class="card-header">
      <span class="card-title">Multi-Criteria Decision Matrix</span>
      <span class="type-tag tag-dec">Multi-Criteria Decision Analysis (MCDA)</span>
    </div>
    <ul class="points">
      <li><strong>What it does:</strong> Places up to 3 selected anime side-by-side in a comparative matrix.</li>
      <li><strong>Trade-Off Factors Compared:</strong> Total episodes, hours to complete, community review counts, 5-star vs 1-star ratios, and genre overlap.</li>
      <li><strong>Decision Benefit:</strong> Eliminates tab clutter and mental overload by presenting all trade-offs on one screen.</li>
    </ul>
  </div>

  <div class="footer">
    <div>ANIVIBE Architectural Guide — Assumption University</div>
    <div>Page 3 of 4</div>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SHEET 4: BENCHMARKS & SUMMARY ==================== -->

  <!-- SECTION 6: ACADEMIC BENCHMARKS -->
  <div class="section-banner">
    <div class="section-title">
      <span>6. Academic Benchmarks Page</span>
      <span class="route-pill">/benchmarks</span>
    </div>
    <span class="role-badge role-blue">Model Evaluation</span>
  </div>

  <div class="goal-callout">
    <strong>User Goal:</strong> Provides instructors and evaluators with empirical proof of model performance.
  </div>

  <!-- Card 1: Benchmark Dashboard (Sky Tint) -->
  <div class="feature-card theme-sky">
    <div class="card-header">
      <span class="card-title">Empirical Benchmark Evaluation</span>
      <span class="type-tag tag-dec">Scientific Validation</span>
    </div>
    <ul class="points">
      <li><strong>Metrics Evaluated:</strong> Precision (accuracy of matches), Recall (catalog relevance), Diversity (genre variety), and Coverage (% of catalog reachable).</li>
      <li><strong>Academic Finding:</strong> Proves the <strong>1+1 Hybrid</strong> achieves superior precision while maintaining balanced diversity, validating the hybrid design.</li>
    </ul>
  </div>

  <!-- SUMMARY TABLE (Alternating Rows) -->
  <div style="margin-top: 14px;">
    <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">
      Architecture At A Glance
    </div>
    <table class="summary-table">
      <thead>
        <tr>
          <th>Page</th>
          <th>Recommender System</th>
          <th>Decision Support Tool</th>
          <th>Key Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>1. Home</strong></td>
          <td>Popularity + Personalized CBF</td>
          <td>Cold-Start Decision Banner</td>
          <td>Immediate start; personal feed as you rate</td>
        </tr>
        <tr>
          <td><strong>2. Anime Detail</strong></td>
          <td>Item-to-Item Similarity</td>
          <td>Rating Histogram & Badges</td>
          <td>Spot controversial vs loved titles</td>
        </tr>
        <tr>
          <td><strong>3. Browse & Find</strong></td>
          <td>Knowledge-Based Recommender</td>
          <td>Rule Checklist & Filters</td>
          <td>Match strict episode budget & mood</td>
        </tr>
        <tr>
          <td><strong>4. Smart Match</strong></td>
          <td>1+1 Hybrid (CBF + KBR)</td>
          <td>Dual Taste vs Fit Match Badges</td>
          <td>Picks what you love AND have time to watch</td>
        </tr>
        <tr>
          <td><strong>5. Decision Center</strong></td>
          <td>Comparative Candidate Ranking</td>
          <td>Side-by-Side Trade-off Matrix</td>
          <td>Resolve dilemmas between finalist shows</td>
        </tr>
        <tr>
          <td><strong>6. Benchmarks</strong></td>
          <td>Cross-Model Evaluation</td>
          <td>Precision, Recall, Diversity Table</td>
          <td>Objective proof for grading & defense</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Defense Summary Box -->
  <div class="defense-card">
    <div class="defense-title">Academic Defense Summary for Evaluators</div>
    <p>
      ANIVIBE demonstrates that a complete Decision Support and Recommendation System cannot rely on one paradigm alone.
      <strong>Popularity</strong> solves Cold-Start, <strong>Content-Based Filtering</strong> captures authentic taste,
      <strong>Knowledge-Based rules</strong> respect real-world time budgets, and the <strong>1+1 Hybrid</strong>
      unifies them into a transparent, optimal decision support platform.
    </p>
  </div>

  <div class="footer">
    <div>ANIVIBE Architectural Guide — Assumption University</div>
    <div>Page 4 of 4</div>
  </div>

</body>
</html>
"""

def generate_pdf():
    html_path = "/tmp/anivibe_guide_v2.html"
    pdf_path = os.path.abspath("docs/ANIVIBE_Decision_and_Recommender_Systems_Guide.pdf")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    chrome_cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        html_path
    ]

    print(f"Generating PDF via Headless Chrome: {pdf_path}")
    result = subprocess.run(chrome_cmd, capture_output=True, text=True)
    
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"SUCCESS: Generated {pdf_path} ({size_kb:.1f} KB)")
        return pdf_path
    else:
        print(f"Error generating PDF: {result.stderr}")
        return None

if __name__ == "__main__":
    generate_pdf()
