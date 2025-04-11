from fastapi import APIRouter, Depends, Request  
from pymongo.database import Database
from bson.objectid import ObjectId
from fastapi.responses import HTMLResponse, StreamingResponse
from io import BytesIO
from database import get_db

router = APIRouter()

@router.get("/download-form/", response_class=HTMLResponse)
def download_form(db: Database = Depends(get_db), request: Request = None):
    """
    Serve an HTML form with a dropdown menu to select a PDF for download.
    Only display PDFs that belong to the current user.
    """
    if not request.session:
        return {"error": "Not authenticated"}

    try:
        # Get the current user's email from the session
        user_email = request.session.get("user_email")
        if not user_email:
            return {"error": "User email not found in session"}

        # Fetch the user's document to get their files array
        user_collection = db["users"]
        user = user_collection.find_one({"email": user_email})
        if not user or "files" not in user:
            return {"error": "No files found for the user"}

        # Fetch only the PDFs whose ObjectIds are in the user's files array
        collection = db["files"]
        pdfs = collection.find({"_id": {"$in": user["files"]}}, {"_id": 1, "name": 1})

        # Generate the dropdown options
        options = "".join(f'<option value="{str(pdf["_id"])}">{pdf["name"]}</option>' for pdf in pdfs)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Download PDF</title>
        </head>
        <body>
            <h1>Select a PDF to Download</h1>
            <form action="/download-pdf/" method="get">
                <label for="pdf_id">Choose a PDF:</label>
                <select id="pdf_id" name="pdf_id" required>
                    {options}
                </select>
                <br><br>
                <button type="submit">Download</button>
            </form>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

@router.get("/download-pdf/")
async def download_pdf(pdf_id: str, db: Database = Depends(get_db)):
    """
    Download a PDF file from the database by ID.
    """
    try:
        collection = db["files"]
        pdf = collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf:
            return {"error": "PDF not found"}

        pdf_content = BytesIO(pdf["content"])
        response = StreamingResponse(pdf_content, media_type="application/pdf")
        response.headers["Content-Disposition"] = f"attachment; filename={pdf['filename']}"
        return response
    except Exception as e:
        return {"error": str(e)}