#!/usr/bin/env python3
"""
ANIVIBE Presentation Generator (.pptx)
Assumption University — CSX/ITX 4207 Decision Support and Recommendation System
Creates a professional, clean, widescreen (16:9) PowerPoint presentation.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# COLOR PALETTE (Modern Slate & Tech Accent)
# ==============================================================================
BG_DARK = RGBColor(15, 23, 42)       # Slate 900
CARD_BG = RGBColor(30, 41, 59)      # Slate 800
CARD_BORDER = RGBColor(51, 65, 85)  # Slate 700
CARD_MUTED = RGBColor(24, 32, 47)

ACCENT_INDIGO = RGBColor(99, 102, 241) # Primary Accent
ACCENT_PURPLE = RGBColor(168, 85, 247) # Secondary Accent
ACCENT_RED = RGBColor(225, 29, 72)     # Highlight / Brand
ACCENT_CYAN = RGBColor(6, 182, 212)    # Tech / Rules
ACCENT_GREEN = RGBColor(16, 185, 129)  # Success / Metrics
ACCENT_AMBER = RGBColor(245, 158, 11)  # Star / Score

TEXT_WHITE = RGBColor(248, 250, 252) # Slate 50
TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
TEXT_DIM = RGBColor(100, 116, 139)   # Slate 500

FONT_HEADING = "Helvetica"
FONT_BODY = "Arial"

def set_slide_background(slide, prs):
    """Sets a rich dark background rectangle covering the whole slide."""
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background() # No border
    # Send to back
    slide.shapes._spTree.remove(bg._element)
    slide.shapes._spTree.insert(2, bg._element)
    return bg

def add_header(slide, tag_text, title_text, subtitle_text=None):
    """Adds a standard clean header to content slides."""
    # 1. Pill tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.5), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.name = FONT_BODY
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_INDIGO

    # 2. Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    # 3. Optional Subtitle
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.5), Inches(0.4))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Adds a rounded rectangle card container."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def main():
    prs = Presentation()
    # 16:9 Widescreen dimensions: 13.333 x 7.5 inches
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, prs)

    # Accent decorative top bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_RED
    bar.line.fill.background()

    # Center card for title
    add_card(s1, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1), bg_color=CARD_BG, border_color=CARD_BORDER)

    tb = s1.shapes.add_textbox(Inches(2.0), Inches(1.6), Inches(9.333), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ASSUMPTION UNIVERSITY • VINCENT MARY SCHOOL OF SCIENCE & TECHNOLOGY"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "ANIVIBE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "Anime Decision Support & 1+1 Hybrid Recommendation System"
    p.font.name = FONT_HEADING
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(20)

    p = tf.add_paragraph()
    p.text = "Solving the streaming paradox of choice by uniting genuine taste profiles with situational constraints."
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(32)

    # Footer Metadata inside Title Card
    p = tf.add_paragraph()
    p.text = "Course: CSX/ITX 4207 Decision Support and Recommendation System\nLive App: https://minkhanttin-anivibe.static.hf.space   •   Code: github.com/manisandar/anime-dsrs"
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN

    # ==========================================================================
    # SLIDE 2: THE PROBLEM (WHY ANIVIBE?)
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, prs)
    add_header(s2, "Project Motivation & Problem Statement", "The 'Paradox of Choice' in Entertainment Streaming", "Why conventional anime recommendation systems fail modern viewers.")

    # 3 Column Cards
    col_w = Inches(3.64)
    gap = Inches(0.4)
    start_x = Inches(0.8)
    top_y = Inches(1.9)
    card_h = Inches(4.8)

    # Problem 1
    add_card(s2, start_x, top_y, col_w, card_h)
    tb = s2.shapes.add_textbox(start_x + Inches(0.25), top_y + Inches(0.3), col_w - Inches(0.5), card_h - Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "01 • CHOICE OVERLOAD"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Too Many Titles, Too Little Time"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "• Catalogs have over 1,200+ anime titles.\n• Viewers spend 20–30 minutes browsing without deciding.\n• Users suffer from decision fatigue and end up watching nothing."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Problem 2
    add_card(s2, start_x + col_w + gap, top_y, col_w, card_h)
    tb = s2.shapes.add_textbox(start_x + col_w + gap + Inches(0.25), top_y + Inches(0.3), col_w - Inches(0.5), card_h - Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "02 • REAL-WORLD CONSTRAINTS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Context is Usually Ignored"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "• Standard recommenders only look at what you watched in the past.\n• They ignore your time tonight (e.g. only have time for a 12-episode show).\n• They ignore your current mood (e.g. want something chill vs exciting)."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Solution
    add_card(s2, start_x + (col_w + gap) * 2, top_y, col_w, card_h, border_color=ACCENT_INDIGO)
    tb = s2.shapes.add_textbox(start_x + (col_w + gap) * 2 + Inches(0.25), top_y + Inches(0.3), col_w - Inches(0.5), card_h - Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "03 • ANIVIBE SOLUTION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Decision Support + Recommender"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "• Combines personal taste history with active situational constraints.\n• 1+1 Hybrid engine: 50% Taste + 50% Requirement Fit.\n• Transparent explanations: tells the viewer exactly why each show was chosen."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================================================
    # SLIDE 3: 4 RECOMMENDATION PARADIGMS ARCHITECTURE
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, prs)
    add_header(s3, "System Architecture", "The 4 Core Recommendation Paradigms", "Strict academic separation between consensus, taste, rules, and hybrid fusion.")

    # 4 horizontal cards
    card_w = Inches(5.6)
    card_h = Inches(2.35)
    row_gap = Inches(0.3)
    col_gap = Inches(0.5)

    coords = [
        (Inches(0.8), Inches(1.9)),
        (Inches(6.9), Inches(1.9)),
        (Inches(0.8), Inches(4.55)),
        (Inches(6.9), Inches(4.55)),
    ]

    paradigm_info = [
        ("1. POPULARITY BASELINE", "Bayesian Weighted Consensus", "Provides cold-start stability for new visitors without requiring any ratings history. Uses Bayesian smoothing to avoid low-sample bias.", ACCENT_AMBER),
        ("2. CONTENT-BASED FILTERING", "29-Genre Vector Space Matching", "Calculates cosine similarity between 29 anime genres. Builds an active preference vector from user ratings (5★ boosts taste, 1★ reduces).", ACCENT_PURPLE),
        ("3. KNOWLEDGE-BASED RECOMMENDATION", "Constraint Reasoning & Mood Rules", "Acts as an interactive decision filter. Evaluates hard constraints (episodes, rating) and soft domain rules (mood affinity) with clear explanations.", ACCENT_CYAN),
        ("4. 1+1 HYBRID FUSION (SMART MATCH)", "50% Taste + 50% Situational Fit", "Linear combination of Content-Based affinity and Knowledge-Based utility. Handles cold-start gracefully and eliminates overspecialization.", ACCENT_GREEN)
    ]

    for (x, y), (tag, title, desc, col) in zip(coords, paradigm_info):
        add_card(s3, x, y, card_w, card_h, border_color=col)
        tb = s3.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED

    # ==========================================================================
    # SLIDE 4: DATASET & PREPROCESSING
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, prs)
    add_header(s4, "Data Engineering & Preprocessing", "Genuine Dataset & Scientific Vectorization", "Zero synthetic fake users. Grounded in 1,255 real Crunchyroll anime records.")

    # Left: Stats Column (3 stat boxes)
    stat_w = Inches(3.6)
    stat_h = Inches(1.4)
    stat_gap = Inches(0.25)
    top_y = Inches(1.9)

    stats = [
        ("1,255", "Real Anime Titles", "Cleaned Crunchyroll streaming catalog with genuine synopsis, episode counts, and artwork.", ACCENT_RED),
        ("29", "Genre Binary Features", "Action, Shonen, Romance, Sci-Fi, Psychological, Slice of Life, Mystery, etc.", ACCENT_INDIGO),
        ("18,500+", "Viewer Rating Records", "Authentic 5-star distribution breakdowns (rate_1 to rate_5) for Bayesian prior.", ACCENT_AMBER),
    ]

    for i, (val, title, desc, col) in enumerate(stats):
        cy = top_y + i * (stat_h + stat_gap)
        add_card(s4, Inches(0.8), cy, stat_w, stat_h, border_color=col)
        tb = s4.shapes.add_textbox(Inches(1.0), cy + Inches(0.15), stat_w - Inches(0.4), stat_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title + " — " + desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    # Right: Data Pipeline Explanation Card
    add_card(s4, Inches(4.7), top_y, Inches(7.8), Inches(4.7))
    tb = s4.shapes.add_textbox(Inches(5.0), top_y + Inches(0.3), Inches(7.2), Inches(4.1))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "DATA PIPELINE & EVALUATION INTEGRITY"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(14)

    pipeline_points = [
        ("Vector Space Model", "Each anime is encoded as a 29-dimensional binary vector representing presence or absence of specific genres."),
        ("No Data Leakage (80/20 Holdout)", "20% of interaction ratings were sequestered in an untouched test vault to simulate real unobserved future user choices during metric evaluation."),
        ("Community Consensus Priors", "Multi-star histograms (1 to 5 stars) are loaded for every title, enabling real-time vote distribution charts inside the detail hero view."),
        ("Zero Synthetic Users", "All evaluations use genuine user interactions rather than fabricated artificial test accounts.")
    ]

    for title, body in pipeline_points:
        p = tf.add_paragraph()
        p.text = f"• {title}: {body}"
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    # ==========================================================================
    # SLIDE 5: POPULARITY-BASED RECOMMENDATION
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, prs)
    add_header(s5, "Recommendation Paradigm 1", "Popularity Baseline (Bayesian Weighted Rating)", "Independent consensus ranking serving as the non-personalized cold-start baseline.")

    # Left Card: Formula & Logic
    add_card(s5, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8), border_color=ACCENT_AMBER)
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "MATHEMATICAL FORMULATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Weighted Bayesian Rating (WR)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "WR = ( v / (v + m) ) × R + ( m / (v + m) ) × C\n"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• v = Number of votes for the anime\n• m = Minimum threshold prior (m = 100 votes)\n• R = Average viewer score of the anime\n• C = Global catalog mean score (C = 3.65)\n\nWhy this is important:\nA title with one 5.0★ review will NOT outrank a legendary title with 4.8★ across 50,000 community votes."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Right Card: Characteristics & UI
    add_card(s5, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8))
    tb = s5.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ROLE IN THE SYSTEM & BEHAVIOR"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Key Characteristics"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "• Always Available:\n  Displayed on the Home page as 'Popular Right Now' without needing any user ratings.\n\n• High Diversity Across Genres (0.7801):\n  Spans shonen, slice-of-life, sports, and fantasy blockbusters.\n\n• The Trade-off:\n  Zero personalization. Shows the same consensus titles to all users regardless of personal taste."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================================================
    # SLIDE 6: CONTENT-BASED FILTERING (CBF)
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, prs)
    add_header(s6, "Recommendation Paradigm 2", "Content-Based Filtering (Cosine Similarity)", "Pairing item genre vectors with dynamic session user preference profiles.")

    # Left: Item-to-Item
    add_card(s6, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8))
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ITEM-TO-ITEM SIMILARITY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "'More Like This' (Detail Page)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "sim(A, B) = ( A • B ) / ( ||A|| × ||B|| )\n"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• Computes Euclidean dot-product of 29-genre binary feature vectors.\n• Displayed as a single horizontal Netflix-style row with left/right carousel navigation.\n• Independent of user profile; lets users explore titles directly similar to what they are viewing."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Right: Personalized Profile
    add_card(s6, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8))
    tb = s6.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "PERSONALIZED USER PROFILING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "'Recommended For You'"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Profile Vector Centering Weight:\nw_i = Rating - 3.0\n"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• 5★ rating: +2.0 weight (strongly loved genre)\n• 4★ rating: +1.0 weight (mild affinity)\n• 3★ rating: 0.0 weight (neutral, ignored)\n• 2★ rating: -1.0 weight (penalized genre)\n• 1★ rating: -2.0 weight (strongly avoided)\n• Negative sum is clamped at 0 to maintain positive preference magnitude."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================================================
    # SLIDE 7: KNOWLEDGE-BASED RECOMMENDATION (KBR)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, prs)
    add_header(s7, "Recommendation Paradigm 3", "Knowledge-Based Recommendation & Decision Rules", "Evaluating situational constraints, domain commitment rules, and viewing mood.")

    # 3 Cards: Hard Rules, Domain Rules, Explainability
    card_w = Inches(3.64)
    gap = Inches(0.4)
    start_x = Inches(0.8)
    top_y = Inches(1.9)
    card_h = Inches(4.8)

    # 1. Hard Constraints
    add_card(s7, start_x, top_y, card_w, card_h)
    tb = s7.shapes.add_textbox(start_x + Inches(0.2), top_y + Inches(0.25), card_w - Inches(0.4), card_h - Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EXPLICIT FILTERS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "Hard Constraints"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• Episode Budget:\n  Limits maximum episodes (e.g. ≤ 26 episodes for a weekend binge).\n\n• Minimum Quality:\n  Candidate must have rating ≥ specified score (e.g. ≥ 4.0★).\n\n• Genre Requirements:\n  Must include required genres and strictly exclude unwanted genres."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # 2. Domain Knowledge Rules
    add_card(s7, start_x + card_w + gap, top_y, card_w, card_h)
    tb = s7.shapes.add_textbox(start_x + card_w + gap + Inches(0.2), top_y + Inches(0.25), card_w - Inches(0.4), card_h - Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DOMAIN LOGIC"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "Domain Rules & Mood"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• Commitment Rule:\n  ≤ 13 eps = Short\n  14–26 eps = Medium\n  > 26 eps = Long commitment\n\n• Viewing Mood Affinities:\n  - Exciting: Action, Shonen, Tournament\n  - Chill: Slice of Life, Comedy, Romance\n  - Dark: Psychological, Thriller, Horror\n  - Emotional: Drama, Romance"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # 3. Transparent Explainability
    add_card(s7, start_x + (card_w + gap) * 2, top_y, card_w, card_h, border_color=ACCENT_GREEN)
    tb = s7.shapes.add_textbox(start_x + (card_w + gap) * 2 + Inches(0.2), top_y + Inches(0.25), card_w - Inches(0.4), card_h - Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EXPLAINABLE AI"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "Rule Transparency"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• Zero Black-Box Decisions:\n  Outputs a transparent checklist for every recommended show.\n\n• Clear Verdicts:\n  Target vs Actual for episode length, minimum score, and genre constraints.\n\n• Decision Confidence:\n  Viewers see exactly why an anime matches their current situation."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================================================
    # SLIDE 8: 1+1 HYBRID RECOMMENDATION (SMART MATCH)
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, prs)
    add_header(s8, "Recommendation Paradigm 4", "1+1 Hybrid Fusion ('Smart Match')", "The core innovation uniting personal taste with real-world situational constraints.")

    # Left: Formula & Architecture
    add_card(s8, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8), border_color=ACCENT_INDIGO)
    tb = s8.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "HYBRID FUSION FORMULA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Balanced 50/50 Architecture"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Score_Hybrid = 0.50 × S_CBF + 0.50 × S_KBR\n"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "• 50% Personal Taste (CBF):\n  Grounded in user's rated anime history and genre preference vectors.\n\n• 50% Situational Fit (KBR):\n  Grounded in current episode availability, quality thresholds, and mood.\n\n• Why Both Matter:\n  High taste alone is useless if the show is 500 episodes long when you only have 3 hours."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Right: Cold-Start Strategy & Benefits
    add_card(s8, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8))
    tb = s8.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "COLD-START RESILIENCE & ADVANTAGES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Switching Hybrid Handling"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "• 0 Ratings (Cold Start):\n  If the user has not rated any anime yet, the system detects this state immediately and prompts them with popular titles to rate.\n\n• Switching Strategy:\n  Can fall back smoothly to Knowledge-Based filter without crashing.\n\n• Solves Overspecialization:\n  Adding constraint rules introduces healthy serendipity, boosting diversity without losing accuracy."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================================================
    # SLIDE 9: ACADEMIC BENCHMARK EVALUATION
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, prs)
    add_header(s9, "Empirical Validation & Results", "Academic Evaluation Benchmark Metrics", "Verified offline benchmark testing on holdout ratings (Precision, Recall, Diversity, Coverage).")

    # Table of Results
    rows = 5
    cols = 5
    left = Inches(0.8)
    top = Inches(1.9)
    width = Inches(11.7)
    height = Inches(2.2)

    table_shape = s9.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(3.7)
    table.columns[1].width = Inches(2.0)
    table.columns[2].width = Inches(2.0)
    table.columns[3].width = Inches(2.0)
    table.columns[4].width = Inches(2.0)

    headers = ["Recommendation Paradigm", "Precision@10", "Recall@10", "Diversity", "Coverage"]
    data = [
        ["Popularity Baseline", "0.3000", "0.0158", "0.7801", "0.8%"],
        ["Content-Based Filtering (CBF)", "0.5500", "0.0380", "0.1334", "3.2%"],
        ["Knowledge-Based Filtering (KBR)", "0.7750", "0.0933", "0.5248", "2.4%"],
        ["1+1 Hybrid (CBF + KBR)", "1.0000", "0.1175", "0.2017", "3.2%"]
    ]

    for c_idx, text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BORDER
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    for r_idx, row in enumerate(data):
        is_hybrid = (r_idx == 3)
        for c_idx, text in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if not is_hybrid else RGBColor(39, 45, 75)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(13)
            p.font.bold = is_hybrid or (c_idx == 0)
            p.font.color.rgb = ACCENT_GREEN if (is_hybrid and c_idx > 0) else TEXT_WHITE
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    # Defense Takeaways Card below Table
    add_card(s9, Inches(0.8), Inches(4.4), Inches(11.7), Inches(2.4))
    tb = s9.shapes.add_textbox(Inches(1.1), Inches(4.55), Inches(11.1), Inches(2.1))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "KEY DEFENSE INSIGHTS FOR THE COMMITTEE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(8)

    points = [
        ("Highest Overall Precision (1.0000)", "The 1+1 Hybrid achieves perfect Top-10 relevant hits on test test profiles by filtering out irrelevant lengths and aligning with loved genres."),
        ("Resolves CBF Overspecialization (+51% Diversity Boost)", "Content-Based alone has low diversity (0.1334). The 1+1 Hybrid increases diversity to 0.2017 while keeping recommendations relevant."),
        ("No Data Leakage", "All metrics were computed using our Python evaluation suite (recommender/evaluate.py) against unobserved holdout test ratings.")
    ]

    for title, desc in points:
        p = tf.add_paragraph()
        p.text = f"• {title}: {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

    # ==========================================================================
    # SLIDE 10: USER INTERFACE & DEMONSTRATION
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, prs)
    add_header(s10, "Modern User Interface", "Interactive Decision Platform Experience", "Clean, Netflix-style interface designed for effortless discovery and decision making.")

    col_w = Inches(3.64)
    gap = Inches(0.4)
    start_x = Inches(0.8)
    top_y = Inches(1.9)
    card_h = Inches(4.8)

    features = [
        ("SMART MATCH PAGE", "Interactive Decision Sliders", "Users adjust episode budgets (≤ 26, ≤ 50), minimum rating thresholds, mood pills, and genre filters with real-time score updates.", ACCENT_INDIGO),
        ("ANIME DETAIL VIEW", "Hero & Rating Histogram", "Includes community 1–5 star vote breakdown histograms inside the hero view, alongside a single-row Netflix carousel for 'More Like This'.", ACCENT_AMBER),
        ("ZERO-LATENCY ENGINE", "Instant Browser Math (< 3ms)", "Both pure Python microservice AND client-side local engine ensure instantaneous calculation of dot-products and constraint checks.", ACCENT_GREEN)
    ]

    for i, (tag, title, desc, col) in enumerate(features):
        x = start_x + i * (col_w + gap)
        add_card(s10, x, top_y, col_w, card_h, border_color=col)
        tb = s10.shapes.add_textbox(x + Inches(0.2), top_y + Inches(0.3), col_w - Inches(0.4), card_h - Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(12)

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(14)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED

    # ==========================================================================
    # SLIDE 11: DEPLOYMENT & PRODUCTION ARCHITECTURE
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, prs)
    add_header(s11, "Cloud Deployment & Open-Source Engineering", "100% Free Cloud Deployment Architecture", "Publicly accessible worldwide with zero server maintenance overhead.")

    # Left: Hugging Face Live Space
    add_card(s11, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.8), border_color=ACCENT_INDIGO)
    tb = s11.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "LIVE CLOUD DEPLOYMENT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Hugging Face Spaces"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "• Live Public URL:\n  https://minkhanttin-anivibe.static.hf.space\n\n• Zero Downtime & Global CDN:\n  Served directly from Hugging Face cloud infrastructure.\n\n• Mobile & Tablet Ready:\n  Responsive layout works smoothly on phones, tablets, and desktops anywhere in the world."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Right: GitHub Open-Source Repo
    add_card(s11, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.8), border_color=ACCENT_PURPLE)
    tb = s11.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "OPEN-SOURCE CODEBASE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "GitHub Repository"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "• Official Repository:\n  https://github.com/manisandar/anime-dsrs\n\n• Complete Implementation:\n  Includes core Python algorithms, evaluation suite, and full React client code.\n\n• Reproducible Benchmarks:\n  Anyone can clone and run 'python3 recommender/evaluate.py' to reproduce the benchmark table."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================================================
    # SLIDE 12: CONCLUSION & Q&A
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, prs)

    add_card(s12, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1), border_color=ACCENT_INDIGO)
    tb = s12.shapes.add_textbox(Inches(2.0), Inches(1.8), Inches(9.333), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SUMMARY & CONCLUSION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "Thank You!"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "Key Project Takeaways:\n1. Successfully implemented and compared 4 academic recommendation paradigms.\n2. 1+1 Hybrid achieves 1.0000 Precision@10 while eliminating overspecialization.\n3. Transparent explanations empower users to make confident streaming decisions.\n4. Deployed 100% online with zero server costs."
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(22)

    p = tf.add_paragraph()
    p.text = "Questions & Live Demonstration Discussion"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    # Save output
    output_path = os.path.join(os.path.dirname(__file__), "..", "ANIVIBE_Presentation.pptx")
    prs.save(output_path)
    print(f"✅ Presentation successfully generated at: {output_path}")

if __name__ == "__main__":
    main()
