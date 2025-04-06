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
      <NavBar />

      <HeroSection />

      {/* About Section */}
      <Section heading="About" cards={aboutCards} />
      <Section heading="Features" cards={featureCards} />
      <section className="about text-center py-5">
        <h2>About</h2>
        <div className="about-content mx-auto p-3 bg-light">
          <p>Power your learning with AI!</p>
          {/* <p>
            [Title] uses AI to create study materials from files you upload.
          </p> */}
        </div>
      </section>

      {/* Features Section */}
      <section className="features text-center py-5">
        <h2>Features</h2>
        <div className="row justify-content-center mt-4">
          <div className="col-md-4">
            <div className="feature-card p-3 bg-light">
              <h3>Flashcards</h3>
            </div>
          </div>
          <div className="col-md-4">
            <div className="feature-card p-3 bg-light">
              <h3>Quizzes</h3>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default App;
