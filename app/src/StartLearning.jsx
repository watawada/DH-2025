import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import NavBar from "./components/NavBar.jsx"; // Import the NavBar component
import connection from "./backend"; // Import Axios instance

function StartLearning() {
  const navigate = useNavigate();
  const location = useLocation();
  const { pdfId } = location.state || {}; // Retrieve the PDF ID from the state

  const handleFlashcards = async () => {
    if (!pdfId) {
      alert("No PDF selected. Please upload a PDF first.");
    }

    try {
        const formData = new FormData();
        formData.append("pdf_id", pdfId);

        const res = await connection.post("generate-flashcards/", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
            }
        );
        const flashcards = res.data.flashcards;
        if (flashcards) {
            navigate("/flashcards", { state: { pdfId } }); // Pass the PDF ID to the Flashcards page
          } else {
            alert("Failed to generate flashcards. Please try again.");
        }
    } catch (err) {
        console.error("Error generating flashcards:", err);
        alert("Failed to generate flashcards. Please try again.");
    }
    
  
  };

  const handleQuiz = async () => {
    if (!pdfId) {
      alert("No PDF selected. Please upload a PDF first.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("pdf_id", pdfId);

      // Call the backend to generate the quiz
      const response = await connection.post("/generate-reviewquiz/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const quiz = response.data.quiz; // Get the quiz data from the response
      if (quiz) {
        navigate("/quiz", { state: { quiz } }); // Pass the quiz data to the QuizPage
      } else {
        alert("Failed to generate quiz. Please try again.");
      }
    } catch (err) {
      console.error("Error generating quiz:", err);
      alert("Failed to generate quiz. Please try again.");
    }
  };

  return (
    <>
      <NavBar />
      <div className="container text-center mt-5">
        <h1>Start Learning</h1>
        <div className="d-flex justify-content-center mt-4">
          <button className="btn btn-primary me-3" onClick={handleFlashcards}>
            Flashcards
          </button>
          <button className="btn btn-secondary" onClick={handleQuiz}>
            Quiz
          </button>
        </div>
      </div>
    </>
  );
}

export default StartLearning;