#!/usr/bin/env python
"""Takes messy user input and extracts a clean job title to search with"""
import re


def extract_job_title(user_input):
    """
    Extracts a job title from user input.
    Optimized for tech job queries.

    Args:
        user_input: Raw user message

    Returns:
        Cleaned job title string or None if invalid
    """
    if not user_input or not isinstance(user_input, str):
        return None

    message = user_input.lower().strip()

    # If message is very short and looks like a direct job title, return it
    if len(message.split()) <= 3 and not any(word in message for word in
                                             ['find', 'looking', 'want', 'search', 'show', 'get', 'any', 'do you',
                                              'can you']):
        # Clean and return
        title = _clean_title(message)
        return title if title and len(title) >= 2 else None

    # Patterns ordered from most specific to least specific
    patterns = [
        # "looking for X jobs/positions/roles"
        r"looking for (?:a |an |some )?(.+?)(?:\s+(?:jobs?|positions?|roles?|openings?|opportunities?))?$",

        # "find me X" / "find X"
        r"find(?:\s+me)?\s+(?:a |an |some )?(.+?)(?:\s+(?:jobs?|positions?|roles?|openings?|opportunities?))?$",

        # "I want/need X"
        r"i (?:want|need)\s+(?:a |an |some )?(.+?)(?:\s+(?:jobs?|positions?|roles?|openings?|opportunities?))?$",

        # "search for X" / "searching for X"
        r"search(?:ing)? for\s+(?:a |an |some )?(.+?)(?:\s+(?:jobs?|positions?|roles?|openings?|opportunities?))?$",

        # "show me X" / "get me X"
        r"(?:show|get)\s+me\s+(?:a |an |some )?(.+?)(?:\s+(?:jobs?|positions?|roles?|openings?|opportunities?))?$",

        # "What X are there/available"
        r"what\s+(.+?)\s+(?:are there|are available|do you have|jobs?|positions?|roles?)(?:\s+available)?",

        # "Any X available/jobs"
        r"any\s+(.+?)\s+(?:available|jobs?|positions?|roles?|openings?)",

        # "Do you have X"
        r"do you have\s+(?:any\s+)?(.+?)(?:\s+(?:jobs?|positions?|roles?|openings?|opportunities?))?$",

        # "Can you find X"
        r"can you find\s+(?:me\s+)?(?:any\s+)?(.+?)(?:\s+(?:jobs?|positions?|roles?|openings?|opportunities?))?$",

        # Just "X jobs/positions/roles" at the end
        r"^(.+?)\s+(?:jobs?|positions?|roles?|openings?|opportunities?)$",

        # Anything with "developer/engineer/programmer" etc (tech-specific)
        r"(.*?(?:developer|engineer|programmer|architect|designer|analyst|scientist|manager|lead|devops|sre|admin|specialist|consultant).*?)(?:\s+(?:jobs?|positions?|roles?|openings?|opportunities?))?$",
    ]

    title = None

    # Try each pattern
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            if title:  # Make sure we got something
                break

    # If no pattern matched, use the entire message as fallback
    if not title:
        title = message

    # Clean the extracted title
    title = _clean_title(title)

    # Validate
    if not title or len(title) < 2:
        return None

    return title


def _clean_title(title):
    """
    Clean extracted job title by removing filler words and normalizing

    Args:
        title: Raw extracted title

    Returns:
        Cleaned title string
    """
    # Remove common filler/question words
    fillers = [
        r"\b(?:a|an|the|some|any)\b",
        r"\b(?:jobs?|positions?|roles?|openings?|opportunities?)\b",
        r"\b(?:available|there)\b",
        r"\b(?:please|thanks?|thank you)\b",
    ]

    for filler in fillers:
        title = re.sub(filler, " ", title, flags=re.IGNORECASE)

    # Clean up punctuation and extra spaces
    title = re.sub(r"[?!.,:;]", "", title)
    title = re.sub(r"\s+", " ", title).strip()

    return title