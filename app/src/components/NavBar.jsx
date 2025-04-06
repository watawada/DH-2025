import logo from "../assets/logo.svg";
import Dropdown from "./Dropdown";

function NavBar() {
  return (
    <nav className="navbar navbar-expand-lg bg-dark navbar-dark">
      <div className="container-fluid">
        <div className="navbar-brand d-flex align-items-center">
          <Dropdown/>
          <img
            src={logo}
            alt="Brand Logo"
            width="30"
            height="30"
            className="me-2" // Increased margin class
          />
          <span>Brand Name</span>
        </div>
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
            <button
              className="btn btn-outline-light me-2 login-btn"
              type="button"
            >
              Login
            </button>
            <button className="btn btn-light signup-btn" type="button">
              Signup
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
