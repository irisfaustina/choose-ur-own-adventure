import { useState, createContext, useContext } from 'react'

const ThemeContext = createContext()

function ThemeProvider({ children }) {
    const [isDarkMode, setIsDarkMode] = useState(false)

    const toggleTheme = () => {
        setIsDarkMode(!isDarkMode)
        document.documentElement.classList.toggle('dark')
    }

    return (
        <ThemeContext.Provider value={{ isDarkMode, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    )
}

function useTheme() {
    return useContext(ThemeContext)
}

export default ThemeProvider
export { useTheme }
