def compute_ambiguity_score(vague_phrases, modal_verbs, missing_specifics):
    score = 0

    if vague_phrases:
        score += 1

    if modal_verbs:
        score += 1

    score += len(missing_specifics)

    return score


def ambiguity_level(score):
    if score == 0:
        return "Clear"
    elif score == 1:
        return "Low"
    elif score == 2:
        return "Medium"
    else:
        return "High"
    

def policy_level_summary(all_clauses):
    total_clauses = len(all_clauses)

    ambiguous = [c for c in all_clauses if c["ambiguity_score"] > 0]
    high_ambiguity = [c for c in all_clauses if c["ambiguity_score"] >= 3]

    avg_score = (
        sum(c["ambiguity_score"] for c in all_clauses) / total_clauses
        if total_clauses > 0 else 0
    )

    if avg_score < 1:
        risk = "Low"
    elif avg_score < 2:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "total_clauses": total_clauses,
        "ambiguous_clauses": len(ambiguous),
        "high_ambiguity_clauses": len(high_ambiguity),
        "average_ambiguity_score": round(avg_score, 2),
        "overall_risk_level": risk
    }