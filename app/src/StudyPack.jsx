import "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import React from "react";
import NavBar from "./components/NavBar.jsx";
import Flashcard from "./components/Flashcard/Flashcard.jsx";

function StudyPack() {
  const flashcards = [
    { term: "Term 1", definition: "Definition 1" },
    { term: "Term 2", definition: "Definition 2" },
    { term: "Term 3", definition: "Definition 3" },
    { term: "Term 4", definition: "Definition 4" },
  ];

  return (
    <>
      <NavBar />
      <div className="container mt-4">
        {/* Title and Buttons */}
        <div className="mb-4">
          <div className="d-flex align-items-center mb-3">
            <h1 className="me-2">Title of Study Pack</h1>
            <i className="bi bi-pencil-fill" style={{ cursor: "pointer", fontSize: "1.5rem"}}></i>
          </div>
          <div className="d-flex">
            <button className="btn btn-success me-2">Flashcards</button>
            <button className="btn btn-success">Quiz</button>
          </div>
        </div>

        {/* Flashcards Grid */}
        <div className="row">
          {flashcards.map((card, index) => (
            <div key={index} className="col-12 mb-4">
              <Flashcard term={card.term} definition={card.definition} />
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default StudyPack;
