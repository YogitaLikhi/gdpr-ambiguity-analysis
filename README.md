# GDPR Privacy Policy Ambiguity Detection Tool

## 📌 Project Overview

This project presents a **rule-based and semantic-assisted system** to analyze privacy policies for **ambiguity and lack of specificity**, with a focus on GDPR-relevant aspects such as:

* Purpose limitation
* Data retention
* Data categories collected
* User access and control rights

The tool operates **without using Large Language Models (LLMs)** and instead relies on:

* Linguistic rules (modal verbs, vague phrases)
* Clause-level ambiguity scoring
* Policy-level specificity analysis
* TF-IDF–based semantic similarity for clause retrieval
* An interactive **Streamlit UI** for analysis and visualization

---

## 🎯 Key Features

### Clause-Level Analysis

* Detects **modal verbs** (e.g., *may, might, could*)
* Detects **vague phrases** (e.g., *as necessary, from time to time*)
* Computes an **ambiguity score per clause**
* Displays **only ambiguous clauses** in the final report
* Highlights detected modal verbs and vague phrases in the UI

### Policy-Level Specificity Analysis

For each GDPR-relevant aspect, the policy is classified as:

* **Explicit**
* **Vague**
* **Missing**

If a specificity is *vague or missing*, the system:

* Retrieves **semantically related clauses** using TF-IDF similarity
* Displays them on user interaction (collapsible view)

### Summary Metrics

* Total number of clauses
* Number of ambiguous clauses
* Ambiguity ratio

### Evaluation

* Manual expert annotation
* Precision, Recall, and F1-score reported
* Evaluation results shown in the UI sidebar

### Exportability

* Full analysis report downloadable as **JSON**

---

## 🖥️ User Interface (Streamlit)

The Streamlit UI supports:

### Input Methods

* 📋 Paste privacy policy text
* 📄 Upload `.txt` file

### Output Sections

* Policy-level summary cards
* Specificity status blocks (Explicit / Vague / Missing)
* Collapsible ambiguous clauses with highlights
* Downloadable JSON report

### Disclaimer

> *This tool assists in ambiguity detection and does not constitute legal advice.*

---

## 🧠 Methodology (High-Level)

1. **Policy ingestion & paragraph segmentation**
2. **Clause-level ambiguity detection**

   * Modal verb detection (with user-permission exceptions)
   * Vague phrase detection
3. **Ambiguity scoring**
4. **Policy-level specificity checks**

   * Rule-based detection
   * Tri-state classification
5. **Semantic clause retrieval**

   * TF-IDF + cosine similarity
   * Anchor-based scope filtering
6. **Evaluation against annotated ground truth**
7. **Visualization via Streamlit**

---

## 🚀 Future Work

* Context-aware vague phrase handling
* Improved access rights detection
* Better retention period grounding
* Enhanced semantic retrieval using pretrained embeddings
* LLM-assisted reasoning (subject to constraints)
* UI improvements and clause-level navigation

---

## 🛠️ Setup Instructions

### 1. Install Dependencies

pip install -r requirements.txt

### 2. Run the Streamlit App

streamlit run ui/app.py

---

## 📂 Project Structure (Simplified)

```
gdpr_ambiguity_project/
│
├── src/
│   ├── main.py
│   ├── ambiguity_detector.py
│   ├── clause_scorer.py
|   |── constants.py
|   |── paragraph_segmenter.py
│   ├── semantic_similarity.py
│   └── specificity_detector.py
│
├── ui/
│   └── app.py
│
├── rules/
│   └── vague_phrases.txt
│
├── data/
│   └── sample_policies/
│
├── output/
│   └── report.json
│
├── requirements.txt
└── README.md
```

---

## 👩‍💻 Author Notes

* The system intentionally avoids LLMs to ensure transparency, reproducibility, and rule explainability.
* Designed as an academic prototype for privacy policy analysis and evaluation.

---