import { useState, createContext, useContext } from 'react'

const ThemeContext = createContext()

function ThemeProvider({ children }) {
    const [isDarkMode, setIsDarkMode] = useState(() => {
        // Check if dark mode is preferred by the system
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
        return prefersDark
    })

    const toggleTheme = () => {
        setIsDarkMode(prev => !prev)
        document.documentElement.classList.toggle('dark')
    }

    useEffect(() => {
        // Listen for system theme changes
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
        
        const handleThemeChange = (e) => {
            if (e.matches) {
                setIsDarkMode(true)
                document.documentElement.classList.add('dark')
            } else {
                setIsDarkMode(false)
                document.documentElement.classList.remove('dark')
            }
        }

        mediaQuery.addEventListener('change', handleThemeChange)
        return () => mediaQuery.removeEventListener('change', handleThemeChange)
    }, [])

    useEffect(() => {
        // Update dark mode class on mount
        if (isDarkMode) {
            document.documentElement.classList.add('dark')
        } else {
            document.documentElement.classList.remove('dark')
        }
    }, [isDarkMode])

    return (
        <ThemeContext.Provider value={{ isDarkMode, toggleTheme }}>
            <div className={`app-container ${isDarkMode ? 'dark' : 'light'}`}>
                {children}
            </div>
        </ThemeContext.Provider>
    )
}

function useTheme() {
    return useContext(ThemeContext)
}

export default ThemeProvider
export { useTheme }
