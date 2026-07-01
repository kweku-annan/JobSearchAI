#!/usr/bin/env python
"""Session state management for the JobSearchAI Streamlit app."""
import streamlit as st


def init_state() -> None:
    """Initialise required session-state keys on first run."""
    defaults = {
        "messages": [],       # List[{"role": str, "content": str}]
        "page": "Home",       # Current active page
        "is_loading": False,  # Whether an LLM call is in-flight
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def append_message(role: str, content: str) -> None:
    """Append a chat message to session history."""
    st.session_state.messages.append({"role": role, "content": content})


def clear_history() -> None:
    """Clear all chat history."""
    st.session_state.messages = []


def set_page(page: str) -> None:
    """Set the active page."""
    st.session_state.page = page
