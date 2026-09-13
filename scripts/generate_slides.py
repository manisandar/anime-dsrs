#!/usr/bin/env python3
"""
ANIVIBE Professional Presentation Generator (.pptx)
Assumption University — CSX/ITX 4207 Decision Support and Recommendation System

Design Rules Applied:
- Minimum font size: 18 pt for ALL text (body text: 18-20 pt, headings: 22-26 pt, titles: 32-38 pt).
- High visual readability: widescreen 16:9, generous spacing, modern dark card layout.
- Simple, clear, presentation-friendly English.
- Broken into 16 focused, uncluttered slides with definitions, formulas, and examples.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# COLOR PALETTE (Professional Dark Slate & Vibrant Accents)
# ==============================================================================
BG_DARK      = RGBColor(15, 23, 42)      # Slate 900
CARD_BG      = RGBColor(30, 41, 59)     # Slate 800
CARD_BORDER  = RGBColor(51, 65, 85)     # Slate 700

ACCENT_INDIGO = RGBColor(99, 102, 241)  # Primary Brand Accent
ACCENT_PURPLE = RGBColor(168, 85, 247)  # Secondary Accent
ACCENT_RED    = RGBColor(225, 29, 72)   # Highlight / Brand
ACCENT_CYAN   = RGBColor(6, 182, 212)   # Rules / Technology
ACCENT_GREEN  = RGBColor(16, 185, 129)  # Success / Metrics
ACCENT_AMBER  = RGBColor(245, 158, 11)  # Scores / Ratings

TEXT_WHITE   = RGBColor(248, 250, 252) # Pure White
TEXT_LIGHT   = RGBColor(226, 232, 240) # Slate 200 (Body text)
TEXT_MUTED   = RGBColor(148, 163, 184) # Slate 400 (Secondary descriptions)

FONT_HEADING = "Helvetica"
FONT_BODY    = "Arial"

def set_slide_background(slide, prs):
    """Sets a rich dark background rectangle covering the full slide."""
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()
    # Send to back
    slide.shapes._spTree.remove(bg._element)
    slide.shapes._spTree.insert(2, bg._element)
    return bg

def add_header(slide, tag_text, title_text, subtitle_text=None):
    """Adds a standard clean header to content slides."""
    # 1. Pill tag (18 pt bold)
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.name = FONT_BODY
    p_tag.font.size = Pt(18)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_INDIGO

    # 2. Main Title (32 pt bold)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(32)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    # 3. Subtitle (20 pt)
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.42), Inches(11.7), Inches(0.45))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(20)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Adds a rounded rectangle card container."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
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
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_RED
    bar.line.fill.background()

    # Large Center Card
    add_card(s1, Inches(1.2), Inches(1.1), Inches(10.933), Inches(5.3), bg_color=CARD_BG, border_color=CARD_BORDER)

    tb = s1.shapes.add_textbox(Inches(1.8), Inches(1.5), Inches(9.733), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ASSUMPTION UNIVERSITY • VINCENT MARY SCHOOL OF SCIENCE & TECHNOLOGY"
    p.font.name = FONT_BODY
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "ANIVIBE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "Anime Decision Support & 1+1 Hybrid Recommendation System"
    p.font.name = FONT_HEADING
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(18)

    p = tf.add_paragraph()
    p.text = "A modern decision intelligence platform combining genuine user taste with situational constraints."
    p.font.name = FONT_BODY
    p.font.size = Pt(20)
    p.font.color.rgb = TEXT_LIGHT
    p.space_after = Pt(28)

    p = tf.add_paragraph()
    p.text = "Course: CSX/ITX 4207 Decision Support and Recommendation System\nLive App: https://minkhanttin-anivibe.static.hf.space   •   Code: github.com/manisandar/anime-dsrs"
    p.font.name = FONT_BODY
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    # ==========================================================================
    # SLIDE 2: PROBLEM STATEMENT (THE PARADOX OF CHOICE)
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, prs)
    add_header(s2, "Problem Statement & Motivation", "The 'Paradox of Choice' in Streaming", "Why viewers struggle to pick an anime, and why typical recommenders fail.")

    col_w = Inches(5.65)
    card_h = Inches(4.7)
    top_y = Inches(2.15)

    # Left: Choice Overload
    add_card(s2, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_RED)
    tb = s2.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Choice Overload Problem"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    bullets = [
        "Massive Catalogs: Streaming services offer over 1,200+ anime titles.",
        "Decision Fatigue: Viewers spend 20 to 30 minutes browsing endlessly.",
        "Abandoned Sessions: Overwhelmed users often give up without watching anything.",
        "Generic Carousels: Conventional homepages only promote the same top 10 blockbusters."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # Right: The Context Blind Spot
    add_card(s2, Inches(6.883), top_y, col_w, card_h, border_color=ACCENT_AMBER)
    tb = s2.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Context Blind Spot"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    bullets = [
        "Ignores Time Limits: Recommending a 500-episode anime is useless when you only have tonight.",
        "Ignores Viewer Mood: Recommenders ignore whether you feel like laughing or watching drama.",
        "Only Looks Backward: Traditional systems only look at past ratings, not current needs.",
        "Black-Box Suggestions: Users are rarely told why a title was selected for them."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 3: OUR SOLUTION (DECISION SUPPORT + RECOMMENDER)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, prs)
    add_header(s3, "Project Vision & Architecture", "The ANIVIBE Solution", "A dual-purpose platform combining personal taste with situational decision rules.")

    add_card(s3, Inches(0.8), top_y, Inches(11.733), card_h, border_color=ACCENT_INDIGO)
    tb = s3.shapes.add_textbox(Inches(1.2), top_y + Inches(0.4), Inches(10.933), card_h - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "How ANIVIBE Bridges Taste and Situation"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(20)

    solution_items = [
        ("1. Taste Profile (Content-Based)", "Learns your favorite genres dynamically from your 1-to-5 star ratings without requiring fake synthetic user accounts."),
        ("2. Real-World Constraints (Knowledge-Based)", "Filters titles based on your current time budget (episode count), minimum score, and viewing mood."),
        ("3. 1+1 Hybrid Fusion ('Smart Match')", "Combines 50% Personal Taste with 50% Situational Fit into a unified score so every recommendation fits both your taste and your schedule."),
        ("4. Transparent Explainability", "Provides clear checklists showing why an anime matched or was excluded, eliminating black-box mystery.")
    ]
    for title, desc in solution_items:
        p = tf.add_paragraph()
        p.text = f"•  {title}: {desc}"
        p.font.size = Pt(19)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(14)

    # ==========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE (4 PARADIGMS)
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, prs)
    add_header(s4, "Core Engineering", "4 Distinct Recommendation Paradigms", "Strict academic separation between consensus, taste, rules, and hybrid fusion.")

    # 4 distinct cards in 2x2 grid
    card_w = Inches(5.65)
    card_h = Inches(2.2)
    x_left = Inches(0.8)
    x_right = Inches(6.883)
    y_row1 = Inches(2.15)
    y_row2 = Inches(4.65)

    paradigms = [
        (x_left, y_row1, "1. Popularity Baseline", "Consensus Ranking", "Uses Bayesian smoothing to rank globally loved anime. Serves as the cold-start baseline for new visitors with 0 ratings.", ACCENT_AMBER),
        (x_right, y_row1, "2. Content-Based Filtering", "Genre Vector Space Model", "Calculates cosine similarity across 29 genres. Powers 'More Like This' and builds user taste vectors from active ratings.", ACCENT_PURPLE),
        (x_left, y_row2, "3. Knowledge-Based Recommendation", "Constraint Satisfaction & Rules", "Filters candidate anime using hard limits (episodes, rating) and soft domain rules (viewing mood) with clear explanations.", ACCENT_CYAN),
        (x_right, y_row2, "4. 1+1 Hybrid Fusion", "Smart Match Engine", "Equally combines 50% User Taste with 50% Situational Fit. Solves overspecialization and provides personalized results.", ACCENT_GREEN)
    ]

    for x, y, title, subtitle, desc, col in paradigms:
        add_card(s4, x, y, card_w, card_h, border_color=col)
        tb = s4.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), card_w - Inches(0.5), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{title} • {subtitle}"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT

    # ==========================================================================
    # SLIDE 5: DATASET & PREPROCESSING PIPELINE
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, prs)
    add_header(s5, "Data Engineering", "Dataset & Preprocessing Pipeline", "Authentic Crunchyroll streaming dataset with zero synthetic users.")

    add_card(s5, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_INDIGO)
    tb = s5.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Dataset Highlights"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    data_stats = [
        "1,255 Cleaned Anime Titles: Complete metadata from the Crunchyroll catalog including synopsis, artwork, and episodes.",
        "29 Binary Genre Features: Each anime is encoded into a 29-dimensional vector (Action, Shonen, Romance, Sci-Fi, etc.).",
        "18,500+ Community Ratings: Authentic multi-star distribution histograms (1★ to 5★ votes) for every anime.",
        "Zero Synthetic Users: All user tests are based on real interaction sessions, preserving academic integrity."
    ]
    for s in data_stats:
        p = tf.add_paragraph()
        p.text = f"•  {s}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # Right: Preprocessing & Holdout
    add_card(s5, Inches(6.883), top_y, col_w, card_h, border_color=ACCENT_GREEN)
    tb = s5.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Evaluation Integrity"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    integrity_items = [
        "80/20 Train-Test Split: 20% of ratings were held out in a test vault to simulate unobserved future choices.",
        "No Data Leakage: Evaluation metrics only test against the holdout set, guaranteeing objective benchmark scores.",
        "Vector Normalization: L2 Euclidean normalization is applied to genre vectors to ensure fair cosine similarity comparisons.",
        "Lightweight Catalog (< 1 MB): Optimized JSON format loads in milliseconds and runs directly in the browser."
    ]
    for item in integrity_items:
        p = tf.add_paragraph()
        p.text = f"•  {item}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 6: PARADIGM 1 — POPULARITY BASELINE
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, prs)
    add_header(s6, "Recommendation Paradigm 1", "Popularity Baseline (Bayesian Consensus)", "Solving low-sample rating bias with weighted Bayesian consensus ranking.")

    add_card(s6, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_AMBER)
    tb = s6.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Bayesian Rating Formula"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "WR = ( v / (v + m) ) × R + ( m / (v + m) ) × C"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(16)

    formula_items = [
        "v = Number of ratings/votes for this anime",
        "m = Minimum vote threshold prior (m = 100 votes)",
        "R = Average viewer rating for this anime",
        "C = Global mean rating across the entire catalog (C = 3.65)",
        "Weighted Consensus: As votes (v) increase, the score shifts smoothly from the global mean (C) to the anime's true rating (R)."
    ]
    for f in formula_items:
        p = tf.add_paragraph()
        p.text = f"•  {f}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # Right: Concrete Example
    add_card(s6, Inches(6.883), top_y, col_w, card_h)
    tb = s6.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Why This Prevents Unfair Bias"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    example_bullets = [
        "The 1-Vote Flaw: Without Bayesian smoothing, a movie with a single 5.0★ vote would rank #1 overall.",
        "The Solution: With m = 100, an anime with 1 vote of 5.0★ drops to WR ≈ 3.66★ (pulled toward average).",
        "Fair Classic Recognition: A popular classic with 4.8★ across 50,000 votes achieves WR ≈ 4.80★.",
        "Role in ANIVIBE: Displayed on the Home page as 'Popular Right Now' to welcome new users with 0 ratings."
    ]
    for eb in example_bullets:
        p = tf.add_paragraph()
        p.text = f"•  {eb}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 7: PARADIGM 2 — CBF (ITEM-TO-ITEM SIMILARITY)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, prs)
    add_header(s7, "Recommendation Paradigm 2A", "Content-Based Item Similarity", "Pairing anime using Cosine Similarity on 29-genre binary feature vectors.")

    add_card(s7, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_PURPLE)
    tb = s7.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Cosine Similarity Math"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "sim(A, B) = ( A • B ) / ( ||A|| × ||B|| )"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(16)

    sim_bullets = [
        "A and B are 29-dimensional binary vectors where 1 represents genre presence and 0 represents absence.",
        "A • B computes the count of shared overlapping genres between the two titles.",
        "||A|| × ||B|| normalizes the score by vector lengths so titles with many genres do not artificially dominate.",
        "Produces an intuitive similarity percentage from 0% (no overlap) to 100% (identical genre fingerprint)."
    ]
    for b in sim_bullets:
        p = tf.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # Right: "More Like This" UI
    add_card(s7, Inches(6.883), top_y, col_w, card_h)
    tb = s7.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "How It Works on Detail Page"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    ui_bullets = [
        "'More Like This' Row: Displayed on the Anime Detail page directly below the anime information.",
        "Netflix-Style Carousel: Shows recommendations in a single horizontal row with left/right navigation arrows.",
        "Concrete Example: If viewing Naruto (Action, Shonen, Martial Arts), it recommends titles with identical high genre overlap.",
        "Independent of User History: Lets users explore similar shows even before rating any titles."
    ]
    for ub in ui_bullets:
        p = tf.add_paragraph()
        p.text = f"•  {ub}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 8: PARADIGM 2 — CBF (PERSONALIZED USER PROFILE)
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, prs)
    add_header(s8, "Recommendation Paradigm 2B", "Personalized Content-Based Filtering", "Dynamically learning user taste vectors from active 1-to-5 star ratings.")

    add_card(s8, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_INDIGO)
    tb = s8.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Centered Taste Weighting"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "Genre Weight = Rating − 3.0"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(16)

    weight_table = [
        "5★ Rating = +2.0 (Strongly loved genre; heavy boost)",
        "4★ Rating = +1.0 (Mild preference; positive boost)",
        "3★ Rating = 0.0 (Neutral; zero effect on taste profile)",
        "2★ Rating = −1.0 (Mild dislike; penalizes genre)",
        "1★ Rating = −2.0 (Strongly avoided; heavy penalty)"
    ]
    for w in weight_table:
        p = tf.add_paragraph()
        p.text = f"•  {w}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # Right: Profile Vector Construction
    add_card(s8, Inches(6.883), top_y, col_w, card_h)
    tb = s8.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "User Profile Construction"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    profile_bullets = [
        "Active Session Learning: Taste vector updates in real time immediately after each star rating is submitted.",
        "Non-Negative Preference (ReLU): Negative sums are clamped at 0 to maintain a positive genre preference magnitude.",
        "Candidate Ranking: Every unrated anime is scored against the normalized user vector via Cosine Similarity.",
        "High Precision: Delivers 0.5500 Precision@10, accurately targeting the viewer's favorite genre clusters."
    ]
    for pb in profile_bullets:
        p = tf.add_paragraph()
        p.text = f"•  {pb}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 9: PARADIGM 3 — KBR (CONSTRAINTS & RULES)
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, prs)
    add_header(s9, "Recommendation Paradigm 3A", "Knowledge-Based Decision Constraints", "Evaluating user situation limits through hard constraint satisfaction.")

    add_card(s9, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_CYAN)
    tb = s9.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Explicit Hard Constraints"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    hard_rules = [
        "Episode Budget Limit: Candidate must have episodes ≤ user limit (e.g. ≤ 13 eps for a single evening).",
        "Minimum Quality Threshold: Candidate must have viewer score ≥ user minimum (e.g. rating ≥ 4.0★).",
        "Required Genres: Candidate must include all selected required genres (e.g. must include Sci-Fi).",
        "Excluded Genres: Candidate must NOT contain any forbidden genres (e.g. avoid Horror)."
    ]
    for hr in hard_rules:
        p = tf.add_paragraph()
        p.text = f"•  {hr}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # Right: Domain Knowledge Rules
    add_card(s9, Inches(6.883), top_y, col_w, card_h)
    tb = s9.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Domain Knowledge Rules"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    domain_rules = [
        "Viewing Commitment Rule: Categorizes anime length into clear commitment tiers:\n   - Short: ≤ 13 episodes (quick finish)\n   - Medium: 14 to 26 episodes (weekend binge)\n   - Long: > 26 episodes (extended series)",
        "Zero Past History Needed: Functions as an on-demand decision filter; works 100% on day one.",
        "High Utility Focus: Guarantees that every returned title strictly fits the user's available time."
    ]
    for dr in domain_rules:
        p = tf.add_paragraph()
        p.text = f"•  {dr}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 10: PARADIGM 3 — KBR (MOOD & EXPLAINABILITY)
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, prs)
    add_header(s10, "Recommendation Paradigm 3B", "Viewing Mood & Explainable AI", "Mapping emotional mood to genres and providing transparent reasoning checklists.")

    add_card(s10, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_PURPLE)
    tb = s10.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Mood-to-Genre Domain Mapping"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    moods = [
        "Exciting Mood: Action, Shonen, Tournament, Super Power, Martial Arts.",
        "Chill Mood: Slice of Life, Comedy, Light Romance.",
        "Dark Mood: Psychological, Thriller, Horror, Mystery.",
        "Emotional Mood: Drama, Romance, Emotional Slice of Life.",
        "Soft Multiplier: Mood match provides an additive score bonus (+0.15) to boost candidate ranking."
    ]
    for m in moods:
        p = tf.add_paragraph()
        p.text = f"•  {m}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # Right: Explainable AI
    add_card(s10, Inches(6.883), top_y, col_w, card_h, border_color=ACCENT_GREEN)
    tb = s10.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Transparent Explainable AI (XAI)"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    xai_points = [
        "Zero Black-Box Decisions: Users are never left wondering why an anime appeared.",
        "Transparent Evaluation Checklist: Every title displays a clear verdict table:\n   - Episode Limit: Target ≤ 26 vs Actual 12 eps (Passed)\n   - Quality Score: Target ≥ 4.0 vs Actual 4.3★ (Passed)\n   - Mood Overlap: Matched 'Action, Shonen' (Passed)",
        "Builds User Trust: Explaining the reasoning boosts viewer confidence in recommendations."
    ]
    for x in xai_points:
        p = tf.add_paragraph()
        p.text = f"•  {x}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # ==========================================================================
    # SLIDE 11: PARADIGM 4 — 1+1 HYBRID FUSION (SMART MATCH)
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, prs)
    add_header(s11, "Recommendation Paradigm 4A", "1+1 Hybrid Fusion ('Smart Match')", "Balancing personal taste with situational constraints in a unified mathematical model.")

    add_card(s11, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_INDIGO)
    tb = s11.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Hybrid Formula"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "Score_Hybrid = 0.50 × S_CBF + 0.50 × S_KBR"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(16)

    hybrid_bullets = [
        "50% User Taste (S_CBF): Cosine similarity between candidate anime and the user's rated genre profile.",
        "50% Requirement Fit (S_KBR): Continuous utility score reflecting episode fit, score bonus, and mood overlap.",
        "Multi-Dimensional Scoring: Displays both individual match percentages (Taste % and Constraint %) alongside overall Hybrid Match %."
    ]
    for b in hybrid_bullets:
        p = tf.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # Right: Why 50/50 Works
    add_card(s11, Inches(6.883), top_y, col_w, card_h)
    tb = s11.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Why Both Components Are Vital"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    reasons = [
        "Taste Alone is Incomplete: A show may match your taste 100%, but if it has 500 episodes when you only have tonight, it is useless.",
        "Constraints Alone Lack Flavor: A filter alone might find a 12-episode show with 4.5★, but in a genre you completely dislike.",
        "The Synergy: The 1+1 Hybrid guarantees that every top recommendation is both genuinely loved AND realistically watchable right now."
    ]
    for r in reasons:
        p = tf.add_paragraph()
        p.text = f"•  {r}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(14)

    # ==========================================================================
    # SLIDE 12: PARADIGM 4 — COLD-START & DIVERSITY
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, prs)
    add_header(s12, "Recommendation Paradigm 4B", "Cold-Start Handling & Diversity", "Switching hybrid architecture that eliminates cold-start crashes and overspecialization.")

    add_card(s12, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_GREEN)
    tb = s12.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Graceful Cold-Start Strategy"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    cold_bullets = [
        "0 Ratings Detection: When a visitor has not rated any titles, Smart Match detects cold-start immediately.",
        "Interactive Onboarding: Shows a clean banner prompting the user to rate 2 or 3 titles to unlock taste scoring.",
        "Switching Fallback: Seamlessly routes queries through Knowledge-Based constraint filters without throwing errors.",
        "Zero System Crashes: Ensures 100% stability regardless of whether the user is brand new or an experienced rater."
    ]
    for cb in cold_bullets:
        p = tf.add_paragraph()
        p.text = f"•  {cb}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # Right: Solving Overspecialization
    add_card(s12, Inches(6.883), top_y, col_w, card_h, border_color=ACCENT_PURPLE)
    tb = s12.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Overcoming Overspecialization"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    over_bullets = [
        "The Echo Chamber Problem: Pure Content-Based recommenders suffer from low diversity (0.1334), trapping users in one genre.",
        "Healthy Serendipity: Knowledge constraints (mood, length) pull candidates from neighboring genres that still fit the situation.",
        "+51% Diversity Improvement: The 1+1 Hybrid increases recommendation diversity from 0.1334 to 0.2017.",
        "Best of Both Worlds: Delivers fresh variety while preserving 100% relevance to the user's current needs."
    ]
    for ob in over_bullets:
        p = tf.add_paragraph()
        p.text = f"•  {ob}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 13: ACADEMIC BENCHMARK EVALUATION (TABLE)
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, prs)
    add_header(s13, "Empirical Validation", "Academic Evaluation Benchmark Metrics", "Offline benchmark results verified on holdout ratings (python3 recommender/evaluate.py).")

    # Table of Results (Font size 18 pt bold / normal)
    rows = 5
    cols = 5
    t_left = Inches(0.8)
    t_top = Inches(2.15)
    t_width = Inches(11.733)
    t_height = Inches(2.6)

    table_shape = s13.shapes.add_table(rows, cols, t_left, t_top, t_width, t_height)
    table = table_shape.table

    table.columns[0].width = Inches(4.133)
    table.columns[1].width = Inches(1.9)
    table.columns[2].width = Inches(1.9)
    table.columns[3].width = Inches(1.9)
    table.columns[4].width = Inches(1.9)

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
        p.font.size = Pt(18)
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
            p.font.size = Pt(18)
            p.font.bold = is_hybrid or (c_idx == 0)
            p.font.color.rgb = ACCENT_GREEN if (is_hybrid and c_idx > 0) else TEXT_WHITE
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    # Defense Takeaways Card below Table
    c_top = Inches(4.95)
    c_height = Inches(2.0)
    add_card(s13, Inches(0.8), c_top, Inches(11.733), c_height, border_color=ACCENT_CYAN)
    tb = s13.shapes.add_textbox(Inches(1.1), c_top + Inches(0.2), Inches(11.133), c_height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key Defense Insights for Dr. Benjawan"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(8)

    takeaways = [
        "1. Highest Precision (1.0000): 1+1 Hybrid achieves perfect Top-10 relevant hits on test profiles by removing irrelevant lengths and targeting preferred genres.",
        "2. Resolves CBF Overspecialization: Boosts intra-list diversity from 0.1334 to 0.2017 (+51% increase) without losing relevance.",
        "3. Zero Data Leakage: Evaluated objectively against holdout test interactions using our automated test suite."
    ]
    for t in takeaways:
        p = tf.add_paragraph()
        p.text = f"•  {t}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(4)

    # ==========================================================================
    # SLIDE 14: USER INTERFACE & DEMONSTRATION
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, prs)
    add_header(s14, "User Experience & UI", "Modern Interactive Platform Interface", "Designed with streaming-grade aesthetics for effortless decision making.")

    add_card(s14, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_INDIGO)
    tb = s14.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Smart Match Decision Center"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    ui_points1 = [
        "Interactive Sliders: Real-time control of maximum episode budgets (≤ 13, ≤ 26, ≤ 50 eps) and minimum rating thresholds.",
        "Mood & Genre Pills: One-click selection of viewing moods (Exciting, Chill, Dark, Emotional) and required/excluded genres.",
        "Instant Mathematical Scores: Displays both Taste Match % and Requirement Fit % alongside the combined Hybrid Score %."
    ]
    for up in ui_points1:
        p = tf.add_paragraph()
        p.text = f"•  {up}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # Right: Detail View & Discovery
    add_card(s14, Inches(6.883), top_y, col_w, card_h, border_color=ACCENT_AMBER)
    tb = s14.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Detail View & Discovery"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    ui_points2 = [
        "Rating Distribution Histogram: Interactive 1-to-5 star vote breakdown bars located directly inside the anime hero container.",
        "Netflix-Style Carousels: Reusable horizontal carousel rows for 'More Like This' and 'Recommended For You' with chevron navigation.",
        "3D Responsive Canvas: Dynamic background particle grid responding to mouse movements across all pages.",
        "Dark & Light Mode: Full theme toggle support with accessible color contrast."
    ]
    for up in ui_points2:
        p = tf.add_paragraph()
        p.text = f"•  {up}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # ==========================================================================
    # SLIDE 15: CLOUD DEPLOYMENT & OPEN SOURCE
    # ==========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, prs)
    add_header(s15, "Engineering & Deployment", "100% Free Cloud Architecture", "Publicly accessible worldwide with zero server hosting costs.")

    add_card(s15, Inches(0.8), top_y, col_w, card_h, border_color=ACCENT_INDIGO)
    tb = s15.shapes.add_textbox(Inches(1.1), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Hugging Face Spaces (Live App)"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    hf_bullets = [
        "Live Public URL:\n  https://minkhanttin-anivibe.static.hf.space",
        "100% Free Static Hosting: Deployed using Hugging Face Static SDK, requiring $0.00/month and no paid Docker instance.",
        "Zero Downtime & Global CDN: Accessible worldwide with instant load times on phones, iPads, and PCs.",
        "Client-Side Academic Engine: Computes all 4 recommendation algorithms in JavaScript in < 3 ms directly in the browser."
    ]
    for h in hf_bullets:
        p = tf.add_paragraph()
        p.text = f"•  {h}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # Right: GitHub Open Source
    add_card(s15, Inches(6.883), top_y, col_w, card_h, border_color=ACCENT_PURPLE)
    tb = s15.shapes.add_textbox(Inches(7.183), top_y + Inches(0.35), col_w - Inches(0.6), card_h - Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "GitHub Open-Source Codebase"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    git_bullets = [
        "Official Repository:\n  https://github.com/manisandar/anime-dsrs",
        "Core Python Algorithms: Complete implementations in recommender/algorithms.py and pipeline.py.",
        "Reproducible Benchmarks: Anyone can run 'python3 recommender/evaluate.py' to verify the benchmark metrics.",
        "Clean Academic Formatting: Well-documented codebase ready for university examination and code inspection."
    ]
    for g in git_bullets:
        p = tf.add_paragraph()
        p.text = f"•  {g}"
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    # ==========================================================================
    # SLIDE 16: CONCLUSION & Q&A
    # ==========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16, prs)

    add_card(s16, Inches(1.2), Inches(1.1), Inches(10.933), Inches(5.3), border_color=ACCENT_INDIGO)
    tb = s16.shapes.add_textbox(Inches(1.8), Inches(1.5), Inches(9.733), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "PROJECT SUMMARY & CONCLUSION"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "Thank You!"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(16)

    conclusion_points = [
        "1. Complete Paradigm Implementation: Successfully built and compared Popularity, Content-Based, Knowledge-Based, and 1+1 Hybrid systems.",
        "2. Superior Hybrid Performance: Reached 1.0000 Precision@10 while increasing intra-list diversity by +51% over pure Content-Based filtering.",
        "3. User Empowerment: Transparent explainable AI rules remove black-box confusion and solve the streaming paradox of choice.",
        "4. Production Ready: Live public deployment with zero cloud hosting costs."
    ]
    for cp in conclusion_points:
        p = tf.add_paragraph()
        p.text = cp
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "\nQuestions & Live Demonstration Discussion"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    # Save presentation
    output_path = os.path.join(os.path.dirname(__file__), "..", "ANIVIBE_Presentation.pptx")
    prs.save(output_path)
    print(f"✅ Enhanced presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    main()
