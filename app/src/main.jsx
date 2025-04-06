import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// import StudyPack from './StudyPack.jsx'
import 'bootstrap/dist/css/bootstrap.min.css'
import Home from './Home.jsx'
import Dashboard from './Dashboard.jsx'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App/>
  </StrictMode>,
)