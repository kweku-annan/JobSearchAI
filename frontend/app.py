#!/usr/bin/env python
"""JobInsightAI — Streamlit app entry-point.

Run with:
    streamlit run frontend/app.py

The frontend is kept intentionally separate from the Flask app (app.py).
It reuses backend logic directly by importing from the existing packages.
"""
import sys
import os

# Ensure the project root is on sys.path so backend packages resolve
# correctly regardless of where `streamlit run` is invoked from.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import streamlit as st

from frontend.state import init_state
from frontend.styles import inject_styles
from frontend.components.sidebar import render_sidebar
from frontend.views.home import render_home
from frontend.views.about import render_about


def main() -> None:
    # ── Page config (must be first Streamlit call) ──
    st.set_page_config(
        page_title="JobInsightAI",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # ── Inject global CSS ───────────────────────────
    inject_styles()

    # ── Session state ───────────────────────────────
    init_state()

    # ── Sidebar / navigation ────────────────────────
    page = render_sidebar()

    # ── Page routing ────────────────────────────────
    if page == "Home":
        render_home()
    elif page == "About":
        render_about()
    else:
        render_home()


if __name__ == "__main__":
    main()
