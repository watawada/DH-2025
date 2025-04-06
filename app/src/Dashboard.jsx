import "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import React from "react";
import NavBar from "./components/NavBar.jsx";
import Section from "./components/Section";
import UserProfile from "./components/UserProfile/index.jsx";


function Dashboard() {
  

  
  return (
    <>
      <NavBar/>
      <UserProfile/>

    </>
  );
}

export default Dashboardimport "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import React from "react";
import NavBar from "./components/NavBar.jsx";
import HeroSection from "./components/Hero.jsx";
import Section from "./components/Section";
import Dropdown from "./components/Dropdown";

function Dashboard() {
  return (
    <>
      <NavBar />
      <HeroSection />
    </>
  );
}

export default App;
