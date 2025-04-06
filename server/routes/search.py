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
    try:
        search_type = request.query_params.get("search_type", "folder")  # Default to folder search
        search_term = request.query_params.get("search_term", "")  # Get the search term
        
        collection = db["files"]
        query = {}
        
        if search_term:
            if search_type == "folder":
                query["folder"] = {"$regex": search_term, "$options": "i"}  # Case-insensitive search
            else:  # filename search
                query["filename"] = {"$regex": search_term, "$options": "i"}
                
        pdfs = collection.find(query, {"_id": 1, "name": 1, "filename": 1, "folder": 1})
        results = [{"id": str(pdf["_id"]), "name": pdf["name"], "filename": pdf["filename"], "folder": pdf["folder"]} for pdf in pdfs]
        
        table_rows = "".join(
            f"<tr><td>{pdf['name']}</td><td>{pdf['filename']}</td><td>{pdf['folder']}</td></tr>" for pdf in results
        ) if results else "<tr><td colspan='3'>No PDFs found</td></tr>"
        
        # Determine which option should be selected in the dropdown
        folder_selected = "selected" if search_type == "folder" else ""
        filename_selected = "selected" if search_type == "filename" else ""
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Search PDFs</title>
        </head>
        <body>
            <h1>Search PDFs</h1>
            <form action="/search-page/" method="get">
                <label for="search_type">Search by:</label>
                <select id="search_type" name="search_type">
                    <option value="folder" {folder_selected}>Folder</option>
                    <option value="filename" {filename_selected}>Filename</option>
                </select>
                
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
                    <th>Folder</th>
                </tr>
                {table_rows}
            </table>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"
    
    

