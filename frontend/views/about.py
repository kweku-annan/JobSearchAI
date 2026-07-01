#!/usr/bin/env python
"""About page view — static information about JobInsightAI."""
import streamlit as st


def render_about() -> None:
    """Render the About page."""

    st.markdown(
        "<h2 style='margin-bottom:4px;'>ℹ️ About JobInsightAI</h2>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="color:#9090B0; font-size:0.9rem; margin-bottom:24px;">
        An AI-powered job search and portfolio advisor built for the HNG Internship.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── What it does ─────────────────────────────────
    with st.expander("🤖 What does it do?", expanded=True):
        st.markdown(
            """
            **JobInsightAI** combines real-time job discovery with AI-powered career advice:

            1. **Job Search** — Searches multiple remote job boards (Remotive, RemoteOK, Jobicy, Arbeitnow)
               and caches results locally for fast retrieval.
            2. **Portfolio Recommendations** — Uses an LLM to analyse a matching job and suggest
               3 tailored portfolio projects that would impress hiring managers for that specific role.
            3. **Smart Matching** — Understands natural language queries like *"looking for a senior backend
               engineer"* and extracts the relevant job title automatically.
            """
        )

    # ── How to use ───────────────────────────────────
    with st.expander("💬 How to use"):
        st.markdown(
            """
            Simply type your job search query in the chat input at the bottom of the **Home** page.

            **Example queries:**
            - `python developer`
            - `find me machine learning engineer jobs`
            - `I'm looking for a backend engineer role`
            - `show me devops positions`
            - `data analyst`

            The app will return matching job listings along with AI-generated portfolio project ideas
            tailored to the first matching role.
            """
        )

    # ── Tech stack ───────────────────────────────────
    with st.expander("🛠️ Tech Stack"):
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**Backend**")
            st.markdown(
                """
                - Python 3.12
                - Flask (A2A / Telex integration)
                - SQLAlchemy + SQLite (job cache)
                - OpenAI API via OpenRouter (LLM)
                - FuzzyWuzzy (fuzzy job-title matching)
                """
            )
        with cols[1]:
            st.markdown("**Frontend**")
            st.markdown(
                """
                - Streamlit
                - Custom CSS (dark theme, glassmorphism cards)
                - Google Fonts (Inter)
                """
            )

        st.markdown("**Data Sources**")
        st.markdown(
            """
            | Priority | Source | Type |
            |----------|--------|------|
            | 1st | Remotive | Remote jobs API |
            | 2nd | RemoteOK | Remote jobs API |
            | 3rd | Jobicy   | Remote jobs API |
            | 4th | Arbeitnow | Job board API  |
            """
        )

    # ── Cache behaviour ──────────────────────────────
    with st.expander("🗄️ Cache Behaviour"):
        st.markdown(
            """
            Jobs are fetched from external APIs and stored in a local SQLite database
            (`cache_job_data.db`). The cache is refreshed automatically every **24 hours**
            to keep listings fresh without hammering external APIs on every request.
            """
        )

    # ── Footer ───────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; margin-top:40px; color:#9090B0; font-size:0.8rem;">
            Built with ❤️ for the HNG Internship · 2026
        </div>
        """,
        unsafe_allow_html=True,
    )
