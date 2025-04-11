from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import JSONResponse
from pymongo.database import Database
from database import get_db

router = APIRouter()

@router.get("/self")
async def self(request: Request, db: Database = Depends(get_db)):
    if not request.session:
        return JSONResponse(
            status_code = 401,
            content = {"message": "Unauthorized"}
        )
    
    try:
        user = db["users"].find_one({"email": request.session["user_email"]})
        
        if not user:
            return JSONResponse(
                status_code = 404,
                content = {"message": "User not found"}
            )
        userResponse = {
            "_id": str(user["_id"]),
            "picture": user["picture"],
            "email": user["email"],
        }

        return JSONResponse(content = userResponse)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content = {"message": "Internal Server Error", "error":str(e)}
        )
