import "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import React from "react";
import NavBar from "./components/NavBar.jsx";
import Flashcard from "./components/Flashcard/Flashcard.jsx";

function FlashcardPage() {
  const cards = [
    { term: "Term 1", definition: "Definition 1" },
    { term: "Term 2", definition: "Definition 2" },
    { term: "Term 3", definition: "Definition 3" },
    { term: "Term 4", definition: "Definition 4" },
  ];

  return (
    <>
      <NavBar />
      <div className="container mt-4">
      <div className="mb-4">
          <div className="d-flex align-items-center mb-3">
            <h1 className="me-2">Title of Study Pack</h1>
          </div>
        </div>
        <div className="row justify-content-center">
          {cards.map((card, index) => (
            <div key={index} className="col-12 col-md-8 mb-5">
              <Flashcard term={card.term} definition={card.definition} />
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default FlashcardPage;
