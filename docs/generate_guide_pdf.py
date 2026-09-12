#!/usr/bin/env python3
"""
Generates a clean, modern, 4-page PDF document explaining the Decision Support
and Recommendation Systems used across every page in the ANIVIBE web application.
Zero mathematical equations - simple, plain-English explanations.
"""

import os
import subprocess

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ANIVIBE — Decision Support & Recommender Systems Page-by-Page Guide</title>
<style>
  @page {
    size: A4;
    margin: 12mm 15mm 12mm 15mm;
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.5;
    font-size: 12.5px;
    margin: 0;
    padding: 0;
  }

  /* Header Section */
  .header {
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 12px;
    margin-bottom: 14px;
  }
  .header-tag {
    display: inline-block;
    font-size: 9.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 2px 7px;
    border-radius: 4px;
    background: #f1f5f9;
    color: #475569;
    margin-bottom: 5px;
  }
  h1 {
    font-size: 21px;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 4px 0;
    letter-spacing: -0.3px;
  }
  .subtitle {
    font-size: 12px;
    color: #64748b;
    margin: 0 0 8px 0;
  }
  .meta-bar {
    display: flex;
    gap: 16px;
    font-size: 10.5px;
    color: #475569;
  }
  .meta-bar strong {
    color: #0f172a;
  }

  /* Executive Overview Callout */
  .overview-callout {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 9px 12px;
    margin-bottom: 14px;
    font-size: 11.5px;
    color: #334155;
    line-height: 1.45;
  }
  .overview-callout strong {
    color: #0f172a;
  }

  /* Page Section Cards */
  .page-card {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 14px;
    background: #ffffff;
    page-break-inside: avoid;
  }
  .page-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 6px;
    margin-bottom: 8px;
  }
  .page-title {
    font-size: 14.5px;
    font-weight: 700;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .route-pill {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 10px;
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    color: #475569;
  }
  .badge {
    font-size: 9.5px;
    font-weight: 700;
    padding: 2.5px 7px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .badge-recommender { background: #ede9fe; color: #6d28d9; }
  .badge-decision { background: #e0f2fe; color: #0369a1; }
  .badge-hybrid { background: #fef3c7; color: #b45309; }

  .user-purpose {
    font-size: 11.5px;
    color: #475569;
    background: #f8fafc;
    border-left: 3px solid #cbd5e1;
    padding: 5px 9px;
    margin-bottom: 9px;
    border-radius: 0 4px 4px 0;
  }
  .user-purpose strong { color: #1e293b; }

  /* Subsection inside a page */
  .system-item {
    margin-bottom: 8px;
  }
  .system-item:last-child {
    margin-bottom: 0;
  }
  .system-name {
    font-weight: 700;
    font-size: 12.5px;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 2px;
  }
  .system-name .tag {
    font-size: 8.5px;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    text-transform: uppercase;
  }
  .tag-rec { background: #ede9fe; color: #6d28d9; }
  .tag-dec { background: #dbeafe; color: #1d4ed8; }
  .tag-both { background: #dcfce7; color: #15803d; }

  p {
    margin: 0 0 4px 0;
    color: #334155;
    font-size: 12px;
  }
  ul {
    margin: 3px 0 5px 0;
    padding-left: 16px;
  }
  li {
    margin-bottom: 2px;
    color: #334155;
    font-size: 11.5px;
  }
  li strong {
    color: #0f172a;
  }

  /* Summary Table */
  .summary-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
    font-size: 10.5px;
  }
  .summary-table th, .summary-table td {
    padding: 6px 8px;
    border: 1px solid #e2e8f0;
    text-align: left;
  }
  .summary-table th {
    background: #f8fafc;
    color: #1e293b;
    font-weight: 700;
  }
  .summary-table tr:nth-child(even) td {
    background: #fbfcfe;
  }

  .defense-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 6px;
    padding: 9px 12px;
    margin-top: 10px;
    font-size: 11.5px;
  }
  .defense-box strong { color: #166534; }

  .page-break {
    page-break-before: always;
  }

  .footer {
    border-top: 1px solid #e2e8f0;
    padding-top: 6px;
    margin-top: 12px;
    display: flex;
    justify-content: space-between;
    font-size: 9.5px;
    color: #94a3b8;
  }
</style>
</head>
<body>

  <!-- ==================== SHEET 1: HEADER & HOME PAGE ==================== -->
  <div class="header">
    <div class="header-tag">Academic Systems Reference</div>
    <h1>ANIVIBE — Decision Support & Recommender Systems Guide</h1>
    <div class="subtitle">Page-by-Page Guide to Systems, Decision Tools, and User Experience (Plain English, Zero Equations)</div>
    <div class="meta-bar">
      <div><strong>Course:</strong> CSX/ITX 4207 Decision Support & Recommender Systems</div>
      <div><strong>Institution:</strong> Assumption University</div>
      <div><strong>Live Demo:</strong> minkhanttin-anivibe.static.hf.space</div>
    </div>
  </div>

  <div class="overview-callout">
    <strong>Executive Architectural Summary:</strong> ANIVIBE combines two complementary technologies to eliminate the entertainment Paradox of Choice across 1,255 Crunchyroll anime titles:
    <strong>Recommender Systems</strong> automatically discover matching content based on community wisdom (Popularity), thematic similarity (Content-Based), or situational boundaries (Knowledge-Based).
    <strong>Decision Support Systems</strong> give users transparent evidence (rating distribution histograms, commitment badges, explainable checklists, and side-by-side trade-off matrices) so they can make confident viewing decisions.
  </div>

  <!-- PAGE 1: HOME PAGE -->
  <div class="page-card">
    <div class="page-title-row">
      <div class="page-title">
        <span>Page 1: Home Page</span>
        <span class="route-pill">/</span>
      </div>
      <div>
        <span class="badge badge-recommender">Popularity & Personalization</span>
      </div>
    </div>
    <div class="user-purpose">
      <strong>User Goal:</strong> The welcome portal. Solves first-time exploration for new users and delivers a tailored feed for returning users who have rated anime.
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>1. Popular Right Now</span>
        <span class="tag tag-rec">Popularity-Based Recommender</span>
      </div>
      <p>
        <strong>What it does:</strong> Recommends the most trusted, universally acclaimed anime across the community. It balances high review ratings with total review counts to ensure that anime with thousands of votes outrank titles with only a single 5-star review.
      </p>
      <p>
        <strong>Why it's used (Cold-Start Solution):</strong> When a new user opens the website for the very first time, the system has zero data on their taste. Rather than leaving the screen blank or guessing randomly, Popularity provides a safe, verified starting catalog immediately.
      </p>
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>2. Recommended For You</span>
        <span class="tag tag-rec">Content-Based Filtering</span>
      </div>
      <p>
        <strong>What it does:</strong> Listens to your 1-to-5 star ratings in the app. When you give 5 stars to fantasy or action shows, the system learns what you like, increases the importance of those genres, and recommends unwatched anime sharing those exact themes.
      </p>
      <p>
        <strong>Decision Support Benefit:</strong> Relieves choice overload. Instead of searching through 1,200 titles, the user gets an evolving, tailored feed matching their taste.
      </p>
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>3. Interactive Decision Onboarding Banner</span>
        <span class="tag tag-dec">Decision Support Prompt</span>
      </div>
      <p>
        <strong>What it does:</strong> If the visitor has zero ratings, a friendly card guides them to rate a few anime, explaining how rating unlocks personalized recommendations.
      </p>
    </div>
  </div>

  <div class="footer">
    <div>ANIVIBE Architectural Guide — Assumption University CSX/ITX 4207</div>
    <div>Page 1 of 4</div>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SHEET 2: DETAIL & BROWSE ==================== -->

  <!-- PAGE 2: ANIME DETAIL PAGE -->
  <div class="page-card">
    <div class="page-title-row">
      <div class="page-title">
        <span>Page 2: Anime Detail Page</span>
        <span class="route-pill">/anime/:id</span>
      </div>
      <div>
        <span class="badge badge-decision">Item Similarity & Evidence</span>
      </div>
    </div>
    <div class="user-purpose">
      <strong>User Goal:</strong> Investigating an individual anime to answer: <em>"Is this specific show worth my time and attention right now?"</em>
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>1. More Like This (Netflix-Style Horizontal Carousel)</span>
        <span class="tag tag-rec">Item-to-Item Content-Based Filtering</span>
      </div>
      <p>
        <strong>What it does:</strong> Looks strictly at the anime currently on screen and calculates which other anime in the catalog share the most genre attributes.
      </p>
      <p>
        <strong>Why it's used:</strong> Operates completely independently of user rating history. If you fall in love with a specific anime, you can immediately find direct sister titles with the same tone and pacing.
      </p>
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>2. Viewer Rating Distribution (1 to 5 Stars Breakdown)</span>
        <span class="tag tag-dec">Community Consensus Decision Support</span>
      </div>
      <p>
        <strong>What it does:</strong> Displays a golden bar chart directly inside the anime hero card showing what percentage of viewers gave 5 stars, 4 stars, down to 1 star.
      </p>
      <p>
        <strong>Why it's used (Decision Support):</strong> An average rating like "4.1" can be misleading. Seeing the distribution helps users spot whether an anime is universally beloved (almost all 5 stars) or polarizing/controversial (lots of 1 stars mixed with 5 stars).
      </p>
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>3. Commitment & Time Investment Badges</span>
        <span class="tag tag-dec">Constraint Evaluation</span>
      </div>
      <p>
        <strong>What it does:</strong> Flags each anime as <em>Short (&le; 13 episodes)</em>, <em>Medium (14–26 episodes)</em>, or <em>Long (&gt; 26 episodes)</em> so users can budget their evening or weekend.
      </p>
    </div>
  </div>

  <!-- PAGE 3: BROWSE & FIND PAGE -->
  <div class="page-card">
    <div class="page-title-row">
      <div class="page-title">
        <span>Page 3: Browse & Find Page</span>
        <span class="route-pill">/browse</span>
      </div>
      <div>
        <span class="badge badge-decision">Multi-Attribute Search & Rule-Based Advisory</span>
      </div>
    </div>
    <div class="user-purpose">
      <strong>User Goal:</strong> Provides two modes: self-guided catalog exploration (Browse) or situation-aware digital consultation (Find).
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>Mode A: Catalog Discovery</span>
        <span class="tag tag-dec">Exploratory Decision Support</span>
      </div>
      <p>
        <strong>What it does:</strong> Allows full-catalog search with interactive genre tags, instant title searching, and multi-criteria sorting (by community popularity, score, or title).
      </p>
      <p>
        <strong>Why it's used:</strong> Empowers users when they already have a specific keyword in mind or want to explore a single genre category (e.g. Sci-Fi).
      </p>
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>Mode B: Find What Fits</span>
        <span class="tag tag-rec">Knowledge-Based Recommender (KBR)</span>
      </div>
      <p>
        <strong>What it does:</strong> Acts as an expert advisor. You declare your real-world situational requirements:
      </p>
      <ul>
        <li><strong>Episode Budget:</strong> Set a strict ceiling (e.g., maximum 26 episodes for a weekend binge).</li>
        <li><strong>Quality Threshold:</strong> Set a minimum standard (e.g., ratings &ge; 4.0 only).</li>
        <li><strong>Required & Avoided Genres:</strong> Declare what must be present (e.g., Mystery) and what to exclude (e.g., No Horror).</li>
        <li><strong>Viewing Mood:</strong> Pick an emotional vibe (<em>Exciting, Chill, Dark, or Emotional</em>).</li>
      </ul>
      <p>
        <strong>Explainable Decision Verdicts:</strong> Every recommended title displays an itemized evaluation report (e.g. <em>"✓ Episode Budget: 12 eps satisfies &le; 26"</em> and <em>"✓ Quality: 4.4 rating meets &ge; 4.0"</em>) so users understand exactly why the anime was selected.
      </p>
    </div>
  </div>

  <div class="footer">
    <div>ANIVIBE Architectural Guide — Assumption University CSX/ITX 4207</div>
    <div>Page 2 of 4</div>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SHEET 3: SMART MATCH & DECISION CENTER ==================== -->

  <!-- PAGE 4: SMART MATCH PAGE -->
  <div class="page-card">
    <div class="page-title-row">
      <div class="page-title">
        <span>Page 4: Smart Match Page (Flagship)</span>
        <span class="route-pill">/smart-match</span>
      </div>
      <div>
        <span class="badge badge-hybrid">1+1 Hybrid Fusion Engine</span>
      </div>
    </div>
    <div class="user-purpose">
      <strong>User Goal:</strong> Solves the most common dilemma: <em>"I want something that matches my genuine taste, but also fits my available time and mood right now."</em>
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>1+1 Hybrid Fusion Recommender</span>
        <span class="tag tag-both">Hybrid Recommender + Decision Support</span>
      </div>
      <p>
        <strong>What it does:</strong> Concurrently computes two independent scores and merges them into a single recommendation:
      </p>
      <ul>
        <li><strong>50% User Taste Affinity (Content-Based):</strong> Evaluates how closely the anime's genres match your rating history.</li>
        <li><strong>50% Requirement Fit (Knowledge-Based):</strong> Evaluates how well the anime satisfies your episode budget, quality threshold, and mood.</li>
      </ul>
      <p>
        <strong>Why it's used:</strong> Content-based filtering alone might suggest a 500-episode classic when you only have one evening free. Knowledge-based filtering alone might find a short show in a genre you dislike. The 1+1 Hybrid guarantees you get a title you love <em>and</em> have time to watch.
      </p>
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>Transparent Dual-Score Match Badges</span>
        <span class="tag tag-dec">Decision Transparency</span>
      </div>
      <p>
        Each result card displays two distinct progress bars: <strong>Taste Match %</strong> (purple) and <strong>Requirement Fit %</strong> (cyan), giving users complete clarity into why the title was recommended.
      </p>
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>Cold-Start Safeguard</span>
        <span class="tag tag-dec">System Reliability</span>
      </div>
      <p>
        If a user has 0 ratings, the system prompts them to rate a few anime first or smoothly routes them to Knowledge-Based recommendations, ensuring zero crashes or empty states.
      </p>
    </div>
  </div>

  <!-- PAGE 5: DECISION CENTER -->
  <div class="page-card">
    <div class="page-title-row">
      <div class="page-title">
        <span>Page 5: Decision Center</span>
        <span class="route-pill">/decision-center</span>
      </div>
      <div>
        <span class="badge badge-decision">Multi-Criteria Decision Analysis (MCDA)</span>
      </div>
    </div>
    <div class="user-purpose">
      <strong>User Goal:</strong> Resolves final indecision when a user is torn between 2 or 3 finalist anime.
    </div>

    <div class="system-item">
      <div class="system-name">
        <span>Side-by-Side Comparison Matrix</span>
        <span class="tag tag-dec">Multi-Criteria Decision Making</span>
      </div>
      <p>
        <strong>What it does:</strong> Displays up to 3 selected anime side-by-side across key comparison criteria:
      </p>
      <ul>
        <li><strong>Time Investment:</strong> Total episodes and estimated hours required to complete the show.</li>
        <li><strong>Quality vs. Popularity:</strong> Direct comparison of rating score versus total community review volume.</li>
        <li><strong>Rating Distributions:</strong> Compare the 5-star vs 1-star ratios of each candidate side by side.</li>
        <li><strong>Thematic Comparison:</strong> Shows shared genres and unique thematic elements between the choices.</li>
      </ul>
      <p>
        <strong>Decision Support Benefit:</strong> Eliminates browser tab clutter and mental fatigue by organizing all trade-offs onto a single, structured decision dashboard.
      </p>
    </div>
  </div>

  <div class="footer">
    <div>ANIVIBE Architectural Guide — Assumption University CSX/ITX 4207</div>
    <div>Page 3 of 4</div>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SHEET 4: BENCHMARKS, SUMMARY & DEFENSE ==================== -->

  <!-- PAGE 6: ACADEMIC BENCHMARKS PAGE -->
  <div class="page-card">
    <div class="page-title-row">
      <div class="page-title">
        <span>Page 6: Academic Benchmarks Page</span>
        <span class="route-pill">/benchmarks</span>
      </div>
      <div>
        <span class="badge badge-decision">Empirical Model Evaluation</span>
      </div>
    </div>
    <div class="user-purpose">
      <strong>User Goal:</strong> Provides instructors and evaluators with scientific proof of how each recommender paradigm performs.
    </div>

    <div class="system-item">
      <p>
        <strong>What it does:</strong> Displays benchmark metrics comparing all four approaches:
      </p>
      <ul>
        <li><strong>Precision:</strong> How accurately the recommendations match user test profiles.</li>
        <li><strong>Recall:</strong> The percentage of relevant titles captured in the top recommendations.</li>
        <li><strong>Diversity:</strong> Whether the model offers diverse variety or repeats the same narrow genres.</li>
        <li><strong>Coverage:</strong> The percentage of the 1,255-title catalog the model can reach.</li>
      </ul>
      <p>
        <strong>Key Finding:</strong> Demonstrates that the <strong>1+1 Hybrid</strong> achieves the highest precision while maintaining healthy diversity, proving why hybrid architectures are superior.
      </p>
    </div>
  </div>

  <!-- SUMMARY TABLE -->
  <div class="page-card">
    <div class="page-title-row">
      <div class="page-title">
        <span>Summary: Architecture At A Glance</span>
      </div>
    </div>
    <table class="summary-table">
      <thead>
        <tr>
          <th>Page Name</th>
          <th>Recommender System</th>
          <th>Decision Support Feature</th>
          <th>User Benefit</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>1. Home</strong></td>
          <td>Popularity Baseline + Personalized CBF</td>
          <td>Cold-Start Onboarding Prompt</td>
          <td>Safe start for new users; tailored feed as you rate</td>
        </tr>
        <tr>
          <td><strong>2. Anime Detail</strong></td>
          <td>Item-to-Item Similarity</td>
          <td>5-Star Rating Histogram</td>
          <td>Spot controversial vs loved titles; find sister anime</td>
        </tr>
        <tr>
          <td><strong>3. Browse & Find</strong></td>
          <td>Knowledge-Based Recommender (KBR)</td>
          <td>Rule Checklist & Multi-Attribute Search</td>
          <td>Filter by exact episode limits, minimum score, and mood</td>
        </tr>
        <tr>
          <td><strong>4. Smart Match</strong></td>
          <td>1+1 Hybrid (50% CBF + 50% KBR)</td>
          <td>Dual Taste vs Fit Percentage Badges</td>
          <td>Recommends what you love AND have time to watch</td>
        </tr>
        <tr>
          <td><strong>5. Decision Center</strong></td>
          <td>Comparative Candidate Ranking</td>
          <td>Side-by-Side Multi-Criteria Matrix</td>
          <td>Resolve indecision between 2 or 3 finalist titles</td>
        </tr>
        <tr>
          <td><strong>6. Benchmarks</strong></td>
          <td>Cross-Model Empirical Comparison</td>
          <td>Precision, Recall, Diversity Metrics</td>
          <td>Scientific validation for academic grading and defense</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- DEFENSE BOX -->
  <div class="defense-box">
    <strong>Project Defense Summary for Evaluators:</strong>
    ANIVIBE demonstrates that a modern recommendation platform cannot rely on a single technique. Popularity solves Cold-Start, Content-Based Filtering models personal taste, Knowledge-Based rules satisfy real-world time budgets, and the 1+1 Hybrid fuses them into an optimal decision support system.
  </div>

  <div class="footer">
    <div>ANIVIBE Architectural Guide — Assumption University CSX/ITX 4207</div>
    <div>Page 4 of 4</div>
  </div>

</body>
</html>
"""

def generate_pdf():
    html_path = "/tmp/anivibe_guide.html"
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
