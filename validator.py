import pandas as pd
import os
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np
import time

# Load environment variables (for API key)
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

def read_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def evaluate_metadata(pdf_text, metadata):
    """Use Gemini to evaluate metadata against PDF content."""
    prompt = f"""
    I need you to evaluate how well the provided metadata matches the content of a document. 
    
    Here's the metadata:
    - Title: {metadata['title']}
    - Creator: {metadata['creator']}
    - Subject: {metadata['subject']}
    - Description: {metadata['description']}
    - Contributor: {metadata['contributor']}
    - Date: {metadata['date']}
    - Type: {metadata['type']}
    - Language: {metadata['language']}
    
    Here's the document content:
    ```
    {pdf_text[:10000]}  # Limiting to first 10000 chars to avoid token limits
    ```
    
    Please evaluate the metadata on these 6 metrics, providing a score between 0-10 for each (where 10 is perfect):
    
    1. Title Relevance: Does the title accurately reflect the main theme or content of the document?
    2. Description Alignment: Does the description summarize the core content of the document?
    3. Creator/Contributor Presence: Are the named creator and contributors mentioned or involved in the document?
    4. Subject Accuracy: Are the listed subjects actually discussed or represented in the document?
    5. Date & Type Validity: Does the document match the date and type provided?
    6. Language Consistency: Is the document written in the language specified in the metadata?
    
    For each metric, provide:
    - Score (0-10)
    - Brief explanation for the score
    
    Finally, calculate an overall score as the average of the six metrics.
    
    Format your response as follows:
    
    Title Relevance Score: [number]
    Title Relevance Explanation: [explanation]
    
    Description Alignment Score: [number]
    Description Alignment Explanation: [explanation]
    
    Creator/Contributor Presence Score: [number]
    Creator/Contributor Presence Explanation: [explanation]
    
    Subject Accuracy Score: [number]
    Subject Accuracy Explanation: [explanation]
    
    Date & Type Validity Score: [number]
    Date & Type Validity Explanation: [explanation]
    
    Language Consistency Score: [number]
    Language Consistency Explanation: [explanation]
    
    Overall Score: [number]
    """
    
    try:
        response = model.generate_content(prompt)
        return parse_evaluation_response(response.text)
    except Exception as e:
        print(f"Error with LLM evaluation: {e}")
        return {
            "title_relevance_score": 0,
            "title_relevance_explanation": "Error evaluating",
            "description_alignment_score": 0,
            "description_alignment_explanation": "Error evaluating",
            "creator_contributor_score": 0,
            "creator_contributor_explanation": "Error evaluating",
            "subject_accuracy_score": 0,
            "subject_accuracy_explanation": "Error evaluating",
            "date_type_validity_score": 0,
            "date_type_validity_explanation": "Error evaluating",
            "language_consistency_score": 0,
            "language_consistency_explanation": "Error evaluating",
            "overall_score": 0
        }

def parse_evaluation_response(response_text):
    """Parse the LLM's response to extract scores and explanations."""
    results = {}
    
    # Extract Title Relevance
    if "Title Relevance Score:" in response_text:
        score_line = response_text.split("Title Relevance Score:")[1].split("\n")[0].strip()
        results["title_relevance_score"] = float(score_line)
        
        expl_parts = response_text.split("Title Relevance Explanation:")[1].split("\n\n")[0].strip()
        results["title_relevance_explanation"] = expl_parts
    else:
        results["title_relevance_score"] = np.nan
        results["title_relevance_explanation"] = "Not evaluated"
    
    # Extract Description Alignment
    if "Description Alignment Score:" in response_text:
        score_line = response_text.split("Description Alignment Score:")[1].split("\n")[0].strip()
        results["description_alignment_score"] = float(score_line)
        
        expl_parts = response_text.split("Description Alignment Explanation:")[1].split("\n\n")[0].strip()
        results["description_alignment_explanation"] = expl_parts
    else:
        results["description_alignment_score"] = np.nan
        results["description_alignment_explanation"] = "Not evaluated"
    
    # Extract Creator/Contributor Presence
    if "Creator/Contributor Presence Score:" in response_text:
        score_line = response_text.split("Creator/Contributor Presence Score:")[1].split("\n")[0].strip()
        results["creator_contributor_score"] = float(score_line)
        
        expl_parts = response_text.split("Creator/Contributor Presence Explanation:")[1].split("\n\n")[0].strip()
        results["creator_contributor_explanation"] = expl_parts
    else:
        results["creator_contributor_score"] = np.nan
        results["creator_contributor_explanation"] = "Not evaluated"
    
    # Extract Subject Accuracy
    if "Subject Accuracy Score:" in response_text:
        score_line = response_text.split("Subject Accuracy Score:")[1].split("\n")[0].strip()
        results["subject_accuracy_score"] = float(score_line)
        
        expl_parts = response_text.split("Subject Accuracy Explanation:")[1].split("\n\n")[0].strip()
        results["subject_accuracy_explanation"] = expl_parts
    else:
        results["subject_accuracy_score"] = np.nan
        results["subject_accuracy_explanation"] = "Not evaluated"
    
    # Extract Date & Type Validity
    if "Date & Type Validity Score:" in response_text:
        score_line = response_text.split("Date & Type Validity Score:")[1].split("\n")[0].strip()
        results["date_type_validity_score"] = float(score_line)
        
        expl_parts = response_text.split("Date & Type Validity Explanation:")[1].split("\n\n")[0].strip()
        results["date_type_validity_explanation"] = expl_parts
    else:
        results["date_type_validity_score"] = np.nan
        results["date_type_validity_explanation"] = "Not evaluated"
    
    # Extract Language Consistency
    if "Language Consistency Score:" in response_text:
        score_line = response_text.split("Language Consistency Score:")[1].split("\n")[0].strip()
        results["language_consistency_score"] = float(score_line)
        
        if "Language Consistency Explanation:" in response_text:
            expl_parts = response_text.split("Language Consistency Explanation:")[1].split("\n\n")[0].strip()
            results["language_consistency_explanation"] = expl_parts
        else:
            results["language_consistency_explanation"] = "Not evaluated"
    else:
        results["language_consistency_score"] = np.nan
        results["language_consistency_explanation"] = "Not evaluated"
    
    # Extract Overall Score
    if "Overall Score:" in response_text:
        score_line = response_text.split("Overall Score:")[1].split("\n")[0].strip()
        try:
            results["overall_score"] = float(score_line)
        except:
            # Calculate it ourselves if parsing fails
            scores = [
                results.get("title_relevance_score", 0),
                results.get("description_alignment_score", 0),
                results.get("creator_contributor_score", 0),
                results.get("subject_accuracy_score", 0),
                results.get("date_type_validity_score", 0),
                results.get("language_consistency_score", 0)
            ]
            scores = [s for s in scores if not np.isnan(s)]
            results["overall_score"] = sum(scores) / len(scores) if scores else 0
    else:
        # Calculate it ourselves
        scores = [
            results.get("title_relevance_score", 0),
            results.get("description_alignment_score", 0),
            results.get("creator_contributor_score", 0),
            results.get("subject_accuracy_score", 0),
            results.get("date_type_validity_score", 0),
            results.get("language_consistency_score", 0)
        ]
        scores = [s for s in scores if not np.isnan(s)]
        results["overall_score"] = sum(scores) / len(scores) if scores else 0
    
    return results

