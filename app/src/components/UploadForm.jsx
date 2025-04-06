import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate for navigation
import connection from "../backend"; // Import Axios instance
import NavBar from "./NavBar.jsx"; // Import the NavBar component

function UploadForm() {
  const [pdfName, setPdfName] = useState(""); // For the PDF name
  const [pdfFile, setPdfFile] = useState(null); // For the PDF file
  const [message, setMessage] = useState(""); // For success/error messages
  const [isUploaded, setIsUploaded] = useState(false); // Track if a PDF has been uploaded
  const [pdfId, setPdfId] = useState(""); // Store the uploaded PDF ID
  const navigate = useNavigate(); // Initialize navigation

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the page from refreshing

    if (!pdfFile) {
      alert("Please select a PDF file to upload."); // Show an alert if no file is selected
      return;
    }

    const formData = new FormData(); // Create a form to send to the backend
    formData.append("name", pdfName); // Add the PDF name
    formData.append("file", pdfFile); // Add the PDF file

    try {
      const response = await connection.post("/upload-pdf/", formData, {
        headers: {
          "Content-Type": "multipart/form-data", // Tell the backend we're sending a file
        },
      });
      setMessage(response.data.message || "PDF uploaded successfully!"); // Show success message
      setIsUploaded(true); // Mark as uploaded
      setPdfId(response.data.pdf_id); // Store the uploaded PDF ID
    } catch (err) {
      console.error("Error uploading PDF:", err); // Log the error
      setMessage("Failed to upload PDF. Please try again."); // Show error message
    }
  };

  const handleStartLearning = () => {
    if (isUploaded) {
      navigate("/start-learning", { state: { pdfId } }); // Pass the PDF ID to the new page
    } else {
      alert("Please upload a PDF before starting!"); // Alert if no PDF is uploaded
    }
  };

  return (
    <>
      <NavBar /> {/* Add the NavBar component */}
      <div className="container mt-4">
        <h1>Upload a PDF</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="pdfName" className="form-label">
              PDF Name:
            </label>
            <input
              type="text"
              className="form-control"
              id="pdfName"
              value={pdfName}
              onChange={(e) => setPdfName(e.target.value)} // Update the PDF name
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="pdfFile" className="form-label">
              Choose PDF:
            </label>
            <input
              type="file"
              className="form-control"
              id="pdfFile"
              accept="application/pdf" // Only allow PDF files
              onChange={(e) => setPdfFile(e.target.files[0])} // Update the PDF file
              required
            />
          </div>
          <div className="d-flex">
            <button type="submit" className="btn btn-primary me-2">
              Upload
            </button>
            <button
              type="button"
              className="btn btn-success"
              onClick={handleStartLearning}
            >
              Start Learning
            </button>
          </div>
        </form>
        {message && <p className="mt-3">{message}</p>} {/* Show success/error message */}
      </div>
    </>
  );
}

export default UploadForm;