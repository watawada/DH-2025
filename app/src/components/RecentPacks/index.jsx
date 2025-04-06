import React from "react";
import "./RecentPacks.css";

const RecentPacks = () => {
  const handleCardClick = (packName) => {
    alert(`You clicked on ${packName}`); // Replace this with navigation or other logic
  };

  return (
    <div className="recent-packs-container">
      <h2>Recent Packs</h2>
      <div className="card-container">
        <div
          className="card"
          onClick={() => handleCardClick("Pack 1")} // Make the card clickable
        >
          <h3>Pack 1</h3>
          <p>Description of Pack 1</p>
        </div>
        <div
          className="card"
          onClick={() => handleCardClick("Pack 2")} // Make the card clickable
        >
          <h3>Pack 2</h3>
          <p>Description of Pack 2</p>
        </div>
        <div
          className="card"
          onClick={() => handleCardClick("Pack 3")} // Make the card clickable
        >
          <h3>Pack 3</h3>
          <p>Description of Pack 3</p>
        </div>
      </div>
    </div>
  );
};

export default RecentPacks;