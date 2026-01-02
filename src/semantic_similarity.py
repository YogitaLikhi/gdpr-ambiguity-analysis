from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from specificity_detector import is_customer_data_context


def compute_similarity_matrix(paragraphs):

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1
    )

    tfidf_matrix = vectorizer.fit_transform(paragraphs)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    return similarity_matrix, vectorizer


def get_top_k_similar(similarity_matrix, index, k=3, threshold=0.25):

    similarities = similarity_matrix[index]

    ranked = sorted(
        enumerate(similarities),
        key=lambda x: x[1],
        reverse=True
    )

    # Skip self (index 0)
    similar = [
        idx for idx, score in ranked[1:]
        if score >= threshold
    ]

    return similar[:k]


def get_anchor_related_clauses(
    paragraphs,
    vectorizer,
    anchor_text,
    detect_fn,
    anchor_type,
    max_clauses=3,
    threshold=0.05,
):
    
    used_indices = set()

    anchor_vec = vectorizer.transform([anchor_text])
    para_vecs = vectorizer.transform(paragraphs)

    similarities = cosine_similarity(anchor_vec, para_vecs)[0]

    ranked = sorted(
        enumerate(similarities),
        key=lambda x: x[1],
        reverse=True
    )

    related = []
    for idx, score in ranked:
        if score < threshold:
            break

        if idx in used_indices:
            continue

        if anchor_type == "retention":
            if not is_customer_data_context(paragraphs[idx]):
                continue

        found, _ = detect_fn(paragraphs[idx])
        if found:
            continue

        related.append({
            "clause_id": idx + 1,
            "text": paragraphs[idx][:300]
        })

        used_indices.add(idx)

        used_indices.add(idx - 1)
        used_indices.add(idx + 1)

        if len(related) >= max_clauses:
            break

    return related

"""
def compute_similarity_matrix(paragraphs):
    Computes TF-IDF cosine similarity matrix for paragraphs.
    
    Args:
        paragraphs (List[str]): Paragraph blocks
    
    Returns:
        similarity_matrix (2D array)
        vectorizer (TfidfVectorizer)


def get_top_k_similar(similarity_matrix, index, k=3, threshold=0.25):
    Returns indices of top-k semantically similar paragraphs. 
"""