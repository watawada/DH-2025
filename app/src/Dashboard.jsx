import "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import React from "react";
import NavBar from "./components/NavBar.jsx";
import Section from "./components/Section";
import UserProfile from "./components/UserProfile/index.jsx";
import profileImage from "./assets/ryan.jpg";
import RecentPacks from "./components/RecentPacks/index.jsx";
import AllPacks from "./components/AllPacks/index.jsx";


function Dashboard() {
  
return (
    <>
      <NavBar />
      <UserProfile 
        name="John Doe" 
        username="jdoe123" 
        profilePicture={profileImage}
      />

      <RecentPacks />
      <AllPacks />
    </>

);
}

export default Dashboard;
