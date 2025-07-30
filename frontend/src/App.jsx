import './App.css'
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import StoryLoader from "./components/StoryLoader"
import StoryGenerator from "./components/StoryGenerator"
import ThemeProvider from "./components/ThemeProvider"
import { useTheme } from "./components/ThemeProvider"
import { useEffect } from 'react'

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="App">
          <ThemeToggle />
          <Routes>
            <Route path="/story/:id" element={<StoryLoader />} />
            <Route path="/" element={<StoryGenerator />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  )
}

function ThemeToggle() {
  const { isDarkMode, toggleTheme } = useTheme()

  useEffect(() => {
    // Set initial theme based on user preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    if (prefersDark) {
      toggleTheme()
    }
  }, [])

  return (
    <header className="App-header">
      <button 
        className="theme-toggle" 
        onClick={toggleTheme}
        aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
      >
        {isDarkMode ? '☀️' : '🌙'}
      </button>
      <h1>Choose Your Own Adventure</h1>
    </header>
  )
}

export default App