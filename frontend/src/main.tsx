import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import { chatApiClient } from './api/ChatApiClient'
import './styles/main.scss'

chatApiClient.initialize()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)