def main(input_file):
    # Load data from Excel
    try:
        # input_file = 'generated_metadata.xlsx'  # Replace with your actual file name
        df = pd.read_excel(input_file)
        print(f"Loaded {len(df)} records from {input_file}")
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # Add columns for evaluation results
    evaluation_columns = [
        "title_relevance_score", "title_relevance_explanation",
        "description_alignment_score", "description_alignment_explanation",
        "creator_contributor_score", "creator_contributor_explanation",
        "subject_accuracy_score", "subject_accuracy_explanation",
        "date_type_validity_score", "date_type_validity_explanation", 
        "language_consistency_score", "language_consistency_explanation",
        "overall_score"
    ]
    
    for col in evaluation_columns:
        df[col] = None
    
    # Process each record
    for idx, row in df.iterrows():
        print(f"Processing record {idx+1}/{len(df)}: {row['identifier']}")
        
        # Prepare PDF path
        # Assuming PDF_PATH_COLUMN exists in your data or can be constructed from identifier
        # Modify this based on your actual file path structure
        pdf_path = row.get('pdf_path', '') 
        if not pdf_path or not os.path.exists(pdf_path):
            # Try to construct from identifier URL if path not available
            if 'identifier_url' in row:
                pdf_id = row['identifier'].split('/')[-1]
                # Example: construct path from ID - adjust this to your file structure
                pdf_path = f"pdfs/{pdf_id}.pdf"
        
        if not os.path.exists(pdf_path):
            print(f"PDF file not found for record {row['identifier']}")
            continue
        
        # Extract text from PDF
        pdf_text = read_pdf(pdf_path)
        if not pdf_text:
            print(f"Could not extract text from PDF {pdf_path}")
            continue
        
        # Create metadata dictionary
        metadata = {
            'title': row.get('title', ''),
            'creator': row.get('creator', ''),
            'subject': row.get('subject', ''),
            'description': row.get('description', ''),
            'contributor': row.get('contributor', ''),
            'date': row.get('date', ''),
            'type': row.get('type', ''),
            'language': row.get('language', '')
        }
        
        # Evaluate metadata against PDF content
        evaluation_results = evaluate_metadata(pdf_text, metadata)
        
        # Update dataframe with evaluation results
        for key, value in evaluation_results.items():
            df.at[idx, key] = value
            
        # Add delay to avoid hitting API rate limits
        time.sleep(30)
    
    # Save results to CSV
    output_file = 'metadata_evaluation_results.csv'
    df.to_csv(output_file, index=False)
    print(f"Evaluation complete. Results saved to {output_file}")

# In validator.py
def validate_metadata(metadata_path):
    main(metadata_path)
    df = pd.read_csv('metadata_evaluation_results.csv')
    # Add your existing validation logic here
    return df[['title_relevance_score', 'description_alignment_score', 
              'creator_contributor_score', 'subject_accuracy_score',
              'date_type_validity_score', 'language_consistency_score', 'overall_score']]