import pickle
import numpy as np
import joblib
import json
import os

from scipy.sparse import hstack

from src.paragraph_segmenter import segment_into_paragraphs

from Sem2.dataset.sentence_extractor import extract_sentences

from src.ambiguity_detector import (
    detect_modal_verbs,
    detect_vague_phrases,
    load_vague_phrases
)

from src.clause_scorer import compute_clause_score

from Sem2.coverage_analyzer import (
    analyze_policy_coverage
)


# =========================
# LOAD TRAINED ARTIFACTS
# =========================

svm_model = joblib.load(
    "Sem2/models/svm_model.pkl"
)

tfidf = joblib.load(
    "Sem2/models/tfidf_vectorizer.pkl"
)


vague_phrases = load_vague_phrases()


# =========================
# RULE FEATURE EXTRACTION
# =========================

def build_rule_features(text):

    modal_count = len(
        detect_modal_verbs(text)
    )

    vague_result = detect_vague_phrases(
        text,
        vague_phrases
    )

    vague_count = vague_result["count"]

    ambiguity_score = compute_clause_score(
        modal_count,
        vague_count
    )

    clause_length = len(
        text.split()
    )

    return np.array([[
        modal_count,
        vague_count,
        ambiguity_score,
        clause_length
    ]])


# =========================
# SINGLE CLAUSE PREDICTION
# =========================

def predict_clause(clause):

    tfidf_features = tfidf.transform(
        [clause]
    )

    rule_features = build_rule_features(
        clause
    )

    features = hstack([
        tfidf_features,
        rule_features
    ])

    score = svm_model.decision_function(features)[0]
    prediction = 1 if score >= 0.5 else 0
    confidence = abs(score)

    return {
        "text": clause,
        "prediction": prediction,
        "confidence": round(confidence, 3),
        "modal_verbs": detect_modal_verbs(clause),
        "vague_phrases":
            detect_vague_phrases(
                clause,
                vague_phrases
            )["phrases"]
    }


# =========================
# POLICY ANALYSIS
# =========================

def analyze_policy(policy_text):

    paragraphs = segment_into_paragraphs(
        policy_text
    )

    paragraph_results = []
    all_clauses = []

    ambiguous_clause_count = 0
    total_clause_count = 0

    for paragraph_id, paragraph in enumerate(
        paragraphs,
        start=1
    ):

        clauses = extract_sentences(
            paragraph
        )

        clause_results = []

        paragraph_ambiguous = False

        for clause in clauses:

            all_clauses.append({
                "text": clause,
                "paragraph_text": paragraph
            })

            result = predict_clause(
                clause
            )

            clause_results.append(
                result
            )

            total_clause_count += 1

            if result["prediction"] == 1:

                paragraph_ambiguous = True
                ambiguous_clause_count += 1
        
        coverage_results = analyze_policy_coverage(
            all_clauses
        )

        paragraph_results.append({
            "paragraph_id": paragraph_id,
            "paragraph_text": paragraph,
            "paragraph_ambiguous": paragraph_ambiguous,
            "clauses": clause_results
        })

    return {

        "policy_summary": {
            "total_paragraphs": len(paragraphs),
            "total_clauses": total_clause_count,
            "ambiguous_clauses": ambiguous_clause_count,
            "ambiguity_ratio": round(
                ambiguous_clause_count /
                total_clause_count,
                2
            ) if total_clause_count else 0
        },

        "policy_coverage":
            coverage_results,

        "paragraph_analysis":
            paragraph_results
    }

def save_analysis_to_json(result):

    os.makedirs(
        "output",
        exist_ok=True
    )

    with open(
        "output/analysis_result.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        "\nAnalysis saved to output/analysis_result_svm.json"
    )


if __name__ == "__main__":

    with open(
        "data/weverse_policy.txt",
        "r",
        encoding="utf-8"
    ) as f:

        policy_text = f.read()

    result = analyze_policy(
        policy_text
    )

    save_analysis_to_json(
        result
    )