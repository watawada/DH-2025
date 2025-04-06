import React, { useState } from 'react';
import { Link } from 'react-router-dom'; 
// import Dashboard from '../../Dashboard.jsx';
// import App from '../../App.jsx';


// goDashboard(document.getElementById('root')).render(
//   <StrictMode>
//     <Dashboard/>
//   </StrictMode>,
// )

// goHome(document.getElementById('root')).render(
//   <StrictMode>
//     <App/>
//   </StrictMode>,
// )

const Dropdown = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  // <Routes>
  
  //   <Route path="/dashboard" element={<Dashboard />} />
  //   {/* <Route path="/contact" element={<Contact />} /> */}
  // </Routes>

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
          {/* <li><a onClick={goHome()}>Home</a></li>
          <li><a onClick={goDashboard()}>Dashboard</a></li> */}
          <li><Link to="/">Home</Link></li>    {/* Link to Home */}
          <li><Link to="/dashboard">Dashboard</Link></li>  {/* Link to About */}
        </ul>
      </div>
    </div>
  );
};

export default Dropdown;