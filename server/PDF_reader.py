import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os

# Set up API key (replace with your actual API key)
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file. Accepts either a file path or a BytesIO object.
    """
    try:
        if isinstance(pdf_file, (str, bytes, os.PathLike)):
            # If it's a file path, open the file
            with open(pdf_file, "rb") as f:
                reader = PdfReader(f)
        else:
            # If it's a BytesIO object, use it directly
            reader = PdfReader(pdf_file)

        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return ""

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