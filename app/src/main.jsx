import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import FlashcardPage from "./Flashcard.jsx";
import "bootstrap/dist/css/bootstrap.min.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <FlashcardPage />
  </StrictMode>
);
