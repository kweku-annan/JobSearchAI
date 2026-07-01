#!/usr/bin/env python
"""Home / Chat view — the main search interface.

Renders the chat history, accepts user input, calls the agent,
and renders structured job cards + recommendation cards.
"""
import re
import streamlit as st
from typing import List, Dict, Optional, Tuple

from agent.handler import process_message
from frontend.state import append_message
from frontend.components.chat_bubble import render_bubble
from frontend.components.job_card import render_job_card
from frontend.components.recommendation_card import render_recommendation_card


# ─────────────────────────────────────────────────────────────
# Response parser
# ─────────────────────────────────────────────────────────────

def _parse_agent_response(response: str) -> Tuple[List[Dict], Optional[List[Dict]], str]:
    """Parse the plain-text agent response into structured data.

    The agent formats responses as:
        Here is a list of jobs for 'X':
        1. Job Title @ Company - Location - [Apply Here](url)
           Description: ...

        Portfolio Project Recommendations
        Based on: ...
        1.  Project Title
           • description text
           • Stack: tech1, tech2
           • Demonstrates: ...
           • Time: ...

    Returns:
        jobs: list of job dicts
        recommendations: list of rec dicts, or None if absent
        intro: the opening sentence (for the bubble)
    """
    jobs: List[Dict] = []
    recs: List[Dict] = []

    lines = response.splitlines()
    intro = lines[0].strip() if lines else response

    mode = "jobs"  # "jobs" | "recs"
    current_job: Optional[Dict] = None
    current_rec: Optional[Dict] = None

    for line in lines[1:]:
        stripped = line.strip()

        # ── Detect section change ───────────────────────
        if "Portfolio Project Recommendations" in stripped:
            if current_job:
                jobs.append(current_job)
                current_job = None
            mode = "recs"
            continue

        if stripped.startswith("Based on:"):
            continue  # skip the "Based on: …" line

        # ── Jobs section ────────────────────────────────
        if mode == "jobs":
            # Match: "1. Job Title @ Company - Location - [Apply Here](url)"
            job_line = re.match(
                r"^\d+\.\s+(.+?)\s+@\s+(.+?)\s+-\s+(.+?)\s+-\s*(?:\[.+?\]\((.+?)\))?",
                stripped,
            )
            if job_line:
                if current_job:
                    jobs.append(current_job)
                title, company, location, url = (
                    job_line.group(1),
                    job_line.group(2),
                    job_line.group(3),
                    job_line.group(4) or "",
                )
                current_job = {
                    "job_title": title,
                    "company_name": company,
                    "location": location,
                    "job_url": url,
                    "job_description": "",
                    "is_remote": False,
                    "date_posted": "",
                }
                continue

            desc_match = re.match(r"^Description:\s*(.+)", stripped)
            if desc_match and current_job is not None:
                current_job["job_description"] = desc_match.group(1)
                continue

        # ── Recommendations section ──────────────────────
        if mode == "recs":
            # Match: "1.  Project Title"
            rec_header = re.match(r"^\d+\.\s+(.+)", stripped)
            if rec_header and not stripped.startswith("•"):
                if current_rec:
                    recs.append(current_rec)
                current_rec = {
                    "title": rec_header.group(1).strip(),
                    "description": "",
                    "technologies": [],
                    "demonstrates": "",
                    "timeline": "",
                    "standout_factor": "",
                }
                continue

            if stripped.startswith("•") and current_rec is not None:
                content = stripped.lstrip("•").strip()
                if content.startswith("Stack:"):
                    tech_str = content[len("Stack:"):].strip()
                    current_rec["technologies"] = [t.strip() for t in tech_str.split(",") if t.strip()]
                elif content.startswith("Demonstrates:"):
                    current_rec["demonstrates"] = content[len("Demonstrates:"):].strip()
                elif content.startswith("Time:"):
                    current_rec["timeline"] = content[len("Time:"):].strip()
                else:
                    # description bullet
                    if current_rec["description"]:
                        current_rec["description"] += " " + content
                    else:
                        current_rec["description"] = content
                continue

    # Flush last items
    if current_job:
        jobs.append(current_job)
    if current_rec:
        recs.append(current_rec)

    return jobs, recs if recs else None, intro


# ─────────────────────────────────────────────────────────────
# Structured result renderer
# ─────────────────────────────────────────────────────────────

def _render_structured_response(response: str) -> None:
    """Parse agent text and render it as styled cards + intro bubble."""
    jobs, recommendations, intro = _parse_agent_response(response)

    # Always show the intro line as a bubble
    render_bubble("assistant", intro)

    if not jobs:
        # No structure found — fall back to plain text bubble
        fallback = "\n".join(response.splitlines()[1:]).strip()
        if fallback:
            render_bubble("assistant", fallback)
        return

    # ── Job listings ──────────────────────────────────
    st.markdown(
        "<div class='section-header'>📋 Job Listings</div>",
        unsafe_allow_html=True,
    )
    for i, job in enumerate(jobs, 1):
        render_job_card(job, index=i)

    # ── Portfolio recommendations ─────────────────────
    if recommendations:
        st.markdown(
            "<div class='section-header'>💼 Portfolio Project Recommendations</div>",
            unsafe_allow_html=True,
        )
        for i, rec in enumerate(recommendations, 1):
            render_recommendation_card(rec, index=i)
    else:
        st.markdown(
            "<div style='color:#9090B0; font-size:0.85rem; margin-top:8px;'>"
            "ℹ️ No portfolio recommendations available for this query.</div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────
# View entry-point
# ─────────────────────────────────────────────────────────────

def render_home() -> None:
    """Render the main chat / search page."""

    st.markdown(
        "<h2 style='margin-bottom:4px;'>🔍 Job Search</h2>"
        "<p style='color:#9090B0; font-size:0.9rem; margin-top:0;'>"
        "Tell me what job you're looking for — I'll find listings and suggest portfolio projects.</p>",
        unsafe_allow_html=True,
    )

    # ── Render chat history ───────────────────────────
    messages: List[Dict] = st.session_state.get("messages", [])

    for msg in messages:
        role    = msg["role"]
        content = msg["content"]

        if role == "user":
            render_bubble("user", content)
        else:
            # Assistant messages already rendered as structured output
            # Re-render as structured on re-run
            _render_structured_response(content)

    # ── Chat input ────────────────────────────────────
    user_input = st.chat_input("e.g. python developer, backend engineer…")

    if user_input:
        user_input = user_input.strip()
        if not user_input:
            return

        # Add user message to state + render immediately
        append_message("user", user_input)
        render_bubble("user", user_input)

        # Call agent with a spinner
        with st.spinner("Searching jobs and generating recommendations…"):
            try:
                response = process_message(user_input)
            except Exception as exc:
                response = f"❌ Something went wrong: {exc}"

        # Store response and render it
        append_message("assistant", response)
        _render_structured_response(response)
