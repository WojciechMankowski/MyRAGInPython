// src/main.tsx
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'


const container = document.getElementById('root')
if (!container) throw new Error('Brak elementu #root w index.html')
createRoot(container).render(
	<React.StrictMode>
		<App />
	</React.StrictMode>
)
