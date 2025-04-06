import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import NavBar from "./components/NavBar.jsx";
import Flashcard from "./components/Flashcard/Flashcard.jsx";
import connection from "./backend"; // Axios instance for backend communication

function FlashcardsPage() {
  const location = useLocation();
  const { pdfId } = location.state || {}; // Retrieve the PDF ID from the state
  const [flashcards, setFlashcards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFlashcards = async () => {
      try {
        const formData = new FormData(); // Create FormData to send as form data
        formData.append("pdf_id", pdfId); // Append the pdf_id

        const response = await connection.post("/generate-flashcards/", formData, {
          headers: {
            "Content-Type": "multipart/form-data", // Set the correct content type
          },
        }); // Call the backend route to generate flashcards

        console.log("Flashcards fetched:", response.data.flashcards); // Debugging log
        setFlashcards(response.data.flashcards || []); // Set flashcards or empty array
      } catch (err) {
        console.error("Error fetching flashcards:", err);
        setError("Failed to load flashcards. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    if (pdfId) {
      fetchFlashcards();
    } else {
      setError("No PDF selected. Please upload a PDF first.");
      setLoading(false);
    }
  }, [pdfId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!Array.isArray(flashcards) || flashcards.length === 0) {
    return <div>No flashcards available. Please try again.</div>;
  }

  return (
    <>
      <NavBar />
      <div className="container mt-4">
        <h1>Flashcards</h1>
        <div className="row justify-content-center">
          {flashcards.map((card, index) => (
            <div key={index} className="col-12 col-md-8 mb-5">
              <Flashcard term={card.front} definition={card.back} />
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default FlashcardsPage;
