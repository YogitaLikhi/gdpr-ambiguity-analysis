# Privacy Policy Clause Ambiguity Detection

This project detects **ambiguous clauses** in privacy policies using an **explainable, rule-based NLP pipeline** enhanced with **semantic similarity** for contextual retrieval. The system is designed for legal and compliance analysis, prioritizing transparency over black-box accuracy.

---

## 🎯 Objective

To automatically identify clauses in privacy policies that are **ambiguous**, **vague**, or **underspecified**, particularly with respect to:
- Data collection
- Data sharing
- Data retention
- User rights and access
- Legal disclosures

---

## 🧠 Approach

The system follows a **hybrid architecture**:

### 1. Rule-Based Ambiguity Detection
- Modal verb analysis (e.g., *may*, *might*, *generally*)
- Vague temporal expressions (e.g., *as long as necessary*)
- Missing or underspecified obligations
- Explicit vs vague vs missing specificity scoring

### 2. Semantic Clause Retrieval
- TF-IDF vectorization with n-grams
- Cosine similarity for paragraph-to-paragraph matching
- Anchor-based retrieval to locate related clauses
- Scope filtering to avoid cross-section contamination (e.g., career vs customer data)

### 3. Explainability
Each flagged clause is accompanied by:
- Ambiguity score
- Detected linguistic signals
- Retrieved related clauses (when applicable)

---

## 🛠️ Technologies Used

- Python
- scikit-learn (TF-IDF, cosine similarity)
- Pandas
- Regex-based NLP rules

---

## 📊 Evaluation

- Expert-annotated ground truth dataset
- Binary classification: Ambiguous (1) / Not Ambiguous (0)
- Metrics used:
  - Precision
  - Recall
  - F1-score

---

## 📁 Project Structure
# Privacy Policy Clause Ambiguity Detection

This project detects **ambiguous clauses** in privacy policies using an **explainable, rule-based NLP pipeline** enhanced with **semantic similarity** for contextual retrieval. The system is designed for legal and compliance analysis, prioritizing transparency over black-box accuracy.

---

## 🎯 Objective

To automatically identify clauses in privacy policies that are **ambiguous**, **vague**, or **underspecified**, particularly with respect to:
- Data collection
- Data sharing
- Data retention
- User rights and access
- Legal disclosures

---

## 🧠 Approach

The system follows a **hybrid architecture**:

### 1. Rule-Based Ambiguity Detection
- Modal verb analysis (e.g., *may*, *might*, *generally*)
- Vague temporal expressions (e.g., *as long as necessary*)
- Missing or underspecified obligations
- Explicit vs vague vs missing specificity scoring

### 2. Semantic Clause Retrieval
- TF-IDF vectorization with n-grams
- Cosine similarity for paragraph-to-paragraph matching
- Anchor-based retrieval to locate related clauses
- Scope filtering to avoid cross-section contamination (e.g., career vs customer data)

### 3. Explainability
Each flagged clause is accompanied by:
- Ambiguity score
- Detected linguistic signals
- Retrieved related clauses (when applicable)

---

## 🛠️ Technologies Used

- Python
- scikit-learn (TF-IDF, cosine similarity)
- Pandas
- Regex-based NLP rules

❗ No large language models (LLMs) or pretrained classifiers are used to ensure:
- Full explainability
- Clear attribution of system behavior
- Suitability for low-resource and academic evaluation settings

---

## 📊 Evaluation

- Expert-annotated ground truth dataset
- Binary classification: Ambiguous (1) / Not Ambiguous (0)
- Metrics used:
  - Precision
  - Recall
  - F1-score

### Current Results
- Precision: **0.63**
- Recall: **0.47**
- F1-score: **0.54**

Given the rule-based nature of the system, these results are considered acceptable and interpretable.

---

## 📁 Project Structure
├── main.py # Main pipeline
├── semantic_similarity.py # TF-IDF clause similarity
├── ambiguity_detector.py # Ambiguity detection rules
├── evaluation.py # Precision / Recall / F1
├── data/
│ ├── policies.txt
│ └── annotated_clauses.csv
└── README.md

## 👩‍💻 Author

Yogita Likhi  
Mini Project – Privacy Policy Analysis  