import { useMemo, useState } from 'react'
import CaseTimeline from './CaseTimeline'
import ParcelMap from './ParcelMap'

export default function ResultsDashboard({ searchData, t, onSelectCase }) {
  const [selectedCase, setSelectedCase] = useState(null)
  const result = useMemo(() => (searchData?.results?.length ? searchData.results[0] : null), [searchData])

  if (!result) {
    return (
      <section className="panel">
        <h3>Search Results</h3>
        {searchData?.manual_verification_tips ? (
          <>
            <p>{t.noMatches}</p>
            <ul>
              {searchData.manual_verification_tips.map((tip) => (
                <li key={tip}>{tip}</li>
              ))}
            </ul>
          </>
        ) : (
          <p>Run a search to view litigation and land record links.</p>
        )}
      </section>
    )
  }

  const cases = result.cases || []

  return (
    <section className="panel">
      <h3>Matched Parcel and Linked Cases</h3>
      <div className="verification-bar">
        <span className="badge">{result.verification.badge}</span>
        <span>Hash: {result.verification.hash}</span>
      </div>

      <div className="grid-2">
        <div>
          <h4>Land Details</h4>
          <table className="data-table">
            <tbody>
              <tr><td>Owner</td><td>{result.parcel.owner_name}</td></tr>
              <tr><td>Area</td><td>{result.parcel.area_hectare} ha</td></tr>
              <tr><td>Type</td><td>{result.parcel.land_type}</td></tr>
              <tr><td>RoR Ref</td><td>{result.parcel.ror_reference}</td></tr>
              <tr><td>Village</td><td>{result.parcel.village_name}</td></tr>
              <tr><td>Survey</td><td>{result.parcel.survey_number}</td></tr>
            </tbody>
          </table>
        </div>
        <ParcelMap boundary={result.parcel.geojson_boundary} />
      </div>

      <h4>Case List</h4>
      <table className="data-table">
        <thead>
          <tr>
            <th>CNR</th>
            <th>Type</th>
            <th>Court</th>
            <th>Status</th>
            <th>Next Hearing</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {cases.map((link) => (
            <tr key={link.case.cnr_number}>
              <td>{link.case.cnr_number}</td>
              <td>{link.case.case_type}</td>
              <td>{link.case.court_name}</td>
              <td>{link.case.status}</td>
              <td>{link.case.next_hearing_date || '-'}</td>
              <td>
                <button
                  onClick={() => {
                    setSelectedCase(link.case)
                    onSelectCase(link.case.cnr_number)
                  }}
                >
                  View
                </button>
                <a href={`/api/reports/case-summary/${link.case.cnr_number}/`} target="_blank" rel="noreferrer">PDF</a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedCase && (
        <div className="case-detail">
          <h4>Case Detail: {selectedCase.cnr_number}</h4>
          <p>{selectedCase.petitioner} vs {selectedCase.respondent}</p>
          <p>Filed: {selectedCase.filing_date} | Last: {selectedCase.last_hearing_date} | Stage: {selectedCase.stage}</p>
          <p>Risk Score: {Math.round((selectedCase.risk_score || 0) * 100)}%</p>
          <CaseTimeline events={selectedCase.events} />
          {selectedCase.order_pdf_url && <a href={selectedCase.order_pdf_url} target="_blank" rel="noreferrer">View Court Order</a>}
        </div>
      )}
    </section>
  )
}
