#!/usr/bin/env python
"""Portfolio recommendation card component.

Usage:
    from frontend.components.recommendation_card import render_recommendation_card
    render_recommendation_card(rec_dict, index=1)
"""
import streamlit as st
from typing import Dict, List


def render_recommendation_card(rec: Dict, index: int = 0) -> None:
    """Render a single portfolio project recommendation card.

    Args:
        rec: Dictionary with keys: title, description, technologies,
             demonstrates, timeline, standout_factor
        index: 1-based position
    """
    def esc(s: str) -> str:
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    title          = esc(rec.get("title", "Project Idea"))
    description    = esc(rec.get("description", ""))
    technologies   = rec.get("technologies", [])
    demonstrates   = esc(rec.get("demonstrates", ""))
    timeline       = esc(rec.get("timeline", ""))
    standout       = esc(rec.get("standout_factor", ""))

    tech_str = " · ".join(esc(t) for t in technologies) if technologies else ""

    html = f"""
    <div class="rec-card">
        <div class="rec-title">💡 #{index} &nbsp; {title}</div>
        <div class="rec-body">{description}</div>
        {"<div class='rec-stack'>🛠️ Stack: " + tech_str + "</div>" if tech_str else ""}
        {"<div class='rec-meta'>✅ Demonstrates: " + demonstrates + "</div>" if demonstrates else ""}
        {"<div class='rec-meta'>⏱️ Timeline: " + timeline + "</div>" if timeline else ""}
        {"<div class='rec-meta'>⭐ Why it stands out: " + standout + "</div>" if standout else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
