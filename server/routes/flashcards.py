from fastapi import APIRouter, Form, Depends
from pymongo.database import Database
from bson.objectid import ObjectId
from fastapi.responses import HTMLResponse
from io import BytesIO
from PDF_reader import extract_text_from_pdf, generate_response, parse_flashcards
from database import get_db
from PyPDF2 import PdfReader

router = APIRouter()

@router.post("/generate-flashcards/")
async def generate_flashcards_route(pdf_id: str = Form(...), db: Database = Depends(get_db)):
    """
    Generate flashcards for the selected PDF and return them in the response.
    """
    try:
        collection = db["files"]
        pdf = collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf:
            return {"error": "PDF not found"}

        pdf_content = BytesIO(pdf["content"])
        text = extract_text_from_pdf(pdf_content)

        if not text:
            return {"error": "No text could be extracted from the PDF"}

        # Generate flashcards using Gemini
        prompt = (
            "Create a list of flashcards based on the following text. "
            "Each flashcard should have a keyword, phrase, or question on one side, "
            "and a definition or answer on the other side. Format the response as JSON, "
            "with each flashcard being an object in a list, like this:\n\n"
            "[{\"front\": \"What is X?\", \"back\": \"X is ...\"}, {\"front\": \"Keyword\", \"back\": \"Definition\"}]\n\n"
        )
        flashcards_json = generate_response(text, prompt)

        if not flashcards_json:
            return {"error": "Failed to generate flashcards"}

        # Parse the flashcards JSON
        flashcards = parse_flashcards(flashcards_json)

        if not flashcards:
            return {"error": "No flashcards generated"}

        return {"flashcards": flashcards}  # Return the generated flashcards
    except Exception as e:
        return {"error": str(e)}

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