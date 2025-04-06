import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import CreateStudyPack from "./CreateStudyPack.jsx";
import "bootstrap/dist/css/bootstrap.min.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <CreateStudyPack />
  </StrictMode>
);
