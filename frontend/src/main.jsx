import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import "leaflet/dist/leaflet.css";
import { Toaster } from "react-hot-toast";

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Toaster position="top-right" />
    <App />
  </StrictMode>,
  
)
