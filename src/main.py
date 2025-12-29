from clause_extractor import load_policy, extract_clauses
from ambiguity_detector import (
    load_vague_phrases,
    detect_vague_phrases,
    detect_modal_verbs,
    detect_missing_specificity
)

policy_text = load_policy("../data/sample_policy.txt")
clauses = extract_clauses(policy_text)
vague_phrases = load_vague_phrases("../rules/vague_phrases.txt")

for i, clause in enumerate(clauses, start=1):
    vague_found = detect_vague_phrases(clause, vague_phrases)
    modals_found = detect_modal_verbs(clause)
    missing_specs = detect_missing_specificity(clause)

    print(f"\nClause {i}: {clause}")
    print(f"  Vague phrases: {vague_found}")
    print(f"  Modal verbs: {modals_found}")
    print(f"  Missing specifics: {missing_specs}")



"""
for i, clause in enumerate(clauses, start=1): = This loop iterates through the list of clauses and prints each clause with a sequential clause number starting from 1.
"""