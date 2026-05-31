import re
import csv


def extract_sentences(text, min_length=15):

    # Normalize line breaks
    text = text.replace("\r\n", " ").replace("\n", " ")

    # Step 1: Sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+', text)

    final_clauses = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        # Step 2: Split further using semicolons and colons
        sub_clauses = re.split(r'[;:]', sentence)

        for clause in sub_clauses:

            cleaned = clause.strip()

            # Remove very short/noisy fragments
            if (len(cleaned) >= min_length and len(cleaned.split()) >= 5):
                final_clauses.append(cleaned)

    return final_clauses


def load_policy(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def save_to_csv(clauses, output_path):

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile)

        # Header
        writer.writerow(["clause", "label"])

        # Empty labels for manual annotation
        for clause in clauses:
            writer.writerow([clause, ""])


if __name__ == "__main__":

    input_file = "../../data/zepto_policy.txt"

    output_file = "dataset.csv"

    policy_text = load_policy(input_file)

    clauses = extract_sentences(policy_text)

    save_to_csv(clauses, output_file)

    print(f"✅ Dataset created successfully: {output_file}")