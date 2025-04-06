# FastAPI application for uploading, viewing, and managing PDF files with MongoDB
# upload with route upload-pdf/
# view with route view-pdf/ 
# delete with route delete-pdf/
# search with route search-page/
# generate flashcards with route generate-flashcards/

from fastapi import FastAPI, Form, File, UploadFile
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse, StreamingResponse
from io import BytesIO
from PDF_reader import extract_text_from_pdf, generate_flashcards, parse_flashcards
import tempfile

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["PDF"]  # Replace 'mydatabase' with your database name
collection = db["files"]  # Replace 'mycollection' with your collection name

# Test MongoDB connection
@app.get("/test-mongo/")
def test_mongo():
    try:
        # Attempt to list collections in the database
        collections = db.list_collection_names()
        return {"status": "success", "collections": collections}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Base route for testing
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Upload PDF route
@app.post("/upload-pdf/")
async def upload_pdf(
    name: str = Form(...),
    folder: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload a PDF file and save it in the database.
    """
    try:
        # Read the file content
        file_content = await file.read()

        # Save the PDF in the database
        pdf_result = collection.insert_one({
            "name": name,
            "folder": folder,
            "filename": file.filename,
            "content": file_content
        })

        return {"message": "PDF uploaded successfully", "pdf_id": str(pdf_result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}

# HTML form for uploading PDFs
@app.get("/upload-form/", response_class=HTMLResponse)
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
            <label for="folder">Folder:</label>
            <input type="text" id="folder" name="folder" required><br><br>
            <label for="file">Choose PDF:</label>
            <input type="file" id="file" name="file" accept="application/pdf" required><br><br>
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """

# Search PDFs by folder
@app.get("/search-page/", response_class=HTMLResponse)
def search_page(folder: str = None):
    """
    Serve a search page that displays all PDFs or filters by folder.
    """
    try:
        # Query the database for PDFs
        query = {}
        if folder:
            query["folder"] = folder

        pdfs = collection.find(query, {"_id": 1, "name": 1, "filename": 1, "folder": 1})
        results = [{"id": str(pdf["_id"]), "name": pdf["name"], "filename": pdf["filename"], "folder": pdf["folder"]} for pdf in pdfs]

        # Generate table rows for the results
        if results:
            table_rows = "".join(
                f"<tr><td>{pdf['name']}</td><td>{pdf['filename']}</td><td>{pdf['folder']}</td></tr>" for pdf in results
            )
        else:
            table_rows = "<tr><td colspan='3'>No PDFs found</td></tr>"

        # Generate the HTML page
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Search PDFs</title>
        </head>
        <body>
            <h1>Search PDFs</h1>
            <form action="/search-page/" method="get">
                <label for="folder">Filter by Folder:</label>
                <input type="text" id="folder" name="folder" placeholder="Enter folder name">
                <button type="submit">Search</button>
            </form>
            <br>
            <h2>Uploaded PDFs</h2>
            <table border="1">
                <tr>
                    <th>Name</th>
                    <th>Filename</th>
                    <th>Folder</th>
                </tr>
                {table_rows}
            </table>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

# Flashcard generation route
@app.post("/generate-flashcards/", response_class=HTMLResponse)
async def generate_flashcards_route(pdf_id: str = Form(...)):
    """
    Generate flashcards for the selected PDF and display them on a new page.
    """
    try:
        # Fetch the PDF from the database
        pdf = collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf:
            return f"<h1>Error: PDF not found</h1>"

        # Extract text from the PDF content
        pdf_content = BytesIO(pdf["content"])
        text = extract_text_from_pdf(pdf_content)

        if not text:
            return f"<h1>Error: No text could be extracted from the PDF</h1>"

        # Generate flashcards using Gemini AI
        flashcards_json = generate_flashcards(text)
        if not flashcards_json:
            return f"<h1>Error: Failed to generate flashcards</h1>"

        # Parse the flashcards
        flashcards = parse_flashcards(flashcards_json)
        if not flashcards:
            return f"<h1>Error: No flashcards generated</h1>"

        # Save flashcards to the database (optional)
        flashcards_collection = db["flashcards"]
        flashcards_collection.insert_one({
            "pdf_id": ObjectId(pdf_id),
            "flashcards": flashcards
        })

        # Display the flashcards on a new page
        flashcards_html = "".join(
            f"<div class='flashcard'><div class='front'>{card['front']}</div><div class='back'>{card['back']}</div></div>"
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

# Flashcard generation HTML form
@app.get("/flashcard-form/", response_class=HTMLResponse)
def flashcard_form():
    """
    Serve an HTML form with a dropdown menu to select a PDF for flashcard generation.
    """
    try:
        # Fetch all PDFs from the database
        pdfs = collection.find({}, {"_id": 1, "name": 1})  # Only fetch `_id` and `name`
        options = ""
        for pdf in pdfs:
            options += f'<option value="{str(pdf["_id"])}">{pdf["name"]}</option>'

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

# View flashcards route
@app.get("/view-flashcards/", response_class=HTMLResponse)
def view_flashcards(pdf_id: str):
    """
    View flashcards for a specific PDF.
    """
    try:
        # Fetch flashcards from the database
        flashcards_collection = db["flashcards"]
        flashcards = flashcards_collection.find_one({"pdf_id": ObjectId(pdf_id)})
        if not flashcards:
            return f"<h1>Error: No flashcards found for this PDF</h1>"

        # Generate HTML for the flashcards
        flashcards_html = "".join(
            f"<div class='flashcard'><div class='front'>{card['front']}</div><div class='back'>{card['back']}</div></div>"
            for card in flashcards["flashcards"]
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
            <h1>Flashcards for PDF</h1>
            {flashcards_html}
            <br>
            <a href="/flashcard-form/">Generate Flashcards for Another PDF</a>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

# HTML form for downloading PDFs
@app.get("/download-form/", response_class=HTMLResponse)
def download_form():
    """
    Serve an HTML form with a dropdown menu to select a PDF for download.
    """
    try:
        # Fetch all PDFs from the database
        pdfs = collection.find({}, {"_id": 1, "name": 1})  # Only fetch `_id` and `name`
        options = ""
        for pdf in pdfs:
            options += f'<option value="{str(pdf["_id"])}">{pdf["name"]}</option>'

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

# Download PDF route
@app.get("/download-pdf/")
async def download_pdf(pdf_id: str):
    """
    Download a PDF file from the database by ID.
    """
    try:
        # Fetch the PDF from the database
        pdf = collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf:
            return {"error": "PDF not found"}

        # Stream the PDF content
        pdf_content = BytesIO(pdf["content"])
        response = StreamingResponse(pdf_content, media_type="application/pdf")
        response.headers["Content-Disposition"] = f"attachment; filename={pdf['filename']}"
        return response
    except Exception as e:
        return {"error": str(e)}

# HTML form for deleting PDFs
@app.get("/delete-form/", response_class=HTMLResponse)
def delete_form():
    """
    Serve an HTML form with a dropdown menu to select a PDF for deletion.
    """
    try:
        # Fetch all PDFs from the database
        pdfs = collection.find({}, {"_id": 1, "name": 1})  # Only fetch `_id` and `name`
        options = ""
        for pdf in pdfs:
            options += f'<option value="{str(pdf["_id"])}">{pdf["name"]}</option>'

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

# Delete PDF route
@app.post("/delete-pdf/")
async def delete_pdf(pdf_id: str = Form(...)):
    """
    Delete a PDF file from the MongoDB collection by ID.
    """
    try:
        # Delete the PDF from the database
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

# HTML form for viewing PDFs
@app.get("/view-form/", response_class=HTMLResponse)
def view_form():
    """
    Serve an HTML form with a dropdown menu to select a PDF for viewing.
    """
    try:
        # Fetch all PDFs from the database
        pdfs = collection.find({}, {"_id": 1, "name": 1})  # Only fetch `_id` and `name`
        options = ""
        for pdf in pdfs:
            options += f'<option value="{str(pdf["_id"])}">{pdf["name"]}</option>'

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

# View PDF route
@app.get("/view-pdf/")
async def view_pdf(pdf_id: str):
    """
    View a PDF file from the MongoDB collection by ID.
    """
    try:
        # Find the PDF in the database
        pdf = collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf:
            return {"error": "PDF not found"}

        # Create a streaming response for the PDF content
        pdf_content = BytesIO(pdf["content"])
        response = StreamingResponse(pdf_content, media_type="application/pdf")
        response.headers["Content-Disposition"] = f"inline; filename={pdf['filename']}"
        return response
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
