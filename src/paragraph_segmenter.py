import re

def segment_into_paragraphs(policy_text, min_length=40):

    # Normalize line endings
    text = policy_text.replace("\r\n", "\n").replace("\r", "\n")

    # Split on one or more blank lines
    raw_paragraphs = re.split(r"\n\s*\n+", text)

    paragraphs = []
    for para in raw_paragraphs:
        cleaned = para.strip()

        # Remove very short / noisy fragments
        if len(cleaned) >= min_length:
            paragraphs.append(cleaned)

    return paragraphs

"""
Splits policy text into paragraph-level blocks.
    
    Args:
        policy_text (str): Full policy text
        min_length (int): Minimum character length to keep a paragraph
    
    Returns:
        List[str]: Cleaned paragraph blocks
"""