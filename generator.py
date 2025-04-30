import pandas as pd
import os
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

def read_pdf(pdf_path):
    """Extract text from PDF file (same as validator)"""
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

def extract_metadata(pdf_text):
    """Use Gemini to generate metadata from document content"""
    prompt = f"""
    Analyze the following document content and generate appropriate metadata. 
    Provide only the following fields in exactly this format:
    
    Title: [Document title]
    Creator: [Author/Organization]
    Subject: [Main topics/keywords]
    Description: [Brief summary]
    Contributor: [Contributors if mentioned]
    Date: [Publication date in YYYY-MM-DD format if available]
    Type: [Document type e.g., Report, Research Paper]
    Language: [ISO 639-1 language code e.g., en, fr]
    
    Document Content:
    {pdf_text[:10000]}  # Limit to first 10k characters
    
    Rules:
    1. Use 'Unknown' for any field that can't be determined
    2. Date format must be YYYY-MM-DD or YYYY if only year is available
    3. Language must be 2-letter code
    4. No additional explanations or text
    """
    
    try:
        response = model.generate_content(prompt)
        return parse_metadata(response.text)
    except Exception as e:
        print(f"Error generating metadata: {e}")
        return default_metadata()

def parse_metadata(response_text):
    """Parse Gemini's response into metadata dictionary"""
    metadata = default_metadata()
    
    lines = [line.strip() for line in response_text.split('\n') if line.strip()]
    for line in lines:
        if line.startswith('Title:'):
            metadata['title'] = line.split('Title:', 1)[1].strip()
        elif line.startswith('Creator:'):
            metadata['creator'] = line.split('Creator:', 1)[1].strip()
        elif line.startswith('Subject:'):
            metadata['subject'] = line.split('Subject:', 1)[1].strip()
        elif line.startswith('Description:'):
            metadata['description'] = line.split('Description:', 1)[1].strip()
        elif line.startswith('Contributor:'):
            metadata['contributor'] = line.split('Contributor:', 1)[1].strip()
        elif line.startswith('Date:'):
            metadata['date'] = line.split('Date:', 1)[1].strip()
        elif line.startswith('Type:'):
            metadata['type'] = line.split('Type:', 1)[1].strip()
        elif line.startswith('Language:'):
            lang = line.split('Language:', 1)[1].strip()[:2].lower()
            metadata['language'] = lang if len(lang) == 2 else 'Unknown'
    
    return metadata

def default_metadata():
    """Return default metadata dictionary"""
    return {
        'title': 'Unknown',
        'creator': 'Unknown',
        'subject': 'Unknown',
        'description': 'Unknown',
        'contributor': 'Unknown',
        'date': 'Unknown',
        'type': 'Unknown',
        'language': 'Unknown'
    }

def main(input_file):
    # Load input file
    try:
        # input_file = 'input.xlsx'  # Update with your filename
        df = pd.read_excel(input_file)
        print(f"Loaded {len(df)} records from {input_file}")
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # Add metadata columns
    metadata_fields = [
        'title', 'creator', 'subject', 'description',
        'contributor', 'date', 'type', 'language'
    ]
    
    for field in metadata_fields:
        df[field] = 'Unknown'

    # Process each record
    for idx, row in df.iterrows():
        print(f"Processing {idx+1}/{len(df)}: {row['identifier']}")
        
        # Get PDF path
        pdf_path = row['pdf_path']
        if not os.path.exists(pdf_path):
            print(f"PDF not found: {pdf_path}")
            continue
            
        # Extract text
        pdf_text = read_pdf(pdf_path)
        if not pdf_text:
            print(f"Empty text for {pdf_path}")
            continue
            
        # Generate metadata
        metadata = extract_metadata(pdf_text)
        
        # Update dataframe
        for field in metadata_fields:
            df.at[idx, field] = metadata[field]
            
        # API rate limit delay
        time.sleep(30)
    
    # Save results
    output_file = 'generated_metadata.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Metadata generation complete. Saved to {output_file}")

# In generator.py
def generate_metadata(input_path):
    main(input_path)
    df = pd.read_excel('generated_metadata.xlsx')
    # Add your existing generation logic here
    return {
        "generated": df.to_dict(),
        "stats": {"processed": len(df)}
    }