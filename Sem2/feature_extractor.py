import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack

from src.ambiguity_detector import (
    detect_modal_verbs,
    detect_vague_phrases,
    load_vague_phrases
)

from src.clause_scorer import compute_clause_score


def extract_rule_features(texts):

    vague_phrases = load_vague_phrases()

    features = []

    for text in texts:

        modal_count = len(detect_modal_verbs(text))

        vague_result = detect_vague_phrases(
            text,
            vague_phrases
        )

        vague_count = vague_result["count"]

        ambiguity_score = compute_clause_score(
            modal_count,
            vague_count
        )

        clause_length = len(text.split())

        features.append([
            modal_count,
            vague_count,
            ambiguity_score,
            clause_length
        ])

    return np.array(features)


def build_feature_matrix(texts):

    tfidf = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2
    )

    tfidf_features = tfidf.fit_transform(texts)

    rule_features = extract_rule_features(texts)

    combined_features = hstack([
        tfidf_features,
        rule_features
    ])

    return combined_features, tfidf