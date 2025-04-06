from fastapi import APIRouter, Form, Depends
from pymongo.database import Database
from bson.objectid import ObjectId
from fastapi.responses import HTMLResponse
from database import get_db

router = APIRouter()

@router.get("/delete-form/", response_class=HTMLResponse)
def delete_form(db: Database = Depends(get_db)):
    """
    Serve an HTML form with a dropdown menu to select a PDF for deletion.
    """
    try:
        collection = db["files"]
        pdfs = collection.find({}, {"_id": 1, "name": 1})
        options = "".join(f'<option value="{str(pdf["_id"])}">{pdf["name"]}</option>' for pdf in pdfs)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Delete PDF</title>
        </head>
        <body>
            <h1>Select a PDF to Delete</h1>
            <form action="/delete-pdf/" method="post">
                <label for="pdf_id">Choose a PDF:</label>
                <select id="pdf_id" name="pdf_id" required>
                    {options}
                </select>
                <br><br>
                <button type="submit">Delete</button>
            </form>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

@router.post("/delete-pdf/")
async def delete_pdf(pdf_id: str = Form(...), db: Database = Depends(get_db)):
    """
    Delete a PDF file from the MongoDB collection by ID.
    """
    try:
        collection = db["files"]
        result = collection.delete_one({"_id": ObjectId(pdf_id)})
        if result.deleted_count == 0:
            return {"error": "PDF not found or could not be deleted"}

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Delete Success</title>
        </head>
        <body>
            <h1>PDF Deleted Successfully</h1>
            <a href="/delete-form/">Delete Another PDF</a>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Delete Failed</title>
        </head>
        <body>
            <h1>PDF Deletion Failed</h1>
            <p>Error: {str(e)}</p>
            <a href="/delete-form/">Try Again</a>
        </body>
        </html>
        """