import React, { useState } from 'react'
import axios from 'axios'

const RagChat = () => {
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAsk = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setAnswer('')
    try {
      const res = await axios.post('/api/rag/query', { query })
      setAnswer(res?.data?.answer || '')
    } catch (err) {
      setError(err?.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h2 className="text-2xl font-semibold mb-4">RAG Assistant</h2>
      <form onSubmit={handleAsk} className="flex gap-2 mb-4">
        <input
          className="flex-1 border rounded px-3 py-2"
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="submit"
          className="bg-primary-600 text-white px-4 py-2 rounded disabled:opacity-60"
          disabled={!query || loading}
        >
          {loading ? 'Asking...' : 'Ask'}
        </button>
      </form>
      {error && <div className="text-destructive mb-2">{error}</div>}
      {answer && (
        <div className="bg-muted/50 border rounded p-3 whitespace-pre-wrap">
          {answer}
        </div>
      )}
    </div>
  )
}

export default RagChat


