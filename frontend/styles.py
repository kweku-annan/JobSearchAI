#!/usr/bin/env python
"""Global CSS theming for the JobSearchAI Streamlit app.

Call `inject_styles()` once from the main app entry-point.
All visual tokens (colours, radius, typography, etc.) live here.
"""
import streamlit as st

# ──────────────────────────────────────────────
# Design tokens
# ──────────────────────────────────────────────
ACCENT      = "#6C63FF"       # purple-ish primary
ACCENT_DARK = "#4B44CC"
BG_DARK     = "#0F0F1A"
CARD_BG     = "#1A1A2E"
CARD_BORDER = "#2D2D4E"
USER_BUBBLE = "#6C63FF"
BOT_BUBBLE  = "#1E1E35"
TEXT_MAIN   = "#E8E8F0"
TEXT_MUTED  = "#9090B0"
TAG_BG      = "#2A2A45"

CSS = f"""
<style>
/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {{
    background: {BG_DARK} !important;
    color: {TEXT_MAIN};
    font-family: 'Inter', 'Segoe UI', sans-serif;
}}

/* Remove default Streamlit padding on main block */
[data-testid="block-container"] {{
    padding-top: 1.5rem !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {CARD_BG} !important;
    border-right: 1px solid {CARD_BORDER};
}}

[data-testid="stSidebar"] * {{
    color: {TEXT_MAIN} !important;
}}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {{
    background: {CARD_BG} !important;
    border: 1px solid {CARD_BORDER} !important;
    color: {TEXT_MAIN} !important;
    border-radius: 12px !important;
}}

[data-testid="stChatInput"] textarea:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 2px {ACCENT}33 !important;
}}

/* ── Chat bubbles ── */
.bubble-user {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT_DARK});
    color: #fff;
    padding: 10px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 4px 0 4px auto;
    max-width: 75%;
    word-wrap: break-word;
    font-size: 0.95rem;
    line-height: 1.5;
    box-shadow: 0 4px 15px {ACCENT}44;
}}

.bubble-assistant {{
    background: {BOT_BUBBLE};
    color: {TEXT_MAIN};
    padding: 10px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 4px auto 4px 0;
    max-width: 75%;
    word-wrap: break-word;
    font-size: 0.95rem;
    line-height: 1.5;
    border: 1px solid {CARD_BORDER};
}}

.bubble-wrapper {{
    display: flex;
    margin-bottom: 8px;
}}

.bubble-wrapper.user  {{ justify-content: flex-end;  }}
.bubble-wrapper.assistant {{ justify-content: flex-start; }}

/* ── Job card ── */
.job-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
    transition: border-color 0.2s, transform 0.15s;
}}
.job-card:hover {{
    border-color: {ACCENT};
    transform: translateY(-2px);
    box-shadow: 0 8px 24px {ACCENT}22;
}}
.job-card .job-title {{
    font-size: 1.05rem;
    font-weight: 700;
    color: {TEXT_MAIN};
    margin-bottom: 4px;
}}
.job-card .job-company {{
    font-size: 0.88rem;
    color: {TEXT_MUTED};
    margin-bottom: 8px;
}}
.job-card .job-tag {{
    display: inline-block;
    background: {TAG_BG};
    color: {ACCENT};
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.78rem;
    margin-right: 6px;
    margin-bottom: 6px;
}}
.job-card .job-desc {{
    font-size: 0.86rem;
    color: {TEXT_MUTED};
    margin-top: 8px;
    line-height: 1.55;
}}
.job-card .apply-btn {{
    display: inline-block;
    margin-top: 10px;
    background: linear-gradient(135deg, {ACCENT}, {ACCENT_DARK});
    color: #fff !important;
    text-decoration: none !important;
    padding: 6px 18px;
    border-radius: 8px;
    font-size: 0.84rem;
    font-weight: 600;
    transition: opacity 0.2s;
}}
.job-card .apply-btn:hover {{ opacity: 0.85; }}

/* ── Recommendation card ── */
.rec-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-left: 3px solid {ACCENT};
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 12px;
}}
.rec-card .rec-title {{
    font-size: 1rem;
    font-weight: 700;
    color: {TEXT_MAIN};
    margin-bottom: 6px;
}}
.rec-card .rec-body {{
    font-size: 0.86rem;
    color: {TEXT_MUTED};
    line-height: 1.55;
}}
.rec-card .rec-stack {{
    margin-top: 8px;
    font-size: 0.82rem;
    color: {ACCENT};
}}
.rec-card .rec-meta {{
    margin-top: 4px;
    font-size: 0.82rem;
    color: {TEXT_MUTED};
}}

/* ── Section headers ── */
.section-header {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {TEXT_MAIN};
    margin: 20px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid {CARD_BORDER};
}}

/* ── Spinner override ── */
.stSpinner > div {{ border-top-color: {ACCENT} !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: {BG_DARK}; }}
::-webkit-scrollbar-thumb {{ background: {CARD_BORDER}; border-radius: 4px; }}
</style>
"""


def inject_styles() -> None:
    """Inject global CSS into the Streamlit app."""
    st.markdown(CSS, unsafe_allow_html=True)
    # Also pull in Inter font from Google Fonts
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True
    )
