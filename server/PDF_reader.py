import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os
import json

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

def generate_flashcards(text):
    """Generates flashcards using Gemini Flash 1.5 model."""
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = (
        "Create a list of flashcards based on the following text. "
        "Each flashcard should have a keyword, phrase, or question on one side, "
        "and a definition or answer on the other side. Format the response as JSON, "
        "with each flashcard being an object in a list, like this:\n\n"
        "[{\"front\": \"What is X?\", \"back\": \"X is ...\"}, {\"front\": \"Keyword\", \"back\": \"Definition\"}]\n\n"
        f"Text:\n{text}"
    )
    
    try:
        response = model.generate_content(prompt)
        return response.text  # The response should be a JSON string
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return None

def parse_flashcards(response_text):
    """Parses the JSON response from the AI into a list of flashcards."""
    try:
        flashcards = json.loads(response_text)
        return flashcards  # A list of dictionaries with "front" and "back" keys
    except json.JSONDecodeError as e:
        print(f"Error parsing flashcards: {e}")
        return []

def save_summary_to_file(summary, output_file="summary.txt"):
    """Saves summary to a text file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(summary)
    print(f"Summary saved to {output_file}")

def save_flashcards_to_file(flashcards, output_file="flashcards.json"):
    """Saves flashcards to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(flashcards, file, indent=4)
    print(f"Flashcards saved to {output_file}")

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
    
    # Generate flashcards
    flashcards_json = generate_flashcards(text)
    if flashcards_json:
        flashcards = parse_flashcards(flashcards_json)
        if flashcards:
            # Save flashcards to a file
            save_flashcards_to_file(flashcards)
        else:
            print("Error: No flashcards generated")
    else:
        print("Error: Failed to generate flashcards")

if __name__ == "__main__":
    main()