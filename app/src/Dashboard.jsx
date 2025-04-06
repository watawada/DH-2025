import "./Styles.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import React, { useEffect, useState } from "react";
import NavBar from "./components/NavBar.jsx";
import UserProfile from "./components/UserProfile/index.jsx";
import RecentPacks from "./components/RecentPacks/index.jsx";
import AllPacks from "./components/AllPacks/index.jsx";
import connection from "./backend"; // Import Axios instance
import profileImage from "./assets/ryan.jpg";

function Dashboard() {
  const [user, setUser] = useState(null); // State to store user data
  const [loading, setLoading] = useState(true); // State to handle loading
  const [error, setError] = useState(null); // State to handle errors


  
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await connection.get("/user/self");
        console.log("User data fetched:", response.data); // Debug: Log the response
        setUser(response.data); // Set user data if session is valid
      } catch (err) {
        console.error("Error fetching user data:", err);
        setError("Failed to fetch user data. Please log in.");
      } finally {
        setLoading(false); // Stop loading after the request
      }
    };
  
    fetchUserData();
  }, []);

  console.log("User at render time:", user);
  if (loading) {
    return <div>Loading...</div>; // Show a loading message while fetching data
  }

  if (error) {
    return <div>{error}</div>; // Show an error message if fetching fails
  }

  return (
    <div key={user?._id || "default"}>
      <NavBar />
      <UserProfile
        name={user?.email || "john@doe.com"}
        profilePicture={user?.picture || profileImage}
      />
      <RecentPacks />
      <AllPacks />
    </div>
  );
}

export default Dashboard;

