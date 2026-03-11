import { useState } from 'react'
import client from '../api/client'

export default function AlertPanel({ selectedCnr, canUse }) {
  const [destination, setDestination] = useState('')
  const [message, setMessage] = useState('')

  const createAlert = async () => {
    if (!canUse) {
      setMessage('Login required for alerts.')
      return
    }
    if (!selectedCnr) {
      setMessage('Select a case first.')
      return
    }
    await client.post('/alerts/', { cnr_number: selectedCnr, channel: 'email', destination })
    setMessage('Alert subscription created.')
  }

  return (
    <section className="panel">
      <h3>Track Case Alerts</h3>
      <div className="field-row">
        <input value={destination} onChange={(e) => setDestination(e.target.value)} placeholder="Email or mobile" />
        <button onClick={createAlert}>Subscribe</button>
      </div>
      {message && <p className="hint">{message}</p>}
    </section>
  )
}
