import { useState } from 'react'
import client, { setAuthToken } from '../api/client'

export default function AuthPanel({ t, onAuth }) {
  const [email, setEmail] = useState('official@tn.gov.in')
  const [otp, setOtp] = useState('')
  const [debugOtp, setDebugOtp] = useState('')

  const requestOtp = async () => {
    const { data } = await client.post('/auth/request-otp/', { email })
    setDebugOtp(data.debug_otp)
  }

  const verifyOtp = async () => {
    const { data } = await client.post('/auth/verify-otp/', { email, otp })
    setAuthToken(data.token)
    onAuth({ token: data.token, user: data.user })
  }

  return (
    <section className="panel auth-panel">
      <h2>{t.login}</h2>
      <div className="field-row">
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <button onClick={requestOtp}>Request OTP</button>
      </div>
      {debugOtp && <p className="hint">Mock OTP: {debugOtp}</p>}
      <div className="field-row">
        <input value={otp} onChange={(e) => setOtp(e.target.value)} placeholder="Enter OTP" />
        <button onClick={verifyOtp}>Verify</button>
      </div>
    </section>
  )
}
