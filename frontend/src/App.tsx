import { useState, useEffect } from 'react'

interface HealthStatus {
  status: string
}

function App() {
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Use VITE_API_URL environment variable or default to localhost for development
  const apiUrl = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '')

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const healthUrl = `${apiUrl}/health`
        const response = await fetch(healthUrl)
        if (!response.ok) {
          throw new Error('Health check failed')
        }
        const data = await response.json()
        setHealthStatus(data)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setHealthStatus(null)
      } finally {
        setLoading(false)
      }
    }

    checkHealth()
  }, [apiUrl])

  return (
    <div className="min-h-screen bg-[#1E2A26] text-[#E8E8D8]">
      <div className="container mx-auto px-4 py-8 max-w-[600px]">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-[#F0F2F1] mb-2">Folio</h1>
          <p className="text-[#5B8A7A]">AI Portfolio Assistant</p>
        </header>

        <main className="space-y-6">
          <section className="bg-[#F0F2F1] text-[#1E2A26] p-6 rounded-lg">
            <h2 className="text-2xl font-semibold mb-4">System Status</h2>
            
            {loading && (
              <div className="text-[#5B8A7A]">Checking backend health...</div>
            )}

            {error && (
              <div className="text-red-600">
                <p className="font-semibold">Backend Connection Error</p>
                <p className="text-sm mt-1">{error}</p>
                <p className="text-sm mt-2">API URL: {apiUrl}</p>
              </div>
            )}

            {healthStatus && (
              <div className="text-green-700">
                <p className="font-semibold">✓ Backend Connected</p>
                <p className="text-sm mt-1">Status: {healthStatus.status}</p>
              </div>
            )}
          </section>

          <section className="bg-[#2D4A42] p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-4 text-[#F0F2F1]">Welcome to Folio</h2>
            <p className="text-[#E8E8D8]">
              Your AI-powered portfolio assistant. This is a minimal setup to verify deployment.
            </p>
          </section>
        </main>
      </div>
    </div>
  )
}

export default App

