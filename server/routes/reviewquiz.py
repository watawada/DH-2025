from fastapi import APIRouter, Form, Depends
from pymongo.database import Database
from bson.objectid import ObjectId
from fastapi.responses import HTMLResponse
from io import BytesIO
from PDF_reader import extract_text_from_pdf, generate_response, parse_reviewquiz
from database import get_db
from fastapi import Request

router = APIRouter()

@router.post("/generate-reviewquiz/")
async def generate_reviewquiz_route(pdf_id: str = Form(...), db: Database = Depends(get_db)):
    """
    Generate a review quiz for the selected PDF and return it in the response.
    """
    try:
        collection = db["files"]
        pdf = collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf:
            return {"error": "PDF not found"}

        pdf_content = BytesIO(pdf["content"])
        text = extract_text_from_pdf(pdf_content)

        if not text:
            return {"error": "No text could be extracted from the PDF"}

        # Generate quiz using Gemini
        prompt = (
            "Create a review quiz based on the following text. "
            "Each question should have 4 multiple-choice answers, with one correct answer. "
            "Format the response as JSON, like this:\n\n"
            "[{\"question\": \"What is X?\", \"choices\": [\"A\", \"B\", \"C\", \"D\"], \"correct\": \"A\"}, ...]\n\n"
        )
        quiz_json = generate_response(text, prompt)

        if not quiz_json:
            return {"error": "Failed to generate quiz"}

        # Parse the quiz JSON
        quiz = parse_reviewquiz(quiz_json)

        if not quiz:
            return {"error": "No quiz generated"}

        return {"quiz": quiz}  # Return the generated quiz directly
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/reviewquiz-form/", response_class=HTMLResponse)
async def reviewquiz_form_route(db: Database = Depends(get_db)):
    """
    Serve a form to select a PDF for generating a review quiz.
    """
    try:
        # Fetch all PDFs from the database
        collection = db["files"]
        pdfs = collection.find()

        # Generate a dropdown for available PDFs
        options_html = "".join(
            f"<option value='{str(pdf['_id'])}'>{pdf['name']}</option>"
            for pdf in pdfs
        )

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Generate Review Quiz</title>
        </head>
        <body>
            <h1>Select a PDF to Generate a Review Quiz</h1>
            <form action="/generate-reviewquiz/" method="post">
                <label for="pdf_id">Select PDF:</label>
                <select name="pdf_id" id="pdf_id" required>
                    {options_html}
                </select>
                <br><br>
                <button type="submit">Generate Review Quiz</button>
            </form>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

@router.post("/submit-quiz/", response_class=HTMLResponse)
async def submit_quiz_route(request: Request, db: Database = Depends(get_db)):
    """
    Handle the submitted quiz and provide feedback on the answers.
    """
    try:
        # Parse form data
        form_data = await request.form()
        pdf_id = form_data.get("pdf_id")
        if not pdf_id:
            return "<h1>Error: Missing PDF ID</h1>"

        # Fetch the quiz from the database
        quizzes_collection = db["quizzes"]
        quiz = quizzes_collection.find_one({"pdf_id": ObjectId(pdf_id)})

        if not quiz:
            return "<h1>Error: Quiz not found</h1>"

        quiz_questions = quiz["quiz"]

        # Generate feedback for each question
        feedback_html = ""
        for i, question in enumerate(quiz_questions):
            user_answer = form_data.get(str(i))
            correct_answer = question["correct"]

            if user_answer == correct_answer:
                feedback_html += f"<div class='question'><p>{question['question']}</p>"
                feedback_html += f"<p style='color: green;'>Correct! The answer is: {correct_answer}</p></div><br>"
            else:
                feedback_html += f"<div class='question'><p>{question['question']}</p>"
                feedback_html += f"<p style='color: red;'>Incorrect. Your answer: {user_answer}. The correct answer is: {correct_answer}</p></div><br>"

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Quiz Results</title>
            <style>
                .question {{ margin-bottom: 20px; }}
                .correct {{ color: green; }}
                .incorrect {{ color: red; }}
            </style>
        </head>
        <body>
            <h1>Quiz Results for PDF: {pdf_id}</h1>
            {feedback_html}
            <br>
            <a href="/reviewquiz-form/">Take Another Quiz</a>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"
