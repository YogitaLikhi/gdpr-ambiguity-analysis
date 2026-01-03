import streamlit as st
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from main import analyze_policy


st.markdown("""
<style>
hr {
    border: none !important;
    height: 0 !important;
    margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Page padding */
.main {
    padding: 2rem 3rem;
}

/* Section card */
.section-card {
    background-color: #f9fafb;
    padding: 20px;
    margin-bottom: 25px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
}

/* Status badges */
.badge-explicit {
    background-color: #d1fae5;
    color: #065f46;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.badge-vague {
    background-color: #fef3c7;
    color: #92400e;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.badge-missing {
    background-color: #fee2e2;
    color: #991b1b;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

/* Improve expanders spacing */
div.streamlit-expander {
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

/* Sidebar spacing */
section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* Evaluation box */
.eval-box {
    background-color: #f3f4f6;
    padding: 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    color: #374151;
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="Privacy Policy Ambiguity Analyzer",
    layout="wide"
)

st.title("Privacy Policy Ambiguity Analyzer")
st.write("GDPR Policy Ambiguity Detection")


st.sidebar.header("Ambiguity Score Guide")
st.sidebar.markdown("""
- **1** – Modal verb ambiguity  
- **2** – Vague phrase ambiguity  
- **3+** – Multiple ambiguity indicators  
""")

st.sidebar.markdown(
    "<small><i>This tool assists in ambiguity detection and does not constitute legal advice.</i></small>",
    unsafe_allow_html=True
)

st.sidebar.markdown("<div style='height: 65vh'></div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div class="eval-box">
<b>Evaluation (Expert Annotation)</b><br>
Precision: 0.64<br>
Recall: 0.47<br>
F1-Score: 0.54
</div>
""", unsafe_allow_html=True)


st.markdown("## 📄 Input Privacy Policy")

input_mode = st.radio(
    "Choose input method:",
    ["Paste policy text", "Upload .txt file"]
)

policy_text = ""

if input_mode == "Paste policy text":
    policy_text = st.text_area(
        "Paste policy text here",
        height=300
    )

else:
    uploaded_file = st.file_uploader(
        "Upload policy text file",
        type=["txt"]
    )
    if uploaded_file is not None:
        policy_text = uploaded_file.read().decode("utf-8")


if st.button("Analyze"):
    if not policy_text.strip():
        st.warning("Please paste a privacy policy first.")
        st.stop()

    result = analyze_policy(policy_text)
    
    summary = result["policy_summary"]

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Policy Ambiguity Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Clauses", summary["total_clauses"])

    with col2:
        st.metric("Ambiguous Clauses", summary["ambiguous_clause_count"])

    with col3:
        st.metric("Ambiguity Ratio", summary["ambiguity_ratio"])
    st.markdown("</div>", unsafe_allow_html=True)

    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## 📑 Policy Coverage Analysis")

    left, right = st.columns(2)

    def show_coverage_block(title, item):
        status = item["status"]
    
        st.markdown(f"### {title}")
        badge_class = {
            "explicit": "badge-explicit",
            "vague": "badge-vague",
            "missing": "badge-missing"
        }[status]

        st.markdown(
            f"Status: <span class='{badge_class}'>{status.capitalize()}</span>",
            unsafe_allow_html=True
        )       

        if status in ["missing", "vague"] and "related_clauses" in item:
            with st.expander("Show related clauses"):
                for clause in item["related_clauses"]:
                    st.markdown(clause["text"])

    with left:
        show_coverage_block("Purpose", summary["coverage"]["purpose"])
        show_coverage_block("Retention", summary["coverage"]["retention"])

    with right:
        show_coverage_block("Data Categories", summary["coverage"]["data_categories"])
        show_coverage_block("Access Rights", summary["coverage"]["access_rights"])
    st.markdown("</div>", unsafe_allow_html=True)


    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## ⚠️ Ambiguous Clauses")
    st.caption(f"Showing {len(result['clause_analysis'])} ambiguous clauses")

    for clause in result["clause_analysis"]:
        with st.expander(f"Clause {clause['clause_id']} | Score {clause['ambiguity_score']}"):
        
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

            st.markdown(text, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        label="📥 Download Analysis Report (JSON)",
        data=json.dumps(result, indent=4),
        file_name="policy_ambiguity_report.json",
        mime="application/json"
    )