from clause_extractor import load_policy
from paragraph_segmenter import segment_into_paragraphs
from semantic_similarity import compute_similarity_matrix, get_anchor_related_clauses
from specificity_detector import (
    mentions_purpose,
    mentions_retention,
    mentions_data_category,
    mentions_access_rights
)
from clause_scorer import compute_clause_score, is_user_permission
from ambiguity_detector import (
    detect_vague_phrases, 
    detect_modal_verbs, 
    load_vague_phrases,
)
from constants import ANCHORS
import json

def analyze_policy(policy_text: str) -> dict:
    vague_phrases = load_vague_phrases()

    paragraphs = segment_into_paragraphs(policy_text)

    similarity_matrix, vectorizer = compute_similarity_matrix(paragraphs)

    clause_results = []
    ambiguous_clause_count = 0

    for i, paragraph in enumerate(paragraphs):

        if is_user_permission(paragraph):
            ambiguous_modals = []
        else:
            ambiguous_modals = detect_modal_verbs(paragraph)

        vague_result = detect_vague_phrases(paragraph, vague_phrases)

        ambiguity_score = compute_clause_score(
            len(ambiguous_modals),
            vague_result["count"]
        )

        if ambiguity_score > 0:
            ambiguous_clause_count += 1

            clause_results.append({
                "clause_id": i + 1,
                "text": paragraph,
                "ambiguity_score": ambiguity_score,
                "modal_verbs": ambiguous_modals,
                "vague_phrases": vague_result["phrases"]
            })

    # ---- Policy-level coverage ----
    policy_coverage = {
        "purpose": "missing",
        "retention": "missing",
        "data_categories": "missing",
        "access_rights": "missing"
    }

    for paragraph in paragraphs:

        found, status = mentions_purpose(paragraph)
        if found:
            policy_coverage["purpose"] = (
                "explicit" if status == "explicit" else
                "vague" if policy_coverage["purpose"] != "explicit" else "explicit"
            )

        found, status = mentions_retention(paragraph)
        if found:
            policy_coverage["retention"] = (
                "explicit" if status == "explicit" else
                "vague" if policy_coverage["retention"] != "explicit" else "explicit"
            )

        found, status = mentions_data_category(paragraph)
        if found:
            policy_coverage["data_categories"] = (
                "explicit" if status == "explicit" else
                "vague" if policy_coverage["data_categories"] != "explicit" else "explicit"
            )

        found, status = mentions_access_rights(paragraph)
        if found:
            policy_coverage["access_rights"] = (
                "explicit" if status == "explicit" else
                "vague" if policy_coverage["access_rights"] != "explicit" else "explicit"
            )

    policy_level_details = {}

    for key, detector in [
        ("retention", mentions_retention),
        ("purpose", mentions_purpose),
        ("data_categories", mentions_data_category),
        ("access_rights", mentions_access_rights),
    ]:
        if policy_coverage[key] in ["missing", "vague"]:
            policy_level_details[key] = {
                "status": policy_coverage[key],
                "related_clauses": get_anchor_related_clauses(
                    paragraphs,
                    vectorizer,
                    ANCHORS[key],
                    detector,
                    anchor_type=key
                )
            }
        else:
            policy_level_details[key] = {"status": "explicit"}

    return {
        "policy_summary": {
            "total_clauses": len(paragraphs),
            "ambiguous_clause_count": ambiguous_clause_count,
            "ambiguity_ratio": round(
                ambiguous_clause_count / len(paragraphs), 2
            ),
            "coverage": policy_level_details
        },
        "clause_analysis": clause_results
    }


if __name__ == "__main__":
    policy_text = load_policy("../data/zomato_policy.txt")

    final_output = analyze_policy(policy_text)

    output_path = "../output/report.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    print(f"✅ Output successfully saved to '{output_path}'")