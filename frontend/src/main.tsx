import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { App } from './App'
import { createMockAnalysisClient } from './services/mockAnalysisClient'

const rootElement = document.getElementById('root')

if (!rootElement) {
  throw new Error('Root element was not found')
}

const queryParameters = new URLSearchParams(window.location.search)
const analysisClient = createMockAnalysisClient({
  failFirstRequest: queryParameters.get('mock') === 'failure',
})

createRoot(rootElement).render(
  <StrictMode>
    <App analysisClient={analysisClient} />
  </StrictMode>,
)
