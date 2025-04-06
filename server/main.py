# main.py - Updated version
from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.search import router as search_router
from routes.flashcards import router as flashcards_router
from routes.download import router as download_router
from routes.delete import router as delete_router
from routes.view import router as view_router
from routes.reviewquiz import router as reviewquiz_router
from routes.userRoute import router as user_router
import logging
from fastapi.middleware.cors import CORSMiddleware
from routes.authRoutes import router
from starlette.middleware.sessions import SessionMiddleware
from auth import SECRET_KEY

app = FastAPI()

# Include routers
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(flashcards_router)
app.include_router(download_router)
app.include_router(delete_router)
app.include_router(view_router)
app.include_router(reviewquiz_router)
app.include_router(user_router, prefix="/user", tags=["user"])


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

@app.get("/")
def root():
    return {"message": "THIS IS THE HOME PAGE"}

app.include_router(router, prefix="/auth", tags=["auth"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
