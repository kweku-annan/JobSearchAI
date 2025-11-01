#!/usr/bin/env python
"""Parse texts"""

from bs4 import BeautifulSoup


def html_to_text(html_content):
    """Convert HTML content to plain text"""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text().strip()