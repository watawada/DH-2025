from fastapi import APIRouter, Form, Depends
from pymongo.database import Database
from bson.objectid import ObjectId
from fastapi.responses import HTMLResponse
from io import BytesIO
from PDF_reader import extract_text_from_pdf, generate_response, parse_flashcards
from database import get_db
from PyPDF2 import PdfReader

router = APIRouter()

@router.post("/generate-flashcards/", response_class=HTMLResponse)
async def generate_flashcards_route(pdf_id: str = Form(...), db: Database = Depends(get_db)):
    """
    Generate flashcards for the selected PDF and display them on a new page.
    """



    try:
        collection = db["files"]
        pdf = collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf:
            return "<h1>Error: PDF not found</h1>"

        pdf_content = BytesIO(pdf["content"])  # Create a BytesIO object from the PDF content
        text = extract_text_from_pdf(pdf_content)  # Pass the BytesIO object to the function

        # Debug: Log the extracted text
        print(f"Extracted text: {text[:500]}")  # Print the first 500 characters of the text

        if not text:
            return "<h1>Error: No text could be extracted from the PDF</h1>"
        prompt = (
            "Create a list of flashcards based on the following text. "
            "Each flashcard should have a keyword, phrase, or question on one side, "
            "and a definition or answer on the other side. Format the response as JSON, "
            "with each flashcard being an object in a list, like this:\n\n"
            "[{\"front\": \"What is X?\", \"back\": \"X is ...\"}, {\"front\": \"Keyword\", \"back\": \"Definition\"}]\n\n"
            f"Text:\n{text}"
        )
        flashcards_json = generate_response(text, prompt)
        print(f"Gemini API Response: {flashcards_json}")  # Debug: Log the raw response

        if not flashcards_json:
            return "<h1>Error: Failed to generate flashcards</h1>"

        flashcards = parse_flashcards(flashcards_json)
        print(f"Parsed Flashcards: {flashcards}")  # Debug: Log the parsed flashcards

        if not flashcards:
            return "<h1>Error: No flashcards generated</h1>"

        flashcards_collection = db["flashcards"]
        flashcards_collection.insert_one({
            "pdf_id": ObjectId(pdf_id),
            "flashcards": flashcards
        })

        flashcards_html = "".join(
            f"<div class='flashcard'><div class='front'>{card}</div><div class='back'>{flashcards[card]}</div></div>"
            for card in flashcards
        )
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flashcards</title>
            <style>
                .flashcard {{ border: 1px solid #ccc; padding: 10px; margin: 10px; }}
                .front {{ font-weight: bold; }}
                .back {{ color: gray; }}
            </style>
        </head>
        <body>
            <h1>Flashcards for PDF: {pdf['name']}</h1>
            {flashcards_html}
            <br>
            <a href="/flashcard-form/">Generate Flashcards for Another PDF</a>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

@router.get("/flashcard-form/", response_class=HTMLResponse)
def flashcard_form(db: Database = Depends(get_db)):
    """
    Serve an HTML form with a dropdown menu to select a PDF for flashcard generation.
    """
    try:
        collection = db["files"]
        pdfs = collection.find({}, {"_id": 1, "name": 1})
        options = "".join(f'<option value="{str(pdf["_id"])}">{pdf["name"]}</option>' for pdf in pdfs)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Generate Flashcards</title>
        </head>
        <body>
            <h1>Select a PDF to Generate Flashcards</h1>
            <form action="/generate-flashcards/" method="post">
                <label for="pdf_id">Choose a PDF:</label>
                <select id="pdf_id" name="pdf_id" required>
                    {options}
                </select>
                <br><br>
                <button type="submit">Generate Flashcards</button>
            </form>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"