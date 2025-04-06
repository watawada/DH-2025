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
      <UserProfile name="John Doe" username="jdoe123"/>
    </>
);
}

export default Dashboard;
