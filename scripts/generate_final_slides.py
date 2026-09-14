#!/usr/bin/env python3
"""
ANIVIBE Professional Presentation Generator (.pptx) - Light / White Theme
Assumption University — CSX/ITX 4207 Decision Support and Recommendation System

Generates a modern, clean, widescreen (16:9) presentation in a crisp, high-readability
white/light theme covering:
1. Title Page
2. Introduction (2 slides: Context & Decision Support Goals)
3. Explain About Dataset (2 slides: Overview & Feature Preprocessing)
4. List of Recommender Systems (1 slide: The 4 Core Paradigms)
5. Explain Popularity Base (3 slides: Theory, Bayesian Calculation, Top 10 Anime Table)
6. Content Base (4 slides: Concept, Vector Space Model, Naruto Step-by-Step, Top Similar Anime Table)
7. Knowledge Base (3 slides: Concept, Constraints & Rules, Continuous Fit Scoring)
8. Hybrid (4 slides: Concept, Multi-Anime Taste Profile, 70/40 Formula, Cold-Start Handling)
9. Conclusion (1 slide: Key Takeaways & Impact)
10. Thank You (1 slide: Q&A and Project Links)

Design Principles:
- Light / White background (soft pearl white #f8fafc with crisp #ffffff cards).
- High contrast: deep charcoal text (#0f172a, #334155) with vibrant, professional accents.
- Minimum font size >= 14 pt (Body: 16-18 pt, Headings: 22-26 pt, Titles: 30-44 pt).
- Uncluttered, simple slides with short bullet points, equations, and exact dataset tables.
"""

import os
import json
import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# COLOR PALETTE (Clean White Theme with High-Contrast Vibrant Accents)
# ==============================================================================
BG_LIGHT      = RGBColor(248, 250, 252)  # #f8fafc - Soft off-white / pearl slate
CARD_BG       = RGBColor(255, 255, 255)  # #ffffff - Pure crisp white card
CARD_BORDER   = RGBColor(226, 232, 240)  # #e2e8f0 - Subtle clean slate border
HEADER_BG     = RGBColor(241, 245, 249)  # #f1f5f9 - Light slate table header

# High-contrast, bright, legible accents on white:
ACCENT_INDIGO = RGBColor(79, 70, 229)    # #4f46e5 - Deep Vibrant Indigo
ACCENT_CYAN   = RGBColor(8, 145, 178)    # #0891b2 - Deep Vibrant Cyan
ACCENT_GREEN  = RGBColor(5, 150, 105)    # #059669 - Emerald Green
ACCENT_AMBER  = RGBColor(217, 119, 6)    # #d97706 - Warm Amber / Gold
ACCENT_ROSE   = RGBColor(225, 29, 72)    # #e11d48 - Deep Vivid Rose
ACCENT_PURPLE = RGBColor(147, 51, 234)   # #9333ea - Rich Purple

# Typography colors:
TEXT_DARK     = RGBColor(15, 23, 42)     # #0f172a - Slate 900 (High contrast titles & headings)
TEXT_BODY     = RGBColor(51, 65, 85)     # #334155 - Slate 700 (Crisp, easily readable body text)
TEXT_MUTED    = RGBColor(100, 116, 139)  # #64748b - Slate 500 (Subtitles & secondary notes)

