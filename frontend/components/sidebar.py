#!/usr/bin/env python
"""Sidebar component — branding, navigation, and query tips.

Usage:
    from frontend.components.sidebar import render_sidebar
    page = render_sidebar()   # returns the selected page name
"""
import streamlit as st
from frontend.state import clear_history


def render_sidebar() -> str:
    """Render the sidebar and return the currently selected page.

    Returns:
        The page name selected by the user ("Home" or "About").
    """
    with st.sidebar:
        # ── Brand ──────────────────────────────────────
        st.markdown(
            """
            <div style="text-align:center; padding: 12px 0 20px;">
                <div style="font-size:2.6rem;">🔍</div>
                <div style="font-size:1.3rem; font-weight:700;
                            background:linear-gradient(135deg,#6C63FF,#4B44CC);
                            -webkit-background-clip:text;
                            -webkit-text-fill-color:transparent;">
                    JobInsightAI
                </div>
                <div style="font-size:0.78rem; color:#9090B0; margin-top:4px;">
                    AI-powered job search &amp; portfolio advisor
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Navigation ─────────────────────────────────
        pages = ["🏠 Home", "ℹ️ About"]
        selected = st.radio(
            "Navigation",
            pages,
            label_visibility="collapsed",
            key="nav_radio",
        )

        st.divider()

        # ── Query tips ─────────────────────────────────
        st.markdown(
            "<div style='font-size:0.85rem; font-weight:600; color:#9090B0;'>"
            "💬 Try asking…</div>",
            unsafe_allow_html=True,
        )
        tips = [
            "python developer",
            "backend engineer",
            "data analyst",
            "devops engineer",
            "machine learning engineer",
        ]
        for tip in tips:
            st.markdown(
                f"<div style='font-size:0.82rem; color:#6C63FF; "
                f"padding:3px 0;'>→ {tip}</div>",
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Clear history button ────────────────────────
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_history()
            st.rerun()

        # ── Footer ─────────────────────────────────────
        st.markdown(
            "<div style='font-size:0.72rem; color:#9090B0; text-align:center;"
            "margin-top:20px;'>v1.0 · HNG Internship</div>",
            unsafe_allow_html=True,
        )

    # Strip the emoji prefix from the selected page label
    return selected.split(" ", 1)[1] if " " in selected else selected
