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

policy_text = load_policy("../data/zomato_policy.txt")
vague_phrases = load_vague_phrases("../rules/vague_phrases.txt")
paragraphs = segment_into_paragraphs(policy_text)
similarity_matrix, _ = compute_similarity_matrix(paragraphs)

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

similarity_matrix, vectorizer = compute_similarity_matrix(paragraphs)

policy_coverage = {
    "purpose": "missing",
    "retention": "missing",
    "data_categories": "missing",
    "access_rights": "missing"
}

for i, paragraph in enumerate(paragraphs):

    found, status = mentions_purpose(paragraph)

    if found:
        if status == "explicit":
            policy_coverage["purpose"] = "explicit"
        elif policy_coverage["purpose"] != "explicit":
            policy_coverage["purpose"] = "vague"

    found, status = mentions_retention(paragraph)

    if found:
        if status == "explicit":
            policy_coverage["retention"] = "explicit"
        elif policy_coverage["retention"] != "explicit":
            policy_coverage["retention"] = "vague"

    found, status = mentions_data_category(paragraph)

    if found:
        if status == "explicit":
            policy_coverage["data_categories"] = "explicit"
        elif policy_coverage["data_categories"] != "explicit":
            policy_coverage["data_categories"] = "vague"
    
    found, status = mentions_access_rights(paragraph)

    if found:
        if status == "explicit":
            policy_coverage["access_rights"] = "explicit"
        elif policy_coverage["access_rights"] != "explicit":
            policy_coverage["access_rights"] = "vague"


policy_level_details = {}

if policy_coverage["retention"] in ["missing", "vague"]:
    policy_level_details["retention"] = {
        "status": policy_coverage["retention"],
        "related_clauses": get_anchor_related_clauses(
            paragraphs,
            vectorizer,
            ANCHORS["retention"],
            mentions_retention,
            anchor_type="retention"
        )
    }
else:
    policy_level_details["retention"] = {
        "status": "explicit"
    }

if policy_coverage["purpose"] in ["missing", "vague"]:
    policy_level_details["purpose"] = {
        "status": policy_coverage["purpose"],
        "related_clauses": get_anchor_related_clauses(
            paragraphs,
            vectorizer,
            ANCHORS["purpose"],
            mentions_purpose,
            anchor_type="purpose"
        )
    }
else:
    policy_level_details["purpose"] = {
        "status": "explicit"
    }

if policy_coverage["data_categories"] in ["missing", "vague"]:
    policy_level_details["data_categories"] = {
        "status": policy_coverage["data_categories"],
        "related_clauses": get_anchor_related_clauses(
            paragraphs,
            vectorizer,
            ANCHORS["data_categories"],
            mentions_data_category,
            anchor_type="data_categories"
        )
    }
else:
    policy_level_details["data_categories"] = {
        "status": "explicit"
    }

if policy_coverage["access_rights"] in ["missing", "vague"]:
    policy_level_details["access_rights"] = {
        "status": policy_coverage["access_rights"],
        "related_clauses": get_anchor_related_clauses(
            paragraphs,
            vectorizer,
            ANCHORS["access_rights"],
            mentions_access_rights,
            anchor_type="access_rights"
        )
    }
else:
    policy_level_details["access_rights"] = {
        "status": "explicit"
    }

final_output = {
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

output_path = "../output/report.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=4, ensure_ascii=False)

print(f"✅ Output successfully saved to '{output_path}'")