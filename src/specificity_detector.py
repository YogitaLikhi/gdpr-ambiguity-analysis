import re

EXPLICIT_PURPOSE_KEYWORDS = [
    "to provide",
    "to operate",
    "to improve",
    "to deliver",
    "to process",
    "to comply with",
    "for the purpose of",
    "so that we can",
    "in order to"
]

VAGUE_PURPOSE_KEYWORDS = [
    "for business purposes",
    "for internal purposes",
    "for operational reasons",
    "as necessary",
    "as required"
]

RETENTION_NUMERIC_PATTERN = re.compile(
    r"\b\d+\s*(day|days|month|months|year|years)\b",
    re.IGNORECASE
)

RETENTION_VAGUE_PHRASES = [
    "as long as necessary",
    "as long as required",
    "for as long as needed",
    "until no longer required",
    "as required by law"
]

WORD_NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "thirty": 30
}

EXPLICIT_DATA_CATEGORY_KEYWORDS = [
    "name",
    "email",
    "address",
    "phone number",
    "payment information",
    "credit card",
    "location data",
    "device information",
    "ip address",
    "cookies"
]

VAGUE_DATA_CATEGORY_KEYWORDS = [
    "personal information",
    "personal data",
    "information about you",
    "user information"
]

EXPLICIT_ACCESS_KEYWORDS = [
    "access your data",
    "request access",
    "download your data",
    "correct your data",
    "delete your data",
    "data subject rights",
    "right to access",
    "right to erasure"
]

VAGUE_ACCESS_KEYWORDS = [
    "contact us regarding your information",
    "manage your account",
    "control your information"
]

def mentions_purpose(text):
    for phrase in EXPLICIT_PURPOSE_KEYWORDS:
        if phrase in text:
            return True, "explicit"

    for phrase in VAGUE_PURPOSE_KEYWORDS:
        if phrase in text:
            return True, "vague"

    return False, None

def resolve_missing_purpose(
    paragraphs,
    similarity_matrix,
    index,
    top_k_similar
):

    for idx in top_k_similar:
        if mentions_purpose(paragraphs[idx]):
            return True
    return False

def mentions_retention(text):
    text_lower = text.lower()

    # Numeric duration
    if RETENTION_NUMERIC_PATTERN.search(text_lower):
        return True, "explicit"

    # Word-based duration
    for word, num in WORD_NUMBERS.items():
        if f"{word} day" in text_lower or f"{word} year" in text_lower:
            return True, "explicit"

    # Vague retention
    for phrase in RETENTION_VAGUE_PHRASES:
        if phrase in text_lower:
            return True, "vague"

    return False, None

def mentions_data_category(text):
    for term in EXPLICIT_DATA_CATEGORY_KEYWORDS:
        if term in text:
            return True, "explicit"

    for term in VAGUE_DATA_CATEGORY_KEYWORDS:
        if term in text:
            return True, "vague"

    return False, None

def mentions_access_rights(text):
    for phrase in EXPLICIT_ACCESS_KEYWORDS:
        if phrase in text:
            return True, "explicit"

    for phrase in VAGUE_ACCESS_KEYWORDS:
        if phrase in text:
            return True, "vague"

    return False, None


def is_customer_data_context(paragraph):
    
    keywords = [
        "personal information",
        "personal data",
        "customer",
        "user",
        "you",
        "account"
    ]

    text = paragraph.lower()
    return any(k in text for k in keywords)

"""
def resolve_missing_purpose = Returns True if purpose is resolved via semantic neighbors
"""