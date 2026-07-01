#!/usr/bin/env python
"""Chat bubble component.

Usage:
    from frontend.components.chat_bubble import render_bubble
    render_bubble("user", "Find me python developer jobs")
    render_bubble("assistant", "Here are the results...")
"""
import streamlit as st


def render_bubble(role: str, content: str) -> None:
    """Render a single chat message as a styled HTML bubble.

    Args:
        role: "user" or "assistant"
        content: The text content of the message
    """
    css_class = "bubble-user" if role == "user" else "bubble-assistant"
    wrapper_class = "user" if role == "user" else "assistant"

    # Escape HTML entities to prevent injection
    safe_content = (
        content
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br>")
    )

    label = "You" if role == "user" else "🤖 JobInsightAI"

    html = f"""
    <div class="bubble-wrapper {wrapper_class}">
        <div>
            <div style="font-size:0.72rem; color:#9090B0; margin-bottom:3px;
                        {'text-align:right;' if role == 'user' else ''}">
                {label}
            </div>
            <div class="{css_class}">{safe_content}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
