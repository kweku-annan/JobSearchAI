#!/usr/bin/env python
"""Job listing card component.

Usage:
    from frontend.components.job_card import render_job_card
    render_job_card(job_dict, index=1)
"""
import streamlit as st
from typing import Dict


def render_job_card(job: Dict, index: int = 0) -> None:
    """Render a single job listing as a styled card.

    Args:
        job: Dictionary with keys: job_title, company_name, location,
             job_url, job_description, is_remote, date_posted
        index: 1-based position in the result list (for numbering)
    """
    title       = job.get("job_title", "Unknown Title").title()
    company     = job.get("company_name") or "Company not listed"
    location    = job.get("location") or "Location not specified"
    job_url     = job.get("job_url", "")
    description = job.get("job_description", "No description available.")
    is_remote   = job.get("is_remote", False)
    date_posted = job.get("date_posted") or ""

    # Truncate description
    if len(description) > 200:
        description = description[:200].rsplit(" ", 1)[0] + "…"

    # Escape HTML
    def esc(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    tags_html = ""
    if is_remote in (True, "True", "true", 1):
        tags_html += '<span class="job-tag">🌐 Remote</span>'
    if date_posted:
        tags_html += f'<span class="job-tag">📅 {esc(date_posted)}</span>'

    apply_html = ""
    if job_url:
        apply_html = (
            f'<a class="apply-btn" href="{esc(job_url)}" target="_blank" '
            f'rel="noopener noreferrer">Apply Now →</a>'
        )

    html = f"""
    <div class="job-card">
        <div class="job-title">#{index} &nbsp; {esc(title)}</div>
        <div class="job-company">🏢 {esc(company)} &nbsp;·&nbsp; 📍 {esc(location)}</div>
        {tags_html}
        <div class="job-desc">{esc(description)}</div>
        {apply_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
