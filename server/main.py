# main.py - Updated version
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.authRoutes import router
from starlette.middleware.sessions import SessionMiddleware
from auth import SECRET_KEY

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=3600,
    same_site="lax"
)

app.include_router(router, prefix="/auth", tags=["auth"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)