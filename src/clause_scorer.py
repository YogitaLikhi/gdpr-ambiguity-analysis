import re

def is_user_permission(paragraph):
    text = paragraph.lower()
    return bool(re.search(r"\byou\s+may\s+", text))

def compute_clause_score(modal_count, vague_count):
    return modal_count + (2 * vague_count)