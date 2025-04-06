# auth.py - Updated version
import json
from os import environ as env
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from jose import jwt
import requests

DOMAIN = env.get("DOMAIN")
CLIENT_ID = env.get("CLIENT_ID")
CLIENT_SECRET = env.get("CLIENT_SECRET")
REDIRECT_URI = env.get("REDIRECT_URI")
SECRET_KEY = env.get("SECRET_KEY")
ALGORITHMS = ["RS256"]

oauth = OAuth()
oauth.register(
    name="auth0",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f"https://{DOMAIN}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email", "response_type": "code", "token_endpoint_auth_method": "client_secret_post"},
)

security = HTTPBearer()

# Cache the JWKS
jwks = None

def get_jwks():
    global jwks
    if not jwks:
        jwks_url = f"https://{DOMAIN}/.well-known/jwks.json"
        jwks = requests.get(jwks_url).json()
    return jwks

def verify_jwt(auth: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = auth.credentials
        jwks = get_jwks()
        
        # Parse the token header
        header = jwt.get_unverified_header(token)
        
        # Find the correct key
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        
        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=CLIENT_ID,
                issuer=f"https://{DOMAIN}/"
            )
            return payload
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {str(e)}")