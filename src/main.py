import json
from clause_extractor import load_policy, extract_clauses
from ambiguity_detector import (
    load_vague_phrases,
    detect_vague_phrases,
    detect_modal_verbs,
    detect_missing_specificity
)
from scorer import compute_ambiguity_score, ambiguity_level, policy_level_summary

policy_text = load_policy("../data/sample_policy.txt")
clauses = extract_clauses(policy_text)
vague_phrases = load_vague_phrases("../rules/vague_phrases.txt")

all_clause_results = []
ambiguous_clause_results = []

for i, clause in enumerate(clauses, start=1):
    vague_found = detect_vague_phrases(clause, vague_phrases)
    modals_found = detect_modal_verbs(clause)
    missing_specs = detect_missing_specificity(clause)

    score = compute_ambiguity_score(vague_found, modals_found, missing_specs)
    level = ambiguity_level(score)

    clause_data = {
        "clause_id": i,
        "clause_text": clause,
        "vague_phrases": vague_found,
        "modal_verbs": modals_found,
        "missing_specificity": missing_specs,
        "ambiguity_score": score,
        "ambiguity_level": level
    }

    all_clause_results.append(clause_data)

    if score > 0:
        ambiguous_clause_results.append(clause_data)

summary = policy_level_summary(all_clause_results)

final_report = {
    "policy_summary": summary,
    "ambiguous_clauses": ambiguous_clause_results
}

with open("../output/report.json", "w", encoding="utf-8") as f:
    json.dump(final_report, f, indent=4)

print("Ambiguity analysis report generated: output/report.json")



"""
for i, clause in enumerate(clauses, start=1): = This loop iterates through the list of clauses and prints each clause with a sequential clause number starting from 1.
"""