FONT_HEADING  = "Helvetica"
FONT_BODY     = "Arial"

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def set_slide_background(slide, prs):
    """Fills the slide canvas with a crisp, soft off-white background."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_LIGHT
    bg.line.fill.background()
    # Send to back
    slide.shapes._spTree.remove(bg._element)
    slide.shapes._spTree.insert(2, bg._element)
    return bg

def add_header(slide, tag_text, title_text, subtitle_text=None, tag_color=ACCENT_INDIGO):
    """Standardized clean slide header with category tag, title, and subtitle."""
    # 1. Category Tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.name = FONT_BODY
    p_tag.font.size = Pt(14)
    p_tag.font.bold = True
    p_tag.font.color.rgb = tag_color

    # 2. Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(30)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_DARK

    # 3. Subtitle
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.38), Inches(11.7), Inches(0.45))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(16)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Adds a rounded container card with clean borders and white fill."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.fill.background()
    return card

def add_bullet_point(tf, prefix, text, size=16, prefix_color=ACCENT_INDIGO, body_color=TEXT_BODY, space_after=12):
    """Adds a formatted bullet point with bold colored prefix and dark body text."""
    p = tf.add_paragraph()
    p.space_after = Pt(space_after)

    run_bullet = p.add_run()
    run_bullet.text = "• "
    run_bullet.font.size = Pt(size)
    run_bullet.font.bold = True
    run_bullet.font.color.rgb = prefix_color

    if prefix:
        run_pre = p.add_run()
        run_pre.text = prefix + ": "
        run_pre.font.size = Pt(size)
        run_pre.font.bold = True
        run_pre.font.color.rgb = prefix_color

    run_body = p.add_run()
    run_body.text = text
    run_body.font.size = Pt(size)
    run_body.font.bold = False
    run_body.font.color.rgb = body_color

# ==============================================================================
# MAIN GENERATOR
# ==============================================================================
def generate_all_slides():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Load catalog data for exact numbers
    catalog_path = os.path.join(os.path.dirname(__file__), "../data/processed/anime_catalog.json")
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # Precompute Bayesian scores
    rates = [a["rate"] for a in catalog if a.get("rate")]
    global_mean = sum(rates) / len(rates)
    m = 100
    for a in catalog:
        v = a.get("votes", 0)
        r = a.get("rate", 0)
        a["bayes_score"] = (v / (v + m)) * r + (m / (v + m)) * global_mean

    top_popular = sorted(catalog, key=lambda x: x["bayes_score"], reverse=True)[:10]

    # Precompute Naruto CBF
    naruto = next(a for a in catalog if a["title"] == "Naruto Shippuuden")
    def dot(v1, v2): return sum(x * y for x, y in zip(v1, v2))
    def norm(v): return math.sqrt(sum(x * x for x in v))
    def cos_sim(v1, v2):
        n1, n2 = norm(v1), norm(v2)
        return dot(v1, v2) / (n1 * n2) if n1 and n2 else 0.0

    naruto_sims = []
    for a in catalog:
        if a["anime_id"] == naruto["anime_id"]: continue
        sim = cos_sim(naruto["genre_vector"], a["genre_vector"])
        if sim > 0:
            naruto_sims.append((a["title"], a["genres"], sim, a["rate"], a["episodes"]))
    naruto_sims.sort(key=lambda x: x[2], reverse=True)

    # Layout constants
    top_y = Inches(1.95)
    card_h = Inches(5.0)
    full_w = Inches(11.733)
    half_w = Inches(5.666)
    right_x = Inches(6.866)

    # --------------------------------------------------------------------------
    # 1. TITLE PAGE
    # --------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, prs)

    # Title Card (Pure white with Indigo border)
    add_card(s1, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1), bg_color=CARD_BG, border_color=ACCENT_INDIGO)

    tb = s1.shapes.add_textbox(Inches(1.5), Inches(1.6), Inches(10.333), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ANIVIBE"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "Decision Support & Recommender System for Anime"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_after = Pt(24)

    p = tf.add_paragraph()
    p.text = "Assumption University of Thailand • Vincent Mary School of Science and Technology"
    p.font.size = Pt(18)
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "Course: CSX/ITX 4207 Decision Support and Recommender Systems"
    p.font.size = Pt(16)
    p.font.color.rgb = TEXT_BODY
    p.space_after = Pt(20)

    p = tf.add_paragraph()
    p.text = "Core Architectures: Bayesian Popularity • 29-Genre Content-Based Filtering • Knowledge-Based Constraints • 70/40 Hybrid Fusion"
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED

    # --------------------------------------------------------------------------
    # 2. INTRODUCTION (Slide 1/2: The Problem)
    # --------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, prs)
    add_header(s2, "2. Introduction", "The Challenge: Anime Information Overload", "Why standard single-algorithm recommendation fails real-world streaming viewers.")

    # Left: The Streaming Dilemma
    add_card(s2, Inches(0.8), top_y, half_w, card_h, border_color=ACCENT_ROSE)
    tb = s2.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Overload Problem"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ROSE
    p.space_after = Pt(16)

    add_bullet_point(tf, "Massive Catalogues", "Over 1,200+ anime titles available across hundreds of specialized genres and multi-season formats.", 16, prefix_color=ACCENT_ROSE)
    add_bullet_point(tf, "Choice Paralysis", "Viewers spend 15–20 minutes browsing catalogs without deciding what to watch.", 16, prefix_color=ACCENT_ROSE)
    add_bullet_point(tf, "Severe Length Variance", "Titles range from 12-episode quick watches to 500+ episode long commitments (e.g. Naruto, One Piece).", 16, prefix_color=ACCENT_ROSE)
    add_bullet_point(tf, "Cold-Start Friction", "New visitors have zero watch history, causing pure collaborative systems to completely crash or fail.", 16, prefix_color=ACCENT_ROSE)

    # Right: Why Single Algorithms Fail
    add_card(s2, right_x, top_y, half_w, card_h, border_color=ACCENT_AMBER)
    tb = s2.shapes.add_textbox(Inches(7.166), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Flaws of Single Models"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(16)

    add_bullet_point(tf, "Popularity Alone", "Biased toward blockbusters; ignores individual user tastes and situation limits entirely.", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "Content-Based Alone", "Prone to severe over-specialization and cannot filter by episode commitment or quality.", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "Knowledge-Based Alone", "Finds valid shows matching rules, but lacks personal taste adaptation across user history.", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "The Academic Solution", "A multi-paradigm decision support architecture combining consensus, taste, and situational constraints.", 16, prefix_color=ACCENT_AMBER)

    # --------------------------------------------------------------------------
    # 2. INTRODUCTION (Slide 2/2: ANIVIBE Solution)
    # --------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, prs)
    add_header(s3, "2. Introduction", "The ANIVIBE Solution: Decision Support System", "Providing interactive guidance, real-world constraint solving, and multi-paradigm recommendations.")

    # 3 Column Cards
    col3_w = Inches(3.644)
    c1_x = Inches(0.8)
    c2_x = Inches(4.844)
    c3_x = Inches(8.888)

    # Column 1: Multi-Paradigm Engine
    add_card(s3, c1_x, top_y, col3_w, card_h, border_color=ACCENT_INDIGO)
    tb = s3.shapes.add_textbox(c1_x + Inches(0.25), top_y + Inches(0.4), col3_w - Inches(0.5), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. Multi-Paradigm"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(14)
    add_bullet_point(tf, "Strict Academic Models", "Implements Popularity, CBF, KBR, and 70/40 Hybrid independently.", 15, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "No Black-Box", "Transparent formulas: Bayesian Smoothing, CountVectorizer, and Cosine Similarity.", 15, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Zero Drift", "Mathematical evaluation guarantees stable results.", 15, prefix_color=ACCENT_INDIGO)

    # Column 2: Situation Fit
    add_card(s3, c2_x, top_y, col3_w, card_h, border_color=ACCENT_PURPLE)
    tb = s3.shapes.add_textbox(c2_x + Inches(0.25), top_y + Inches(0.4), col3_w - Inches(0.5), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "2. Situational Fit"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(14)
    add_bullet_point(tf, "Time Commitment", "Users select episode limits (e.g. ≤ 13, ≤ 26, ≤ 50 eps) to fit available time.", 15, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "Quality Thresholds", "Filters anime strictly above user-defined minimum rating thresholds.", 15, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "Genre Directives", "Guarantees must-include genre presence.", 15, prefix_color=ACCENT_PURPLE)

    # Column 3: Zero-Dependency Local Delivery
    add_card(s3, c3_x, top_y, col3_w, card_h, border_color=ACCENT_GREEN)
    tb = s3.shapes.add_textbox(c3_x + Inches(0.25), top_y + Inches(0.4), col3_w - Inches(0.5), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3. Zero-Latency"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(14)
    add_bullet_point(tf, "100% Client-Side Engine", "Runs full vector math in browser client engine without external cloud delays.", 15, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Interactive Session Ratings", "Every rating immediately recalculates the multi-anime taste vector live.", 15, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Dual Deployment", "Supports local Node/Python and 100% static hosting.", 15, prefix_color=ACCENT_GREEN)

    # --------------------------------------------------------------------------
    # 3. EXPLAIN ABOUT DATASET (Slide 1/2: Dataset Overview)
    # --------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, prs)
    add_header(s4, "3. Explain About Dataset", "Dataset Overview & Core Attributes", "Real-world Crunchyroll streaming anime dataset with rich viewer feedback.")

    add_card(s4, Inches(0.8), top_y, half_w, card_h, border_color=ACCENT_INDIGO)
    tb = s4.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Dataset Schema & Scale"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(16)
    add_bullet_point(tf, "Total Catalog Size", f"{len(catalog):,} verified anime titles sourced from Crunchyroll.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Rating Scale", "Continuous scale from 1.0 to 5.0 stars with individual 1–5 star vote breakdowns.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "High Vote Volume", "Includes mega-titles with up to 48,000+ viewer ratings per series.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Episode Lengths", "Varies from 1-episode OVAs/movies up to 1,100+ episodes (One Piece).", 16, prefix_color=ACCENT_INDIGO)

    add_card(s4, right_x, top_y, half_w, card_h, border_color=ACCENT_CYAN)
    tb = s4.shapes.add_textbox(Inches(7.166), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Core Data Fields Per Anime"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(16)
    add_bullet_point(tf, "anime_id", "Unique integer identifier for indexing and vector mapping.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "title", "Canonical series title (e.g. Naruto Shippuuden, Skip Beat!).", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "genres", "Normalized list of category strings (e.g. Action, Shonen, Fantasy).", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "rate & votes", "Arithmetic average rating and total community rating volume.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "rate_1 .. rate_5", "Exact distribution of 1-star, 2-star, 3-star, 4-star, and 5-star votes.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "anime_url & anime_img", "Direct streaming destination link and high-resolution poster.", 16, prefix_color=ACCENT_CYAN)

    # --------------------------------------------------------------------------
    # 3. EXPLAIN ABOUT DATASET (Slide 2/2: Feature Vectorization)
    # --------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, prs)
    add_header(s5, "3. Explain About Dataset", "Data Cleaning & 29-Genre Vectorization", "How raw text genres are transformed into standardized mathematical feature vectors.")

    add_card(s5, Inches(0.8), top_y, full_w, card_h, border_color=ACCENT_PURPLE)
    tb = s5.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), full_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "CountVectorizer Genre Representation"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(14)

    add_bullet_point(tf, "1. Normalization & Tokenization", "Raw genre strings were parsed, trimmed, lowercase-standardized, and deduplicated.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "2. CountVectorizer (sklearn)", "Extracted exactly 29 unique canonical anime genres across the entire database.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "3. Binary Vector Mapping", "Each anime is represented as a 29-dimensional vector v ∈ {0, 1}^29 where index i = 1 if genre is present, 0 otherwise.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "4. Strict Rejection of Prohibited Methods", "NO TF-IDF (preserves rare genres equally), NO synthetic users, and NO centered taste weighting (Rating - 3.0).", 16, prefix_color=ACCENT_PURPLE)

    p = tf.add_paragraph()
    p.text = "The 29 Canonical Genre Dimensions:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    genres_display = "Action, Adventure, Comedy, Drama, Fantasy, Horror, Isekai, Mecha, Mystery, Romance, Sci-Fi, Shonen, Slice of Life, Sports, Supernatural, Thriller, Historical, Martial Arts, Music, Psychological, Post-Apocalyptic, Harem, Idol, Magical Girl, Seinen, Shojo, Tournament, Food, Super Power"
    p.text = genres_display
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED

    # --------------------------------------------------------------------------
    # 4. LIST OF RECOMMENDER SYSTEMS
    # --------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, prs)
    add_header(s6, "4. List of Recommender Systems", "The 4 Core Recommendation Paradigms", "Strict academic separation between consensus, content similarity, rule satisfaction, and hybrid fusion.")

    col2_w = Inches(5.666)
    row_h = Inches(2.35)
    y1 = Inches(2.0)
    y2 = Inches(4.65)

    paradigms = [
        (Inches(0.8), y1, "1. Popularity-Based", "Consensus Ranking (Bayesian)", "Ranks globally loved titles using Bayesian rating smoothing to prevent low-vote score inflation. Serves as the zero-history cold-start baseline.", ACCENT_AMBER),
        (right_x, y1, "2. Content-Based (CBF)", "29-Genre Cosine Similarity", "Evaluates genre overlap using CountVectorizer and Cosine Similarity. Powers 'More Like This' and builds user taste vectors from session ratings.", ACCENT_PURPLE),
        (Inches(0.8), y2, "3. Knowledge-Based (KBR)", "Constraint Satisfaction", "Evaluates explicit situational requirements (episode commitment ≤ N, minimum rating ≥ R, and must-include genres) with zero user history required.", ACCENT_CYAN),
        (right_x, y2, "4. 70/40 Hybrid Recommendation", "Situational Fit + Taste Profile", "Fuses 70% KBR situation constraints with 40% CBR composite taste profile vector U = ∑ v_i across ALL user-rated anime in the session.", ACCENT_GREEN)
    ]

    for x, y, title, subtitle, desc, col in paradigms:
        add_card(s6, x, y, col2_w, row_h, border_color=col)
        tb = s6.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), col2_w - Inches(0.5), row_h - Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = subtitle
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(6)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_BODY

    # --------------------------------------------------------------------------
    # 5. EXPLAIN POPULARITY BASE (Slide 1/3: Theory & Need)
    # --------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, prs)
    add_header(s7, "5. Popularity-Based Recommendation", "Concept & The Flaw of Raw Averages", "Why simple arithmetic mean fails, and how Bayesian smoothing fixes vote imbalance.")

    add_card(s7, Inches(0.8), top_y, half_w, card_h, border_color=ACCENT_AMBER)
    tb = s7.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Problem With Raw Averages"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(16)

    add_bullet_point(tf, "Unreliable Outliers", "An obscure anime with only 2 ratings of 5.0 stars has a raw mean of 5.00 ★.", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "Unfair Blockbuster Penalty", "A masterpiece with 45,000 ratings and an average of 4.85 ★ would be ranked below the 2-vote show.", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "Zero Statistical Confidence", "Raw average fails to account for sample size uncertainty.", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "Ruined User Experience", "Showing obscure or niche titles on the home page damages initial user trust.", 16, prefix_color=ACCENT_AMBER)

    add_card(s7, right_x, top_y, half_w, card_h, border_color=ACCENT_CYAN)
    tb = s7.shapes.add_textbox(Inches(7.166), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Bayesian Solution"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(16)

    add_bullet_point(tf, "Bayesian Prior (Shrinkage)", f"Pulls all anime toward the catalog global mean (C = {global_mean:.3f} ★) as a baseline prior.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Confidence Weighting (m)", "Sets a minimum vote threshold (m = 100 votes) required to establish statistical credibility.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Automatic Equilibrium", "High-vote titles rely almost entirely on their true rating; low-vote titles stay near the global mean.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Home Page Foundation", "Powers 'Popular Right Now' as the reliable cold-start consensus for first-time visitors.", 16, prefix_color=ACCENT_CYAN)

    # --------------------------------------------------------------------------
    # 5. EXPLAIN POPULARITY BASE (Slide 2/3: Formula & Calculations)
    # --------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, prs)
    add_header(s8, "5. Popularity-Based Recommendation", "Mathematical Formulation & Step-by-Step", "The exact Bayesian weighted rating formula utilized in ANIVIBE.")

    add_card(s8, Inches(0.8), top_y, full_w, card_h, border_color=ACCENT_AMBER)
    tb = s8.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), full_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Bayesian Weighted Rating Formula"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(14)

    # Equation box
    p = tf.add_paragraph()
    p.text = "WR = [ v / (v + m) ] × R  +  [ m / (v + m) ] × C"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(16)

    add_bullet_point(tf, "v (Vote Count)", "The number of community ratings for the individual anime series.", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "m (Confidence Threshold)", "Set to 100 ratings in ANIVIBE. Represents the number of votes required for confidence.", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "R (Individual Rating)", "The raw arithmetic mean rating of the anime (1.0 to 5.0 stars).", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "C (Global Prior Mean)", f"Calculated across all 1,255 anime in the dataset: C = {global_mean:.3f} stars.", 16, prefix_color=ACCENT_AMBER)

    p = tf.add_paragraph()
    p.text = "Mathematical Proof of Behavior:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_after = Pt(6)

    add_bullet_point(tf, "When v is huge (e.g. v = 15,011)", "v / (v + 100) = 0.993 → WR ≈ R (true rating dominates).", 15, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "When v is tiny (e.g. v = 2, R = 5.0)", "2 / 102 = 0.02 → WR = 0.02(5.0) + 0.98(4.147) = 4.164 ★ (safely suppressed).", 15, prefix_color=ACCENT_GREEN)

    # --------------------------------------------------------------------------
    # 5. EXPLAIN POPULARITY BASE (Slide 3/3: Top 10 Table)
    # --------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, prs)
    add_header(s9, "5. Popularity-Based Recommendation", "Top 10 Popular Anime (Actual Dataset)", "Calculated using Bayesian rating smoothing across all 1,255 titles.")

    # Table Shape
    table_shape = s9.shapes.add_table(11, 5, Inches(0.8), top_y, full_w, card_h)
    tbl = table_shape.table
    tbl.columns[0].width = Inches(0.8)   # Rank
    tbl.columns[1].width = Inches(5.333) # Title
    tbl.columns[2].width = Inches(1.8)   # Raw Rating
    tbl.columns[3].width = Inches(1.9)   # Total Votes
    tbl.columns[4].width = Inches(1.9)   # Bayesian Score

    headers = ["Rank", "Anime Title", "Raw Rating (R)", "Total Votes (v)", "Bayesian Score (WR)"]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = HEADER_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_HEADING
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = ACCENT_INDIGO
        p.alignment = PP_ALIGN.CENTER if col_idx != 1 else PP_ALIGN.LEFT

    for row_idx, item in enumerate(top_popular, 1):
        row_data = [
            f"#{row_idx}",
            item["title"],
            f"{item['rate']:.2f} ★",
            f"{item['votes']:,}",
            f"{item['bayes_score']:.3f}"
        ]
        is_even = (row_idx % 2 == 0)
        for col_idx, text in enumerate(row_data):
            cell = tbl.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if is_even else RGBColor(248, 250, 252)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = FONT_BODY
            p.font.size = Pt(14)
            p.font.color.rgb = TEXT_DARK if col_idx < 4 else ACCENT_GREEN
            p.font.bold = (col_idx == 4 or col_idx == 0)
            p.alignment = PP_ALIGN.CENTER if col_idx != 1 else PP_ALIGN.LEFT

    # --------------------------------------------------------------------------
    # 6. CONTENT BASE (Slide 1/4: Concept & Core Method)
    # --------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, prs)
    add_header(s10, "6. Content-Based Filtering (CBF)", "Concept & Core Method", "Item-to-Item Content-Based Filtering powering 'More Like This' on the anime viewing page.")

    add_card(s10, Inches(0.8), top_y, half_w, card_h, border_color=ACCENT_PURPLE)
    tb = s10.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Core Principles"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(16)

    add_bullet_point(tf, "Pure Content Matching", "Recommends anime based purely on shared genre attributes between the selected viewing anime and catalog titles.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "Viewing Page Integration", "When a user views an anime (e.g. Naruto Shippuuden), the system generates the 'More Like This' row.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "Reference Exclusion", "The viewing anime itself is strictly excluded from results so only new discovery candidates appear.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "Zero Collaborative Drift", "Requires no user clusters, no synthetic ratings, and no ratings-minus-3.0 math.", 16, prefix_color=ACCENT_PURPLE)

    add_card(s10, right_x, top_y, half_w, card_h, border_color=ACCENT_CYAN)
    tb = s10.shapes.add_textbox(Inches(7.166), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Mathematical Pipeline"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(16)

    add_bullet_point(tf, "Step 1: Clean Genres", "Normalize raw genres into canonical tokens across 29 unique categories.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Step 2: CountVectorizer", "Convert each anime's genres into a 29-dimensional binary vector v_i.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Step 3: Cosine Similarity", "Compute cosine of angle between viewing anime vector and candidate anime vectors.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Step 4: Descending Sort", "Sort candidates descending by Cosine Similarity and display top similar titles.", 16, prefix_color=ACCENT_CYAN)

    # --------------------------------------------------------------------------
    # 6. CONTENT BASE (Slide 2/4: Vector Space Model & Formula)
    # --------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, prs)
    add_header(s11, "6. Content-Based Filtering (CBF)", "Vector Space Model & Cosine Similarity Formula", "Measuring angular proximity in 29-dimensional genre space.")

    add_card(s11, Inches(0.8), top_y, full_w, card_h, border_color=ACCENT_PURPLE)
    tb = s11.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), full_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Cosine Similarity Mathematical Definition"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(14)

    # Formula
    p = tf.add_paragraph()
    p.text = "CosineSimilarity(A, B) = ( A • B ) / ( ||A|| × ||B|| ) = [ ∑ A_i B_i ] / [ √(∑ A_i²) × √(∑ B_i²) ]"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(16)

    add_bullet_point(tf, "A • B (Dot Product)", "Multiplies matching genre elements. Each shared genre adds 1 × 1 = 1 to the dot product numerator.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "||A|| (Euclidean Norm)", "Length of vector A: √(number of genres in anime A). For Naruto with 5 genres: ||A|| = √5 ≈ 2.236.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "||B|| (Euclidean Norm)", "Length of candidate vector B: √(number of genres in candidate anime B).", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "Length Invariance", "Normalizing by vector norms prevents anime with many genres from artificially dominating recommendations.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "Bounded Range", "Score always ranges strictly between 0.0 (zero genre overlap) and 1.0 (identical genre set).", 16, prefix_color=ACCENT_PURPLE)

    # --------------------------------------------------------------------------
    # 6. CONTENT BASE (Slide 3/4: Naruto Shippuuden Calculation Example)
    # --------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, prs)
    add_header(s12, "6. Content-Based Filtering (CBF)", "Step-by-Step Calculation: Naruto Shippuuden", "Demonstrating exact cosine similarity calculations between Naruto and candidate titles.")

    add_card(s12, Inches(0.8), top_y, half_w, card_h, border_color=ACCENT_INDIGO)
    tb = s12.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Reference Anime: Naruto"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(14)

    add_bullet_point(tf, "Title", "Naruto Shippuuden", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Genres (5)", "Action, Adventure, Fantasy, Martial Arts, Shonen", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Feature Vector A", "Has 1s at positions for Action, Adventure, Fantasy, Martial Arts, Shonen; 0s elsewhere.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Norm ||A||", "√(1² + 1² + 1² + 1² + 1²) = √5 ≈ 2.236", 16, prefix_color=ACCENT_INDIGO)

    add_card(s12, right_x, top_y, half_w, card_h, border_color=ACCENT_GREEN)
    tb = s12.shapes.add_textbox(Inches(7.166), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Candidate: Hunter x Hunter"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(14)

    add_bullet_point(tf, "Candidate Genres (4)", "Action, Adventure, Fantasy, Shonen", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Norm ||B||", "√(1² + 1² + 1² + 1²) = √4 = 2.000", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Dot Product (A • B)", "Action(1) + Adventure(1) + Fantasy(1) + Shonen(1) = 4 shared genres", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Cosine Similarity", "4.0 / (2.236 × 2.000) = 4.0 / 4.472 = 0.894", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Percentage Match", "min(99%, round(0.894 × 100)) = 89% Match", 16, prefix_color=ACCENT_GREEN)

    # --------------------------------------------------------------------------
    # 6. CONTENT BASE (Slide 4/4: Top Similar to Naruto Table)
    # --------------------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, prs)
    add_header(s13, "6. Content-Based Filtering (CBF)", "Actual Results: 'More Like This' for Naruto", "Top similar anime generated from our actual catalog using 29-genre Cosine Similarity.")

    # Table Shape
    table_shape = s13.shapes.add_table(9, 6, Inches(0.8), top_y, full_w, card_h)
    tbl = table_shape.table
    tbl.columns[0].width = Inches(0.8)   # Rank
    tbl.columns[1].width = Inches(3.6)   # Title
    tbl.columns[2].width = Inches(4.333) # Genres
    tbl.columns[3].width = Inches(1.1)   # Rate
    tbl.columns[4].width = Inches(0.9)   # Eps
    tbl.columns[5].width = Inches(1.0)   # Sim

    headers = ["Rank", "Similar Anime Title", "Genre Overlap", "Rating", "Eps", "Cosine Sim"]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = HEADER_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_HEADING
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = ACCENT_PURPLE
        p.alignment = PP_ALIGN.CENTER if col_idx not in [1, 2] else PP_ALIGN.LEFT

    for row_idx, (title, genres, sim, rate, eps) in enumerate(naruto_sims[:8], 1):
        g_str = ", ".join(genres[:4])
        row_data = [
            f"#{row_idx}",
            title,
            g_str,
            f"{rate:.2f} ★",
            f"{eps} ep",
            f"{sim:.3f}"
        ]
        is_even = (row_idx % 2 == 0)
        for col_idx, text in enumerate(row_data):
            cell = tbl.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if is_even else RGBColor(248, 250, 252)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = FONT_BODY
            p.font.size = Pt(14)
            p.font.color.rgb = TEXT_DARK if col_idx != 5 else ACCENT_GREEN
            p.font.bold = (col_idx == 5 or col_idx == 0)
            p.alignment = PP_ALIGN.CENTER if col_idx not in [1, 2] else PP_ALIGN.LEFT

    # --------------------------------------------------------------------------
    # 7. KNOWLEDGE BASE (Slide 1/3: Concept & Motivation)
    # --------------------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, prs)
    add_header(s14, "7. Knowledge-Based Recommendation (KBR)", "Concept & Situational Problem Solving", "Why users need explicit constraint matching instead of relying solely on past ratings.")

    add_card(s14, Inches(0.8), top_y, half_w, card_h, border_color=ACCENT_CYAN)
    tb = s14.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Situational Needs"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(16)

    add_bullet_point(tf, "Real-World Contexts", "A viewer's available watching time changes constantly (e.g. quick 2-hour weekend vs 3-month commitment).", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Zero Cold-Start Dependency", "KBR requires zero past user ratings; it evaluates explicit immediate user requirements directly.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "High Precision", "Strictly eliminates anime that violate hard user constraints regardless of how popular they are.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "User Empowerment", "Gives viewers interactive control over the recommendation space.", 16, prefix_color=ACCENT_CYAN)

    add_card(s14, right_x, top_y, half_w, card_h, border_color=ACCENT_INDIGO)
    tb = s14.shapes.add_textbox(Inches(7.166), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "KBR in ANIVIBE"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(16)

    add_bullet_point(tf, "Constraint Box UI", "Integrated directly in the left sidebar of the 'Find What Fits' page.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Domain Knowledge Encoding", "Encodes rules for episode commitment, quality thresholds, and must-include genres.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Continuous Scoring", "Produces a continuous Fit Score (0.0 to 1.0) rather than a crude binary pass/fail cutoff.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "70% Weight in Hybrid", "Serves as the dominant 70% foundation in the hybrid recommendation system.", 16, prefix_color=ACCENT_INDIGO)

    # --------------------------------------------------------------------------
    # 7. KNOWLEDGE BASE (Slide 2/3: Constraints & Rules)
    # --------------------------------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, prs)
    add_header(s15, "7. Knowledge-Based Recommendation (KBR)", "Constraint Solving & Evaluation Rules", "The 3 core constraint rules evaluated against every catalog candidate.")

    add_card(s15, Inches(0.8), top_y, full_w, card_h, border_color=ACCENT_CYAN)
    tb = s15.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), full_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The 3 Core Constraint Rules"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(16)

    add_bullet_point(tf, "Rule 1: Episode Commitment (Hard Limit)", "User selects maximum allowable episode length: episodes ≤ max_episodes. Presets include Short (≤ 13 eps), Medium (≤ 26 eps), Standard (≤ 50 eps), or Any (100 eps).", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Rule 2: Minimum Quality (Hard Threshold)", "User sets a minimum acceptable viewer score: rate ≥ min_rating (range: 2.5 to 4.8 ★). Ensures low-quality productions are filtered out immediately.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Rule 3: Must Include Genres (Hard Requirement)", "User selects mandatory genres (e.g. Action, Romance). All selected required genres must be present in the candidate anime's genre set.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Streamlined Design Decision", "Viewing Moods and Avoid Genres were removed per final architectural refinement to maintain an intuitive, clean interface.", 16, prefix_color=ACCENT_CYAN)

    # --------------------------------------------------------------------------
    # 7. KNOWLEDGE BASE (Slide 3/3: Continuous Fit Scoring)
    # --------------------------------------------------------------------------
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16, prs)
    add_header(s16, "7. Knowledge-Based Recommendation (KBR)", "Continuous Fit Score Formulation", "How constraint satisfaction is converted into a normalized 0.0 to 1.0 fit score.")

    add_card(s16, Inches(0.8), top_y, full_w, card_h, border_color=ACCENT_CYAN)
    tb = s16.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), full_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Continuous KBR Scoring Formula"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "Score_KBR = Baseline(0.85) + Quality_Bonus + Proximity_Bonus"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(16)

    add_bullet_point(tf, "Hard Constraint Gate", "If any hard rule (episodes, min_rating, required_genres) fails, Score_KBR = 0.0 (strictly filtered out).", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Baseline Satisfaction (0.85)", "All titles that successfully satisfy all hard constraints receive a strong base score of 0.85.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Quality Bonus (0.00 to 0.10)", "Calculated as min(0.10, max(0.0, (rate - 3.5) / 15.0)). Rewards exceptional critically acclaimed anime.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Proximity Bonus (0.00 to 0.05)", "Calculated as 0.05 × [1.0 - (episodes / (max_episodes × 2.0))]. Rewards titles that fit comfortably within the time limit.", 16, prefix_color=ACCENT_CYAN)
    add_bullet_point(tf, "Normalized Bound", "Score_KBR is strictly bounded: 0.0 ≤ Score_KBR ≤ 1.0.", 16, prefix_color=ACCENT_CYAN)

    # --------------------------------------------------------------------------
    # 8. HYBRID (Slide 1/4: Concept & Architecture)
    # --------------------------------------------------------------------------
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17, prs)
    add_header(s17, "8. Hybrid Recommendation System", "Concept & System Architecture", "Combining 70% situational requirements with 40% multi-anime user taste profile.")

    add_card(s17, Inches(0.8), top_y, half_w, card_h, border_color=ACCENT_GREEN)
    tb = s17.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Why 70/40 Hybrid Fusion?"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(16)

    add_bullet_point(tf, "Taste Alone Is Not Enough", "A series may match your taste 100%, but if it has 500 episodes when you have only 2 hours, you cannot watch it.", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Constraints Alone Lack Taste", "A 12-episode show with 4.8 ★ is useless if it is in a genre you dislike.", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "The 70/40 Balance", "Allocates 70% weight to situational feasibility and 40% weight to accumulated user genre taste.", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Unified Discovery Page", "Powers the main 'Find What Fits' page in ANIVIBE.", 16, prefix_color=ACCENT_GREEN)

    add_card(s17, right_x, top_y, half_w, card_h, border_color=ACCENT_INDIGO)
    tb = s17.shapes.add_textbox(Inches(7.166), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "System Architecture"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(16)

    add_bullet_point(tf, "Left: Constraint Controls", "Interactive sliders for episode limits, minimum quality, and required genres.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Sidebar: Taste Profile Card", "Displays live status of aggregated user profile vector and number of rated titles.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Right: Ranked Stream", "Candidate anime sorted descending by the unified 70/40 Hybrid score.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "Dual-Score Badges", "Displays individual 'Fit X%' and 'Taste Y%' scores alongside overall match %.", 16, prefix_color=ACCENT_INDIGO)

    # --------------------------------------------------------------------------
    # 8. HYBRID (Slide 2/4: Multi-Anime Composite Taste Vector)
    # --------------------------------------------------------------------------
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18, prs)
    add_header(s18, "8. Hybrid Recommendation System", "Multi-Anime User Taste Profile Vector", "Crucial Design: The system aggregates ALL rated anime genres into a single user vector.")

    add_card(s18, Inches(0.8), top_y, full_w, card_h, border_color=ACCENT_PURPLE)
    tb = s18.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), full_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Single Composite User Profile Vector Construction"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "U_profile = ∑ [ v_i ]   for all rated anime i ∈ User_Ratings"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(16)

    add_bullet_point(tf, "NOT Single-Anime Comparison", "The CBR component in the hybrid system does NOT compare against just one reference anime. It reflects the user's entire accumulated taste.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "Vector Aggregation", "When a user rates Naruto (Action, Shonen, Martial Arts) and Death Note (Mystery, Psychological, Supernatural), both genre vectors sum into U_profile.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "Weighted Genre Affinity", "Genres appearing multiple times across rated titles naturally receive higher weights in U_profile.", 16, prefix_color=ACCENT_PURPLE)
    add_bullet_point(tf, "Cosine Similarity Evaluation", "The composite vector U_profile is compared against candidate anime vector v_candidate: Score_CBR = CosineSim(U_profile, v_candidate).", 16, prefix_color=ACCENT_PURPLE)

    # --------------------------------------------------------------------------
    # 8. HYBRID (Slide 3/4: The 70/40 Formula)
    # --------------------------------------------------------------------------
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19, prs)
    add_header(s19, "8. Hybrid Recommendation System", "The 70/40 Hybrid Mathematical Formula", "Exact weighted fusion combining 70% KBR constraint fit and 40% CBR user taste.")

    add_card(s19, Inches(0.8), top_y, full_w, card_h, border_color=ACCENT_GREEN)
    tb = s19.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), full_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The 70/40 Mathematical Formula"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "Score_Hybrid = 0.70 × Score_KBR  +  0.40 × Score_CBR"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(16)

    add_bullet_point(tf, "70% Weight (KBR Fit)", "0.70 × Score_KBR: Prioritizes hard constraint satisfaction (episode commitment, minimum rating, required genres).", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "40% Weight (CBR Taste)", "0.40 × Score_CBR: Infuses personal taste from the multi-anime aggregated user profile vector.", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Combined Match Percentage", "Match_Pct = min(99%, max(15%, round((Score_Hybrid / 1.10) × 100))). Normalizes total potential score (0.70 + 0.40 = 1.10) to 100%.", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Clean Card Presentation", "Cards display overall Match % alongside dual-score pills (Taste X% • Fit Y%) without distracting reasons accordions.", 16, prefix_color=ACCENT_GREEN)

    # --------------------------------------------------------------------------
    # 8. HYBRID (Slide 4/4: Cold-Start & Live Session Updates)
    # --------------------------------------------------------------------------
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_background(s20, prs)
    add_header(s20, "8. Hybrid Recommendation System", "Cold-Start Handling & Live Session Updates", "How the 70/40 Hybrid adapts dynamically to user interaction in real time.")

    add_card(s20, Inches(0.8), top_y, half_w, card_h, border_color=ACCENT_AMBER)
    tb = s20.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "State A: Cold-Start (0 Ratings)"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(16)

    add_bullet_point(tf, "Zero Crashes", "When a user has rated 0 anime, Score_CBR defaults gracefully to 0.0.", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "100% Functional", "The 70% KBR constraint component remains fully active, ranking candidates by constraint fit.", 16, prefix_color=ACCENT_AMBER)
    add_bullet_point(tf, "Clear UI Notice", "Sidebar indicates: 'Taste profile inactive (0 rated anime). Rate any anime to activate 40% taste weighting.'", 16, prefix_color=ACCENT_AMBER)

    add_card(s20, right_x, top_y, half_w, card_h, border_color=ACCENT_GREEN)
    tb = s20.shapes.add_textbox(Inches(7.166), top_y + Inches(0.4), half_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "State B: Active Taste Profile"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(16)

    add_bullet_point(tf, "Instant Live Recalculation", "The moment a user rates any anime (via modal or card stars), sessionRatings updates in state.", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "40% Taste Activates", "U_profile instantly incorporates the new title's genre vector.", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Real-Time Re-ranking", "Hybrid recommendations automatically refresh live on screen without page reload.", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Taste Badge", "Header badge updates to: 'N Rated Anime Active'.", 16, prefix_color=ACCENT_GREEN)

    # --------------------------------------------------------------------------
    # 9. CONCLUSION
    # --------------------------------------------------------------------------
    s21 = prs.slides.add_slide(blank_layout)
    set_slide_background(s21, prs)
    add_header(s21, "9. Conclusion", "Key Takeaways & Academic Contribution", "Summary of system accomplishments and architectural impact.")

    add_card(s21, Inches(0.8), top_y, full_w, card_h, border_color=ACCENT_INDIGO)
    tb = s21.shapes.add_textbox(Inches(1.1), top_y + Inches(0.4), full_w - Inches(0.6), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Project Summary & Outcomes"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(16)

    add_bullet_point(tf, "1. Comprehensive Decision Support", "Successfully solved anime choice paralysis by addressing consensus, similarity, and situational constraints.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "2. Rigorous Paradigm Separation", "Clear distinction between Bayesian Popularity, 29-Genre Content-Based Filtering, Knowledge-Based Constraints, and 70/40 Hybrid Fusion.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "3. Multi-Anime Profile Vector Innovation", "Constructs a unified composite user taste vector U = ∑ v_i across all rated anime rather than crude single-item comparisons.", 16, prefix_color=ACCENT_INDIGO)
    add_bullet_point(tf, "4. Real-World Streaming Usability", "Zero-dependency client execution delivers instant recommendations with zero latency and complete offline reliability.", 16, prefix_color=ACCENT_INDIGO)

    # --------------------------------------------------------------------------
    # 10. THANK YOU
    # --------------------------------------------------------------------------
    s22 = prs.slides.add_slide(blank_layout)
    set_slide_background(s22, prs)

    add_card(s22, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1), bg_color=CARD_BG, border_color=ACCENT_INDIGO)

    tb = s22.shapes.add_textbox(Inches(2.0), Inches(1.8), Inches(9.333), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "ANIVIBE: Decision Support & Recommendation System"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_after = Pt(24)

    p = tf.add_paragraph()
    p.text = "Questions & Academic Discussion"
    p.font.size = Pt(20)
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(16)

    add_bullet_point(tf, "Live Web Application", "Running locally at http://localhost:3000/", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "GitHub Repository", "https://github.com/manisandar/anime-dsrs.git", 16, prefix_color=ACCENT_GREEN)
    add_bullet_point(tf, "Course", "Assumption University — CSX/ITX 4207 Decision Support and Recommender Systems", 16, prefix_color=ACCENT_GREEN)

    # Save to file
    out_path = os.path.join(os.path.dirname(__file__), "../ANIVIBE_Presentation.pptx")
    prs.save(out_path)
    print(f"✅ White theme presentation successfully saved to: {out_path} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    generate_all_slides()
