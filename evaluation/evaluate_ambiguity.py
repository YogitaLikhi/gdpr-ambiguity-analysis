import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

df = pd.read_csv("annotated_clauses.csv", sep=";")

y_true = df["ground_truth_ambiguous"]
y_pred = df["predicted_ambiguous"]

precision, recall, f1, _ = precision_recall_fscore_support(
    y_true, y_pred, average="binary"
)

print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)