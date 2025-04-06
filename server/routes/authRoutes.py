# authRoutes.py - Updated version
from fastapi import APIRouter, Depends, HTTPException, status
from auth import oauth, verify_jwt
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from authlib.integrations.base_client import OAuthError
from os import environ as env

REDIRECT_URI = "http://localhost:8000/auth/callback"
print(f"REDIRECT_URI: {REDIRECT_URI}")
router = APIRouter()

@router.get("/")
def public():
    return {"message": "public route"}

@router.get("/login")
async def login(request: Request):
    try:
        # Verify a session exists and can be written to
        request.session["auth_test"] = "test_value"
        
        # Clear any previous OAuth state
        for key in list(request.session.keys()):
            if key.startswith("_auth0_"):
                del request.session[key]
        
        redirect_uri = REDIRECT_URI
        if not redirect_uri:
            raise HTTPException(status_code=500, detail="Missing redirect URI configuration")
        
        return await oauth.auth0.authorize_redirect(request, redirect_uri=redirect_uri)
    except Exception as e:
        print(f"Login error: {str(e)}")
        return {"error": f"Login failed: {str(e)}"}
    
@router.get("/callback")
async def callback(request: Request):
    try:
        token = await oauth.auth0.authorize_access_token(request)
        user_info = await oauth.auth0.parse_id_token(request, token)
        request.session["user"] = dict(user_info)
        request.session["token"] = token.get('access_token')
        return RedirectResponse(url="/")
    except Exception as e:
        print(f"Callback error details: {str(e)}")
        return {"error": f"Callback failed: {str(e)}"}
    
@router.get("/private")
def private(user: dict = Depends(verify_jwt)):
    return {"message": "private route", "user": user}

