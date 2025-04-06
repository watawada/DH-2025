import React, { useState } from "react";
import "./Flashcard.css";
import "bootstrap/dist/css/bootstrap.min.css";

function Flashcard({ term = "No term provided", definition = "No definition provided" }) {
  const [flipped, setFlipped] = useState(false);

  const handleFlip = () => {
    setFlipped(!flipped);
  };

  return (
    <div
      className={`flashcard ${flipped ? "flipped" : ""}`}
      onClick={handleFlip}
    >
      <div className="flashcard-inner">
        <div className="flashcard-front d-flex justify-content-center align-items-center">
          <h3 className="text-center fw-bold">{term}</h3>
        </div>
        <div className="flashcard-back d-flex justify-content-center align-items-center">
          <h3 className="text-center fw-bold">{definition}</h3>
        </div>
      </div>
    </div>
  );
}

export default Flashcard;
