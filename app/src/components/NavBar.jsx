import React from "react";
import { Link } from "react-router-dom";

function NavBar() {
  const handleLogin = () => {
    window.location.href = "http://localhost:8000/auth/login"; // Redirect to backend login
  };

  const handleSignup = () => {
    window.location.href = "http://localhost:8000/auth/login"; // Redirect to backend signup (same as login for now)
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          Home
        </Link>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <Link className="nav-link" to="/dashboard">
                Dashboard
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/upload">
                Upload PDF
              </Link>
            </li>
          </ul>
          <div className="ms-auto">
            <button
              className="btn btn-outline-primary me-2"
              onClick={handleLogin}
            >
              Login
            </button>
            <button
              className="btn btn-primary"
              onClick={handleSignup}
            >
              Signup
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;