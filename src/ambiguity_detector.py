import re
import os

def load_vague_phrases(file_path=None):
    if file_path is None:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(BASE_DIR, "rules", "vague_phrases.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]


def detect_vague_phrases(clause, vague_phrases):
    clause_lower = clause.lower()
    found = []

    for phrase in vague_phrases:
        if phrase in clause_lower:
            found.append(phrase)

    return {
        "count": len(found),
        "phrases": found
    }
    

def detect_modal_verbs(clause):
    modal_verbs = ["may", "might", "could", "would", "can"]
    clause_lower = clause.lower()

    ambiguous_modals = []

    # Company-action ambiguity patterns
    patterns = [
    r"\bwe\s+(may\s+(?:collect|use|share|retain|process|store|disclose))",
    r"\bwe\s+(might\s+(?:collect|use|share|retain|process|store|disclose))",
    r"\bwe\s+(could\s+(?:collect|use|share|retain|process|store|disclose))",
    r"\b(may\s+be\s+(?:used|shared|stored|processed))"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, clause_lower)
        ambiguous_modals.extend(matches)

    return list(set(ambiguous_modals))


def has_duration(clause):
    pattern = r'\b\d+\s*(day|days|month|months|year|years)\b'
    return bool(re.search(pattern, clause.lower()))


def has_purpose(clause):
    purpose_markers = [
        "for the purpose of",
        "to provide",
        "to improve",
        "in order to",
        "to comply",
        "to process"
    ]
    clause_lower = clause.lower()
    return any(marker in clause_lower for marker in purpose_markers)


def has_recipient(clause):
    recipient_markers = [
        "third party",
        "partners",
        "vendors",
        "service providers",
        "affiliates"
    ]
    clause_lower = clause.lower()
    return any(marker in clause_lower for marker in recipient_markers)


def detect_missing_specificity(clause):
    missing = []

    if "retain" in clause.lower() and not has_duration(clause):
        missing.append("retention duration")

    if ("use" in clause.lower() or "process" in clause.lower()) and not has_purpose(clause):
        missing.append("purpose")

    if ("share" in clause.lower() or "disclose" in clause.lower()) and not has_recipient(clause):
        missing.append("recipient")

    return missing


"""
r'\b\d+\s*(day|days|month|months|year|years)\b' = Match a number followed by an optional space and a time unit (day/month/year in singular or plural), as a complete word.
"""