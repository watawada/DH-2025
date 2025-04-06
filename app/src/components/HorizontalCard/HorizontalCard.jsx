import React from "react";
import "./HorizontalCard.css";

function HorizontalCard({ term, definition }) {
  return (
    <div className="horizontal-card d-flex">
      <div className="definition bg-light p-3 flex-grow-1">
        <h4 className="text-center fw-bold">{definition}</h4>
      </div>
      <div className="term bg-light text-black p-3 flex-grow-2">
        <h5 className="text-center">{term}</h5>
      </div>
    </div>
  );
}

export default HorizontalCard;