from fastapi import APIRouter, Depends
from pymongo.database import Database
from bson.objectid import ObjectId
from database import get_db

router = APIRouter()

@router.post("/fetch-pdfs")
async def fetch_pdfs(pdfIds: list[str], db: Database = Depends(get_db)):
    """
    Fetch PDF details based on the provided IDs.
    """
    try:
        collection = db["files"]
        pdfs = collection.find({"_id": {"$in": [ObjectId(pdfId) for pdfId in pdfIds]}})
        return {"pdfs": list(pdfs)}
    except Exception as e:
        return {"error": str(e)}