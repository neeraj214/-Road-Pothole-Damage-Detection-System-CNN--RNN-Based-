import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './output.css'

try {
  const stored = localStorage.getItem('roadsight_history')
  if (stored && stored.length > 4 * 1024 * 1024) {
    localStorage.removeItem('roadsight_history')
    console.log('Cleared oversized history')
  }
} catch (e) {
  localStorage.removeItem('roadsight_history')
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
