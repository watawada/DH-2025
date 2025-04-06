import "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import NavBar from "./components/NavBar.jsx";
import HeroSection from "./components/Hero.jsx";

function App() {
  return (
    <>
      {/* Navbar */}
      <NavBar/>

      {/* Hero Section */}
      <HeroSection/>

      {/* About Section */}
      <section className="about text-center py-5">
        <h2>About</h2>
        <div className="about-content mx-auto p-3 bg-light">
          <p>Power your learning with AI!</p>
          <p>
            [Title] uses AI to create study materials from files you upload.
          </p>
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
