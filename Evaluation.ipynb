
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------- USER CONFIGURATION -------- 
RAW_FILE = " "# File location 
LLM_FILE = " "# File location
OUTPUT_IMAGE = "metadata_comparison_llm_vs_raw.png"

# -------- SCORE FIELDS TO COMPARE --------
score_fields = [
    'title_relevance_score',
    'description_alignment_score',
    'creator_contributor_score',
    'subject_accuracy_score',
    'date_type_validity_score',
    'language_consistency_score',
    'overall_score'
]

def main():
    # Check for file existence
    if not os.path.exists(RAW_FILE):
        print(f"❌ File not found: {RAW_FILE}")
        return
    if not os.path.exists(LLM_FILE):
        print(f"❌ File not found: {LLM_FILE}")
        return

    # Load the files
    raw_df = pd.read_csv(RAW_FILE)
    llm_df = pd.read_csv(LLM_FILE)

    # Handle any text-based errors and compute averages
    raw_avg = raw_df[score_fields].replace('Error evaluating', pd.NA).dropna().astype(float).mean()
    llm_avg = llm_df[score_fields].replace('Error evaluating', pd.NA).dropna().astype(float).mean()

    # Plot the comparison
    plt.figure(figsize=(12, 6))
    plt.plot(score_fields, raw_avg, marker='o', label='Raw Evaluation', linestyle='-')
    plt.plot(score_fields, llm_avg, marker='o', label='LLM Validated', linestyle='-')
    plt.title('Comparison of Average Scores: Raw Evaluation vs LLM Validated')
    plt.xlabel('Metadata Quality Dimension')
    plt.ylabel('Average Score')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the plot
    plt.savefig(OUTPUT_IMAGE)
    print(f"Chart saved as '{OUTPUT_IMAGE}' in the current folder.")

if __name__ == "__main__":
    main()
