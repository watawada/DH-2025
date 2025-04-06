import "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import React from "react";
import NavBar from "./components/NavBar.jsx";
import HeroSection from "./components/Hero.jsx";
import Section from "./components/Section";

function App() {
  const aboutCards = [
    {
      title: "Powerful AI",
      description: "Leverage AI to enhance your learning.",
    },
    {
      title: "Easy to Use",
      description: "Upload files and get study materials instantly.",
    },
  ];

  const featureCards = [
    {
      title: "Flashcards",
      icon: <i className="bi bi-card-text"></i>,
      description: "Create flashcards easily.",
    },
    {
      title: "Quizzes",
      icon: <i className="bi bi-lightbulb"></i>,
      description: "Generate quizzes for practice.",
    },
  ];
  return (
    <>
      <NavBar/>

      <HeroSection />

      {/* About Section */}
      <Section heading="About" cards={aboutCards} />
      <Section heading="Features" cards={featureCards} />
    </>
  );
}

export default App;
