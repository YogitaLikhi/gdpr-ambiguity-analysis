import streamlit as st
import json
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from Sem2.policy_analyzer import analyze_policy


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Hybrid Privacy Policy Analyzer",
    layout="wide"
)


# =====================================
# STYLING
# =====================================

st.markdown("""
<style>

.main {
    padding: 2rem;
}

.section-card {
    background-color: #f9fafb;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid #e5e7eb;
}

.badge-explicit {
    background-color: #d1fae5;
    color: #065f46;
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 600;
}

.badge-vague {
    background-color: #fef3c7;
    color: #92400e;
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 600;
}

.badge-missing {
    background-color: #fee2e2;
    color: #991b1b;
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =====================================
# TITLE
# =====================================

st.title("Privacy Policy Ambiguity Analyzer")

st.caption(
    "Hybrid Machine Learning Approach (TF-IDF + Rule Features + SVM)"
)


# =====================================
# SIDEBAR
# =====================================

st.sidebar.header("Model Information")

st.sidebar.markdown("""
### Classifier
Hybrid SVM

### Features
- TF-IDF
- Modal Verbs
- Vague Phrases
- Clause Length

### Dataset
- 239 Annotated Clauses

### Performance
- Accuracy ≈ 90%
- F1 Score ≈ 85%
""")

st.sidebar.markdown(
    "<small><i>This tool assists in ambiguity detection and does not constitute legal advice.</i></small>",
    unsafe_allow_html=True
)


# =====================================
# INPUT
# =====================================

st.markdown("## Input Policy")

input_mode = st.radio(
    "Choose Input Method",
    [
        "Paste Policy Text",
        "Upload TXT File"
    ]
)

policy_text = ""

if input_mode == "Paste Policy Text":

    policy_text = st.text_area(
        "Paste policy text",
        height=300
    )

else:

    uploaded_file = st.file_uploader(
        "Upload Policy",
        type=["txt"]
    )

    if uploaded_file:

        policy_text = uploaded_file.read().decode(
            "utf-8"
        )


# =====================================
# ANALYZE
# =====================================

if st.button("Analyze Policy"):

    if not policy_text.strip():

        st.warning(
            "Please provide a policy first."
        )

        st.stop()

    result = analyze_policy(
        policy_text
    )

    summary_tab, coverage_tab, ambiguity_tab = st.tabs(
        [
            "📊 Summary",
            "📑 Coverage Analysis",
            "⚠️ Ambiguous Clauses"
        ]
    )


    # =================================
    # SUMMARY
    # =================================

    with summary_tab:
        summary = result["policy_summary"]
        coverage = result["policy_coverage"]

        coverage_found = sum(
            1
            for item in coverage.values()
            if item["status"] != "missing"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Clauses",
                summary["total_clauses"]
        )

        with col2:
            st.metric(
                "Ambiguous Clauses",
                summary["ambiguous_clauses"]
        )

        with col3:
            st.metric(
                "Ambiguity Ratio",
                f"{summary['ambiguity_ratio']:.2f}"
        )

        with col4:
            st.metric(
                "Coverage Found",
                f"{coverage_found}/4"
        )

        st.subheader("Policy Ambiguity Level")

        st.progress(
            float(summary["ambiguity_ratio"])
        )

    # =================================
    # COVERAGE
    # =================================


    with coverage_tab:
        
        coverage = result["policy_coverage"]

        def show_coverage(title, item):

            status = item["status"]

            if status == "explicit":
                st.success(f"{title}: Explicit")

            elif status == "vague":
                st.warning(f"{title}: Vague")

            else:
                st.error(f"{title}: Missing")

            if item["evidence"]:

                st.markdown("**Evidence Clause**")

                st.info(item["evidence"])

                st.divider()

            if item["source_paragraph"]:

                with st.expander(
                    "Source Paragraph"
                ):
                    st.write(
                        item["source_paragraph"]
                    )
        
        left, right = st.columns(2)

        with left:

            with st.container(border=True):
                show_coverage(
                    "Purpose",
                    coverage["purpose"]
                )

            with st.container(border=True):
                show_coverage(
                    "Retention",
                    coverage["retention"]
                )

        with right:
            with st.container(border=True):
                show_coverage(
                    "Data Categories",
                    coverage["data_categories"]
                )

            with st.container(border=True):
                show_coverage(
                    "Access Rights",
                    coverage["access_rights"]
                )


    # =================================
    # AMBIGUOUS CLAUSES
    # =================================

    st.caption(
        f"Detected {summary['ambiguous_clauses']} ambiguous clauses"
    )

    with ambiguity_tab:
        for paragraph in result["paragraph_analysis"]:

            for clause in paragraph["clauses"]:

                if clause["prediction"] != 1:
                    continue

                confidence = clause["confidence"]

                if confidence >= 0.9:
                    icon = "🔴"

                elif confidence >= 0.6:
                    icon = "🟠"

                else:
                    icon = "🟡"

                with st.expander(
                    f"{icon} Confidence {confidence}"
                ):
                    text = clause["text"]

                    for modal in clause["modal_verbs"]:

                        text = text.replace(
                            modal,
                            f"<span style='background-color:#FFD580'>{modal}</span>"
                        )

                    for phrase in clause["vague_phrases"]:

                        text = text.replace(
                            phrase,
                            f"<span style='background-color:#FFB6B6'>{phrase}</span>"
                        )

                    st.markdown(
                        text,
                        unsafe_allow_html=True
                    )

    st.download_button(
        label="📥 Download Analysis Report (JSON)",
        data=json.dumps(
            result,
            indent=4
        ),
        file_name="policy_analysis_report.json",
        mime="application/json"
    )