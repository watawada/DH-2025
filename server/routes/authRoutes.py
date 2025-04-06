# authRoutes.py - Updated version
from fastapi import APIRouter, Depends, HTTPException, status, Response
from auth import oauth
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from authlib.integrations.base_client import OAuthError
from os import environ as env
from auth import get_current_user, DOMAIN, CLIENT_ID, CLIENT_SECRET
from typing import Dict, Any

REDIRECT_URI = "http://localhost:8000/auth/callback"
print(f"REDIRECT_URI: {REDIRECT_URI}")
router = APIRouter()

@router.get("/")
async def home():
    return {"message": "Welcome to FastAPI with Auth0 integration"}

@router.get("/login")
async def login(request: Request):
    # Redirect to Auth0 login page
    redirect_uri = REDIRECT_URI
    return await oauth.auth0.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def callback(request: Request):
    # Handle callback from Auth0
    try:
        token = await oauth.auth0.authorize_access_token(request)
        
        # Get user info from userinfo endpoint
        user_info = await oauth.auth0.parse_id_token(request, token)
        request.session["user"] = dict(user_info)
        
        # Store tokens in session for potential future use
        request.session["access_token"] = token.get("access_token")
        request.session["id_token"] = token.get("id_token")
        
        # Redirect to a protected route or homepage
        return RedirectResponse(url="/profile")
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"Could not authenticate: {str(e)}"}
        )

@router.get("/profile")
async def profile(user: Dict = Depends(get_current_user)):
    # Protected route example
    return {
        "message": "You are authenticated!",
        "user": user
    }

@router.get("/logout")
async def logout(request: Request, response: Response):
    # Clear session
    request.session.clear()
    
    # Redirect to Auth0 logout endpoint
    return_to = request.url_for("home")
    logout_url = f"https://{DOMAIN}/v2/logout?client_id={CLIENT_ID}&returnTo={return_to}"
    
    return RedirectResponse(url=logout_url)

@router.get("/api/protected")
async def protected_api(user: Dict = Depends(get_current_user)):
    # Example protected API endpoint
    return {"message": "This is a protected API route", "user_id": user.get("sub")}
