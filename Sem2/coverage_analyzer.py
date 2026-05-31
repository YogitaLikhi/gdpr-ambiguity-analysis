from src.specificity_detector import (
    mentions_purpose,
    mentions_retention,
    mentions_data_category,
    mentions_access_rights,
    EXPLICIT_PURPOSE_KEYWORDS,
    VAGUE_PURPOSE_KEYWORDS,
    EXPLICIT_DATA_CATEGORY_KEYWORDS,
    VAGUE_DATA_CATEGORY_KEYWORDS,
    EXPLICIT_ACCESS_KEYWORDS,
    VAGUE_ACCESS_KEYWORDS,
    RETENTION_VAGUE_PHRASES,
    RETENTION_NUMERIC_PATTERN
)

STATUS_PRIORITY = {
    "missing": 0,
    "vague": 1,
    "explicit": 2
}

def calculate_match_score(category, text):

    text = text.lower()

    score = 0

    if category == "purpose":

        for phrase in EXPLICIT_PURPOSE_KEYWORDS:
            if phrase in text:
                score += 2

        for phrase in VAGUE_PURPOSE_KEYWORDS:
            if phrase in text:
                score += 1

    elif category == "retention":

        if RETENTION_NUMERIC_PATTERN.search(text):
            score += 5

        for phrase in RETENTION_VAGUE_PHRASES:
            if phrase in text:
                score += 1

    elif category == "data_categories":

        for phrase in EXPLICIT_DATA_CATEGORY_KEYWORDS:
            if phrase in text:
                score += 2

        for phrase in VAGUE_DATA_CATEGORY_KEYWORDS:
            if phrase in text:
                score += 1

    elif category == "access_rights":

        for phrase in EXPLICIT_ACCESS_KEYWORDS:
            if phrase in text:
                score += 2

        for phrase in VAGUE_ACCESS_KEYWORDS:
            if phrase in text:
                score += 1

    return score

def analyze_policy_coverage(all_clauses):

    coverage = {
        "purpose": {
            "status": "missing",
            "score": 0,
            "evidence": None,
            "source_paragraph": None
        },

        "retention": {
            "status": "missing",
            "score": 0,
            "evidence": None,
            "source_paragraph": None
        },

        "data_categories": {
            "status": "missing",
            "score": 0,
            "evidence": None,
            "source_paragraph": None
        },

        "access_rights": {
            "status": "missing",
            "score": 0,
            "evidence": None,
            "source_paragraph": None
        }
    }

    detectors = {
        "purpose": mentions_purpose,
        "retention": mentions_retention,
        "data_categories": mentions_data_category,
        "access_rights": mentions_access_rights
    }

    for clause in all_clauses:

        clause_text = clause["text"]

        for category, detector in detectors.items():

            found, status = detector(clause_text)

            if not found:
                continue
    
            current_status = coverage[category]["status"]
            current_score = coverage[category]["score"]

            new_score = calculate_match_score(
                category,
                clause_text
            )

            if (STATUS_PRIORITY[status] > STATUS_PRIORITY[current_status]):

                coverage[category] = {
                    "status": status,
                    "score": new_score,
                    "evidence": clause_text,
                    "source_paragraph":clause["paragraph_text"]
            }

            elif (STATUS_PRIORITY[status]==STATUS_PRIORITY[current_status] and new_score > current_score):

                coverage[category] = {
                    "status": status,
                    "score": new_score,
                    "evidence": clause_text,
                    "source_paragraph": clause["paragraph_text"]
                }
            
    for category in coverage:

        coverage[category].pop(
            "score",
            None
        )

    return coverage