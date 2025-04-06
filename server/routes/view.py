from fastapi import APIRouter, Depends
from pymongo.database import Database
from bson.objectid import ObjectId
from fastapi.responses import HTMLResponse, StreamingResponse
from io import BytesIO
from database import get_db

router = APIRouter()

@router.get("/view-form/", response_class=HTMLResponse)
def view_form(db: Database = Depends(get_db)):
    """
    Serve an HTML form with a dropdown menu to select a PDF for viewing.
    """
    try:
        collection = db["files"]
        pdfs = collection.find({}, {"_id": 1, "name": 1})
        options = "".join(f'<option value="{str(pdf["_id"])}">{pdf["name"]}</option>' for pdf in pdfs)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>View PDF</title>
        </head>
        <body>
            <h1>Select a PDF to View</h1>
            <form action="/view-pdf/" method="get">
                <label for="pdf_id">Choose a PDF:</label>
                <select id="pdf_id" name="pdf_id" required>
                    {options}
                </select>
                <br><br>
                <button type="submit">View</button>
            </form>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

@router.get("/view-pdf/")
async def view_pdf(pdf_id: str, db: Database = Depends(get_db)):
    """
    View a PDF file from the MongoDB collection by ID.
    """
    try:
        collection = db["files"]
        pdf = collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf:
            return {"error": "PDF not found"}

        pdf_content = BytesIO(pdf["content"])
        response = StreamingResponse(pdf_content, media_type="application/pdf")
        response.headers["Content-Disposition"] = f"inline; filename={pdf['filename']}"
        return response
    except Exception as e:
        return {"error": str(e)}