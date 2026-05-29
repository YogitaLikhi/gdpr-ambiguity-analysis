import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

from Sem2.feature_extractor import build_feature_matrix

from src.ambiguity_detector import (
    detect_modal_verbs,
    detect_vague_phrases,
    load_vague_phrases
)

from src.clause_scorer import compute_clause_score


# =========================
# LOAD DATASET
# =========================

df = pd.read_csv(
    "Sem2/dataset/ambiguity_dataset.csv",
    encoding="utf-8",
    encoding_errors="ignore"
)

texts = df["clause"]
labels = df["label"]


# =========================
# TRAIN-TEST SPLIT
# =========================

X_train_texts, X_test_texts, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)


# =========================
# BUILD FEATURES
# =========================

X_train, tfidf = build_feature_matrix(X_train_texts)

# IMPORTANT:
# use SAME tfidf vocabulary for test data

from scipy.sparse import hstack
import numpy as np

tfidf_test = tfidf.transform(X_test_texts)

vague_phrases = load_vague_phrases()

rule_features_test = []

for text in X_test_texts:

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

    rule_features_test.append([
        modal_count,
        vague_count,
        ambiguity_score,
        clause_length
    ])

rule_features_test = np.array(rule_features_test)

X_test = hstack([
    tfidf_test,
    rule_features_test
])


# =========================
# TRAIN SVM
# =========================

svm_model = SVC(
    kernel="linear",
    class_weight="balanced"
)

svm_model.fit(X_train, y_train)

y_pred_svm = svm_model.predict(X_test)


# =========================
# RULE-BASED PREDICTIONS
# =========================

y_pred_rule = []

for text in X_test_texts:

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

    prediction = 1 if ambiguity_score > 0 else 0

    y_pred_rule.append(prediction)


# =========================
# RULE-BASED RESULTS
# =========================

print("\n==============================")
print("RULE-BASED RESULTS")
print("==============================\n")

print("Accuracy:")
print(accuracy_score(y_test, y_pred_rule))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred_rule))

print("\nClassification Report:")
print(classification_report(y_test, y_pred_rule))


# =========================
# SVM RESULTS
# =========================

print("\n==============================")
print("HYBRID SVM RESULTS")
print("==============================\n")

print("Accuracy:")
print(accuracy_score(y_test, y_pred_svm))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred_svm))

print("\nClassification Report:")
print(classification_report(y_test, y_pred_svm))

# =========================
# ERROR ANALYSIS
# =========================

print("\n==============================")
print("ERROR ANALYSIS")
print("==============================\n")


# Convert to lists for indexing
test_texts = list(X_test_texts)
actual = list(y_test)
predicted = list(y_pred_svm)


print("----- FALSE NEGATIVES -----")
print("Actual = 1, Predicted = 0\n")

for text, y_true, y_pred in zip(test_texts, actual, predicted):

    if y_true == 1 and y_pred == 0:

        print(text)
        print("-" * 80)


print("\n\n----- FALSE POSITIVES -----")
print("Actual = 0, Predicted = 1\n")

for text, y_true, y_pred in zip(test_texts, actual, predicted):

    if y_true == 0 and y_pred == 1:

        print(text)
        print("-" * 80)