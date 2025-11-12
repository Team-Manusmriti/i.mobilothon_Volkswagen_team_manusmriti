import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
// @ts-ignore 
import { AppProvider } from './context/AppContext.jsx'
import './styles/index.css'

// debug: confirm entry executes in browser console
console.log('main.tsx loaded');

const rootElement = document.getElementById('root')
if (!rootElement) throw new Error('Root element not found')

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <AppProvider>
      <App />
    </AppProvider>
  </React.StrictMode>,
)