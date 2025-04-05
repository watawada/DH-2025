import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv

import os

# Set up API key (replace with your actual API key)
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def generate_summary(text):
    """Generates summary using Gemini Flash 1.5 model."""
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"Please provide a concise summary of the following text:\n\n{text}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None

def save_summary_to_file(summary, output_file="summary.txt"):
    """Saves summary to a text file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(summary)
    print(f"Summary saved to {output_file}")

def main():
    # Get PDF path from user
    pdf_path = input("Enter the path to your PDF file: ").strip()
    
    if not os.path.exists(pdf_path):
        print("Error: File not found")
        return
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("Error: No text extracted from PDF")
        return
    
    # Generate summary
    summary = generate_summary(text)
    if summary:
        # Save summary
        save_summary_to_file(summary)

if __name__ == "__main__":
    main()