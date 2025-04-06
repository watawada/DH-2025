import "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import React from "react";
import NavBar from "./components/NavBar.jsx";
import Section from "./components/Section";
import UserProfile from "./components/UserProfile/index.jsx";
import profileImage from "./assets/ryan.jpg";


function Dashboard() {
  

  
return (
    <>
      <NavBar />
      <UserProfile 
        name="John Doe" 
        username="jdoe123" 
        profilePicture={profileImage}
      />
    </>
);
}

export default Dashboard;
