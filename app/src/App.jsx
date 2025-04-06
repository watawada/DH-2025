import logo from "./assets/logo.svg";
import "./Styles.css";
import 'bootstrap-icons/font/bootstrap-icons.css';


function App() {
  return (
    <>
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg bg-dark navbar-dark">
        <div className="container-fluid">
          <a className="navbar-brand d-flex align-items-center" href="#">
            <img
              src={logo}
              alt="Brand Logo"
              width="30"
              height="30"
              className="me-2"
            />
            <span>Brand Name</span>
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <div className="ms-auto">
              <button className="btn btn-outline-light me-2 login-btn" type="button">
                Login
              </button>
              <button className="btn btn-light signup-btn" type="button">
                Signup
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero text-center hero-padding bg-light">
        <h1 className="display-4">Study Buddy</h1>
        <button className="btn btn-secondary mt-3">Start Learning</button>
      </section>

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
