import './App.css'
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import StoryLoader from "./components/StoryLoader"
import StoryGenerator from "./components/StoryGenerator"
import ThemeProvider, { useTheme } from "./components/ThemeProvider"
import { useEffect } from 'react'

function App() {
  const { isDarkMode, toggleTheme } = useTheme()

  useEffect(() => {
    // Set initial theme based on user preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    if (prefersDark) {
      toggleTheme()
    }
  }, [])

  return (
    <ThemeProvider>
      <Router>
        <div className="App">
          <header className="App-header">
            <button 
              className="theme-toggle" 
              onClick={toggleTheme}
              aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDarkMode ? '☀️' : '🌙'}
            </button>
            <h1>Interactive Story Generator</h1>
          </header>
          <main>
            <Routes>
              <Route path="/story/:id" element={<StoryLoader />} />
              <Route path="/" element={<StoryGenerator />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App