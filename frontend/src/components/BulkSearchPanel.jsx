import { useState } from 'react'
import client from '../api/client'

export default function BulkSearchPanel({ user }) {
  const [text, setText] = useState('Tamil Nadu,Salem,Veerapandi,45/2B')
  const [rows, setRows] = useState([])

  const runBulk = async () => {
    if (!user || !['administrative', 'institutional'].includes(user.role)) return

    const items = text
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => {
        const [state, district, village_name, survey_number] = line.split(',')
        return { state, district, village_name, survey_number }
      })

    const { data } = await client.post('/search/bulk/', { items })
    setRows(data.output || [])
  }

  return (
    <section className="panel">
      <h3>Administrative Bulk Search</h3>
      <textarea value={text} onChange={(e) => setText(e.target.value)} rows={4} />
      <button onClick={runBulk} disabled={!user || !['administrative', 'institutional'].includes(user.role)}>
        Run Bulk Query
      </button>
      <ul className="flat-list">
        {rows.map((row, idx) => (
          <li key={idx}>
            {row.query.village_name} {row.query.survey_number} &rarr; Matches: {row.matches}, Pending Cases: {row.pending_cases}
          </li>
        ))}
      </ul>
    </section>
  )
}
