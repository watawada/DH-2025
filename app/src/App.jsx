import React from 'react';
import Dropdown from './components/Dropdown/index.jsx';  // Import the Navbar
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home.jsx';      // Import the Home page
import Dashboard from './Dashboard.jsx';    // Import the About page

const App = () => {
  return (
    <Router>
      <div>
        <main>
          <Routes>
            <Route path="/" element={<Home />} /> {/* Home route */}
            <Route path="/dashboard" element={<Dashboard />} /> {/* Dashboard route */}
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
