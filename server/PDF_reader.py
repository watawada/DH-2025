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
    Extracts text from a PDF file.
    :param pdf_file: A BytesIO object containing the PDF content.
    :return: Extracted text as a string.
    """
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def generate_response(text, prompt):
    """Generates flashcards using Gemini Flash 1.5 model."""
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    try:
        response = model.generate_content(prompt+"\nText:\n"+text)
        # Debug: Log the raw response from the Gemini API
        print(f"Gemini API response: {response.text}")
        return response.text  # The response should be a JSON string
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return None

def parse_flashcards(response_text):
    """Parses the JSON response from the AI into a dictionary of flashcards."""
    try:
        if not response_text:
            print("Error: Empty response text")
            return {}

        print(f"Raw response text before cleaning: {repr(response_text)}")  # Debug: Log the raw response

        # Clean the response text by removing the ```json block
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove the leading ```json
        if response_text.endswith("```\n"):
            response_text = response_text[:-4]  # Remove the trailing ```

        cleaned_response = response_text.strip()  # Remove any extra whitespace or newlines
        print(f"Cleaned response text: {repr(cleaned_response)}")  # Debug: Log the cleaned response

        # Parse the JSON response
        flashcards_list = json.loads(cleaned_response)

        # Convert the list of flashcards into a dictionary
        flashcards_dict = {card["front"]: card["back"] for card in flashcards_list}

        # Debug: Log the parsed flashcards dictionary
        print(f"Parsed flashcards dictionary: {flashcards_dict}")

        return flashcards_dict
    except json.JSONDecodeError as e:
        print(f"Error parsing flashcards: {e}")
        print(f"Raw response text: {repr(response_text)}")  # Debug: Log the raw response
        return {}
    except KeyError as e:
        print(f"Error: Missing expected keys in flashcards: {e}")
        return {}
    
def parse_reviewquiz(response_text):
    """Parses the JSON response from the AI into a list of review quiz questions."""
    try:
        if not response_text:
            print("Error: Empty response text")
            return []

        # Clean the response text by removing the ```json block
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove the leading ```json
        if response_text.endswith("```\n"):
            response_text = response_text[:-4]  # Remove the trailing ```

        cleaned_response = response_text.strip()  # Remove any extra whitespace or newlines
        print(f"Cleaned response text: {repr(cleaned_response)}")  # Debug: Log the cleaned response

        # Parse the JSON response
        quiz_list = json.loads(cleaned_response)

        # Validate the structure of each question
        for question in quiz_list:
            if not all(key in question for key in ["question", "choices", "correct"]):
                raise KeyError(f"Missing keys in question: {question}")

        return quiz_list
    except json.JSONDecodeError as e:
        print(f"Error parsing review quiz: {e}")
        return []
    except KeyError as e:
        print(f"Error: Missing expected keys in review quiz: {e}")
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