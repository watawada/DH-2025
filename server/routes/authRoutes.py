# authRoutes.py - Updated version
from fastapi import APIRouter, Depends, HTTPException, status, Response
from auth import oauth
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from authlib.integrations.base_client import OAuthError
from os import environ as env
from auth import DOMAIN, CLIENT_ID, CLIENT_SECRET


REDIRECT_URI = "http://localhost:8000/auth/callback"
print(f"REDIRECT_URI: {REDIRECT_URI}")
router = APIRouter()

@router.get("/")
async def home():
    return {"message": "Welcome to FastAPI with Auth0 integration"}

@router.get("/login")
async def login(request: Request):

    # DEBUG: Log the redirect URI
    print(f"Redirecting to Auth0 with redirect_uri: {REDIRECT_URI}")

    # Redirect to Auth0 login page
    redirect_uri = REDIRECT_URI
    return await oauth.auth0.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def callback(request: Request):
    try:
        # Log the incoming request
        print(f"Callback request: {request.query_params}")
        
        # Retrieve the token
        token = await oauth.auth0.authorize_access_token(request)
        print(f"Token received: {token}")  # DEBUG: Log the token
        
        # Store tokens in session for potential future use
        request.session["access_token"] = token["access_token"]
        request.session["id_token"] = token["id_token"]
        
        # Redirect to a protected route or homepage
        return RedirectResponse(url="/")
    except Exception as e:
        # Log the error
        print(f"Error during callback: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"Could not authenticate: {str(e)}"}
        )

@router.get("/logout")
async def logout(request: Request, response: Response):
    # Clear session
    request.session.clear()
    
    # Redirect to Auth0 logout endpoint
    return_to = request.url_for("home")

    print(f"Logout returnTo URL: {return_to}")  # DEBUG: Log the returnTo URL

    logout_url = f"https://{DOMAIN}/v2/logout?client_id={CLIENT_ID}&returnTo={return_to}"

    print(f"Logout URL: {logout_url}")  # DEBUG: Log the full logout URL
    
    return RedirectResponse(url=logout_url)

@router.get("/protected")
async def protected(request: Request):
    try:
        # Check if the user is logged in by verifying the session
        user = request.session.get("id_token")
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated. Please log in."
            )
        
        # Return a success message if the user is authenticated
        return {"message": "You are logged in and can access this protected route."}
    except Exception as e:
        # Log the error and return an unauthorized response
        print(f"Protected route error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed."
        )
        
