import React, { useState } from 'react';
import './index.css';


const Dropdown = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="dropdown">
      <button className="hamburger" onClick={toggleMenu}>
        ☰
      </button>
      {isOpen && <div className="overlay" onClick={toggleMenu}></div>}
      <div className={`side-navbar ${isOpen ? 'open' : ''}`}>
        <button className="close-btn" onClick={toggleMenu}>
          &times;
        </button>
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#services">Services</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </div>
    </div>
  );
};

export default Dropdown;