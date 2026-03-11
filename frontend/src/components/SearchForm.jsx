import { useEffect, useState } from 'react'
import client from '../api/client'

const defaultForm = {
  state: 'Tamil Nadu',
  district: 'Salem',
  village_name: 'Veerapandi',
  survey_number: '45/2B',
  case_type: '',
  status: '',
  from_date: '',
  to_date: '',
}

export default function SearchForm({ t, onResults, onLoading }) {
  const [form, setForm] = useState(defaultForm)
  const [suggestions, setSuggestions] = useState([])

  useEffect(() => {
    if (!form.village_name || form.village_name.length < 2) return
    const timer = setTimeout(async () => {
      const { data } = await client.get('/search/autocomplete/village/', {
        params: { state: form.state, district: form.district, query: form.village_name },
      })
      setSuggestions(data.suggestions || [])
    }, 300)
    return () => clearTimeout(timer)
  }, [form.village_name, form.state, form.district])

  const onChange = (key, value) => setForm((prev) => ({ ...prev, [key]: value }))

  const submit = async (e) => {
    e.preventDefault()
    onLoading(true)
    try {
      const payload = { ...form }
      if (!payload.from_date) delete payload.from_date
      if (!payload.to_date) delete payload.to_date
      const { data } = await client.post('/search/', payload)
      onResults(data)
    } finally {
      onLoading(false)
    }
  }

  return (
    <form className="panel search-panel" onSubmit={submit}>
      <h2>Search Land Parcel Litigation</h2>
      <div className="grid-4">
        <label>
          {t.state}
          <input value={form.state} onChange={(e) => onChange('state', e.target.value)} required />
        </label>
        <label>
          {t.district}
          <input value={form.district} onChange={(e) => onChange('district', e.target.value)} required />
        </label>
        <label>
          {t.village}
          <input value={form.village_name} onChange={(e) => onChange('village_name', e.target.value)} required list="village-suggestions" />
        </label>
        <label>
          {t.survey}
          <input value={form.survey_number} onChange={(e) => onChange('survey_number', e.target.value)} required pattern="^[0-9]+(/[0-9A-Za-z]+)?$" />
        </label>
      </div>
      <datalist id="village-suggestions">
        {suggestions.map((item) => (
          <option key={item} value={item} />
        ))}
      </datalist>
      <h3>{t.caseFilters}</h3>
      <div className="grid-4">
        <label>
          Case Type
          <select value={form.case_type} onChange={(e) => onChange('case_type', e.target.value)}>
            <option value="">All</option>
            <option value="Title">Title Dispute</option>
            <option value="Encroachment">Encroachment</option>
          </select>
        </label>
        <label>
          Status
          <select value={form.status} onChange={(e) => onChange('status', e.target.value)}>
            <option value="">All</option>
            <option value="pending">Pending</option>
            <option value="disposed">Disposed</option>
            <option value="stayed">Stayed</option>
          </select>
        </label>
        <label>
          From
          <input type="date" value={form.from_date} onChange={(e) => onChange('from_date', e.target.value)} />
        </label>
        <label>
          To
          <input type="date" value={form.to_date} onChange={(e) => onChange('to_date', e.target.value)} />
        </label>
      </div>
      <button type="submit" className="primary-btn">
        {t.search}
      </button>
    </form>
  )
}
