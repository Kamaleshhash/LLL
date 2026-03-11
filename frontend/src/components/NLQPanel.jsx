import { useState } from 'react'
import client from '../api/client'

export default function NLQPanel() {
  const [query, setQuery] = useState('Show encroachment cases in Veerapandi last 5 years')
  const [cases, setCases] = useState([])

  const runQuery = async () => {
    const { data } = await client.post('/search/nlq/', { query })
    setCases(data.cases || [])
  }

  return (
    <section className="panel">
      <h3>Natural Language Search</h3>
      <div className="field-row">
        <input value={query} onChange={(e) => setQuery(e.target.value)} />
        <button onClick={runQuery}>Run Query</button>
      </div>
      <ul className="flat-list">
        {cases.map((item) => (
          <li key={item.cnr_number}>{item.cnr_number} | {item.case_type} | {item.status}</li>
        ))}
      </ul>
    </section>
  )
}
