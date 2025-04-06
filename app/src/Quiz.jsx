import "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import React from "react";
import NavBar from "./components/NavBar.jsx";
import QuizForm from "./components/QuizForm.jsx";

function QuizPage() {
  const questions = [
    {
      question: "What is the capital of France?",
      options: ["Paris", "London", "Berlin", "Madrid"],
    },
    {
      question: "Which planet is known as the Red Planet?",
      options: ["Earth", "Mars", "Jupiter", "Venus"],
    },
    {
      question: "What is the largest ocean on Earth?",
      options: ["Atlantic", "Indian", "Arctic", "Pacific"],
    },
    {
      question: "Who wrote 'Romeo and Juliet'?",
      options: ["Shakespeare", "Hemingway", "Tolkien", "Austen"],
    },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Quiz submitted!");
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
            {questions.map((q, index) => (
              <div key={index} className="col-12 col-md-8 mb-5">
                <QuizForm
                  question={q.question}
                  options={q.options}
                  questionIndex={index}
                />
              </div>
            ))}
          </div>
          <div className="text-center">
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
