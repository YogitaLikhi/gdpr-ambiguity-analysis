import re

def extract_clauses(text):

    """
    Splits policy text into clauses using sentence boundaries.
    Returns a list of cleaned clauses.
    """

    # Split on sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)

    clauses = []
    for sentence in sentences:
        cleaned = sentence.strip()
        if cleaned:
            clauses.append(cleaned)

    return clauses


def load_policy(file_path):  
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


"""
re.split(r'(?<=[.!?])\s+', text) = Split the text at whitespace that comes immediately after ., !, or ?
with open(file_path, 'r', encoding='utf-8') as f: = Opens a UTF-8 encoded text file, reads its entire contents into a string, and safely closes the file.
"""