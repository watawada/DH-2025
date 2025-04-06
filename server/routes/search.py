from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from fastapi.responses import HTMLResponse
from database import get_db

router = APIRouter()

@router.get("/search-page/", response_class=HTMLResponse)
def search_page(db: Database = Depends(get_db), request: Request = None):
    """
    Serve a search page that displays all PDFs with the option to filter by folder or filename.
    """
    if not request.session:
        return {"error": "Cannot access search. Not authenticated"}

    try:
        # Get the current user's email and fetch their document
        user = db["users"].find_one({"email": request.session["user_email"]})
        if not user or "files" not in user:
            return {"error": "No files found for the user"}

        # Get the search term
        search_term = request.query_params.get("search_term", "").lower()

        # Fetch all files belonging to the user
        file_ids = user["files"]
        files = db["files"].find({"_id": {"$in": file_ids}})

        # Filter files based on the search term
        results = [
            file for file in files
            if not search_term or search_term in file.get("filename", "").lower()
        ]

        # Generate table rows for the results
        table_rows = "".join(
            f"<tr><td>{file.get('name', '')}</td><td>{file.get('filename', '')}</td></tr>"
            for file in results
        ) if results else "<tr><td colspan='2'>No PDFs found</td></tr>"

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Search PDFs</title>
        </head>
        <body>
            <h1>Search PDFs</h1>
            <form action="/search-page/" method="get">
                <label for="search_term">Search term:</label>
                <input type="text" id="search_term" name="search_term" value="{search_term}" placeholder="Enter search term">
                <button type="submit">Search</button>
            </form>
            <br>
            <h2>Uploaded PDFs</h2>
            <table border="1">
                <tr>
                    <th>Name</th>
                    <th>Filename</th>
                </tr>
                {table_rows}
            </table>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"