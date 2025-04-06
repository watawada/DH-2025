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
          onClick={() => handleCardClick("Chemistry")} // Make the card clickable
        >
          <h3>Chemistry</h3>
          <p>Experiments🧪</p>
        </div>
        <div
          className="card"
          onClick={() => handleCardClick("Computer Science")} // Make the card clickable
        >
          <h3>Computer Science</h3>
          <p>Machining💻</p>
        </div>
        <div
          className="card"
          onClick={() => handleCardClick("Art")} // Make the card clickable
        >
          <h3>Art</h3>
          <p>Creativity🖌️</p>
        </div>
      </div>
    </div>
  );
};

export default RecentPacks;