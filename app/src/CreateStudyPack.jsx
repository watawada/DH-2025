import React, { useState } from "react";
import "./Styles.css";
import NavBar from "./components/NavBar.jsx";

function CreateStudyPack() {
  const [studyPackName, setStudyPackName] = useState("");
  const [coverImage, setCoverImage] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission logic here
    console.log("Study Pack Name:", studyPackName);
    console.log("Cover Image:", coverImage);
    console.log("PDF File:", pdfFile);
    alert("Study Pack Created!");
  };

  return (
    <>
      <NavBar />
      <div className="container mt-4">
        <h1 className="mb-4">Create a New Study Pack</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="studyPackName" className="form-label">
              Name of Study Pack
            </label>
            <input
              type="text"
              className="form-control"
              id="studyPackName"
              placeholder="Enter study pack name"
              value={studyPackName}
              onChange={(e) => setStudyPackName(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="coverImage" className="form-label">
              Study Pack Cover Image
            </label>
            <input
              type="file"
              className="form-control"
              id="coverImage"
              accept="image/png" // Only accept PNG files
              onChange={(e) => setCoverImage(e.target.files[0])}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="pdfFile" className="form-label">
              Upload PDFs
            </label>
            <input
              type="file"
              className="form-control"
              id="pdfFile"
              accept=".pdf"
              onChange={(e) => setPdfFile(e.target.files[0])}
              required
            />
          </div>
          <button type="submit" className="btn btn-success">
            + Create Study Pack
          </button>
        </form>
      </div>
    </>
  );
}

export default CreateStudyPack;
