from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.search import router as search_router
from routes.flashcards import router as flashcards_router
from routes.download import router as download_router
from routes.delete import router as delete_router
from routes.view import router as view_router
from routes.reviewquiz import router as reviewquiz_router
import logging

app = FastAPI()

# Include routers
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(flashcards_router)
app.include_router(download_router)
app.include_router(delete_router)
app.include_router(view_router)
app.include_router(reviewquiz_router)

# Base route for testing
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}