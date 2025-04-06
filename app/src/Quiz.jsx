import "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import NavBar from "./components/NavBar.jsx";
import QuizForm from "./components/QuizForm.jsx";

function QuizPage() {
  const location = useLocation();
  const { quiz } = location.state || {}; // Retrieve the quiz data from the state
  const [feedback, setFeedback] = useState([]); // State to store feedback for each question

  if (!quiz) {
    return <div>No quiz data available. Please try again.</div>;
  }

  const handleSubmit = (e) => {
    e.preventDefault();
  
    const newFeedback = quiz.map((q, index) => {
      const selectedOption = document.querySelector(
        `input[name="question-${index}"]:checked`
      );
  
      if (!selectedOption) {
        return { correct: false, message: "No answer selected." };
      }
  
      const userAnswer = selectedOption.value; // User's selected answer
      const correctAnswer = q.correct; // Correct answer from the quiz data
  
      // Normalize both answers for comparison
      const isCorrect =
        String(userAnswer).trim().toLowerCase() ===
        String(correctAnswer).trim().toLowerCase();
  
      return {
        correct: isCorrect,
        message: isCorrect
          ? "Correct! The answer is: " + correctAnswer
          : `Incorrect. The correct answer is: ${correctAnswer}`,
      };
    });
  
    setFeedback(newFeedback); // Update feedback state dynamically
  };

  return (
    <>
      <NavBar />
      <div className="container mt-4">
        <div className="mb-4">
          <div className="d-flex align-items-center mb-3">
            <h1 className="me-2">Quiz</h1>
          </div>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="row justify-content-center">
            {quiz.map((q, index) => (
              <div key={index} className="col-12 col-md-8 mb-5">
                <QuizForm
                  question={q.question}
                  options={q.choices}
                  questionIndex={index}
                />
                {/* Display feedback under each question */}
                {feedback[index] && (
                  <p
                    className={`mt-2 ${
                      feedback[index].correct ? "text-success" : "text-danger"
                    }`}
                  >
                    {feedback[index].message}
                  </p>
                )}
              </div>
            ))}
          </div>
          <div className="text-center mb-5">
            <button type="submit" className="btn btn-success mt-4">
              Submit Quiz
            </button>
          </div>
        </form>
      </div>
    </>
  );
}

export default QuizPage;