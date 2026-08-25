const defaultApiBaseUrl = 'http://localhost:8000'

export const appConfig = Object.freeze({
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL?.trim() || defaultApiBaseUrl,
})
