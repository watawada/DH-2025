from fastapi import APIRouter, Form, File, UploadFile, Depends
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from pymongo.database import Database
from database import get_db

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Database = Depends(get_db),
    request: Request = None
):
    """
    Upload a PDF file and save it in the database.
    """
    if not request.session:
        return {"Error": "Not authenticated"}
        
        
    try:
        user_email = request.session.get("user_email")

        file_content = await file.read()
        collection = db["files"]
        pdf_result = collection.insert_one({
            "name": name,
            "filename": file.filename,
            "content": file_content,
        })

        # Get the inserted PDF's ObjectId
        pdf_id = pdf_result.inserted_id

        # Update the current user's "files" array in the "users" collection
        user_collection = db["users"]
        user_collection.update_one(
            {"email": user_email},  
            {"$push": {"files": pdf_id}}  # Add the PDF's ObjectId to the "files" array
        )
        
        return {"message": "PDF uploaded successfully", "pdf_id": str(pdf_result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}

@router.get("/upload-form/", response_class=HTMLResponse)
def upload_form():
    """
    Serve an HTML form for uploading PDFs with a folder field.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload PDF</title>
    </head>
    <body>
        <h1>Upload a PDF</h1>
        <form action="/upload-pdf/" method="post" enctype="multipart/form-data">
            <label for="name">PDF Name:</label>
            <input type="text" id="name" name="name" required><br><br>
            <label for="file">Choose PDF:</label>
            <input type="file" id="file" name="file" accept="application/pdf" required><br><br>
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """