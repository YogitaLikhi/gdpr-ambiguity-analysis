import pandas as pd

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

from src.ambiguity_detector import (
    detect_modal_verbs,
    detect_vague_phrases,
    load_vague_phrases
)

from src.clause_scorer import compute_clause_score


# Load dataset
df = pd.read_csv(
    "Sem2/dataset/ambiguity_dataset.csv",
    encoding="utf-8",
    encoding_errors="ignore"
)

texts = df["clause"]
y_true = df["label"]


# Load vague phrases
vague_phrases = load_vague_phrases()


# Rule-based predictions
y_pred = []

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

    # Same Sem1 logic
    prediction = 1 if ambiguity_score > 0 else 0

    y_pred.append(prediction)


# Evaluation
print("\n===== RULE-BASED RESULTS =====\n")

print("Accuracy:")
print(accuracy_score(y_true, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))

print("\nClassification Report:")
print(classification_report(y_true, y_pred))