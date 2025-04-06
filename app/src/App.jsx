import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./Home.jsx";
import Dashboard from "./Dashboard.jsx";
import UploadForm from "./components/UploadForm.jsx";
import StartLearning from "./StartLearning.jsx";
import FlashcardsPage from "./FlashcardsPage.jsx";
import QuizPage from "./Quiz.jsx"; // Import the QuizPage

const App = () => {
  return (
    <Router>
      <div>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/upload" element={<UploadForm />} />
            <Route path="/start-learning" element={<StartLearning />} />
            <Route path="/flashcards" element={<FlashcardsPage />} />
            <Route path="/quiz" element={<QuizPage />} /> {/* Add this route */}
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;