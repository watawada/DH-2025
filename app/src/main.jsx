import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import QuizPage from "./Quiz.jsx";
import "bootstrap/dist/css/bootstrap.min.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <QuizPage />
  </StrictMode>
);
