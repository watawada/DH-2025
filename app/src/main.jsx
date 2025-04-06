import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import StudyPack from './StudyPack.jsx'
import 'bootstrap/dist/css/bootstrap.min.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <StudyPack/>
  </StrictMode>,
)

