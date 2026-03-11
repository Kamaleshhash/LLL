import { useMemo, useState } from 'react'

import { setAuthToken } from './api/client'
import AlertPanel from './components/AlertPanel'
import AuthPanel from './components/AuthPanel'
import BulkSearchPanel from './components/BulkSearchPanel'
import Header from './components/Header'
import NLQPanel from './components/NLQPanel'
import ResultsDashboard from './components/ResultsDashboard'
import SearchForm from './components/SearchForm'
import { translations } from './i18n/translations'

export default function App() {
  const [language, setLanguage] = useState('en')
  const [auth, setAuth] = useState(null)
  const [searchData, setSearchData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [selectedCnr, setSelectedCnr] = useState('')

  const t = useMemo(() => translations[language], [language])

  const logout = () => {
    setAuth(null)
    setAuthToken(null)
  }

  return (
    <div className="app-shell">
      <Header t={t} language={language} setLanguage={setLanguage} user={auth?.user} onLogout={logout} />

      <main className="main-grid">
        <div className="left-col">
          {!auth ? (
            <>
              <AuthPanel t={t} onAuth={setAuth} />
              <button className="secondary-btn" onClick={() => setAuth({ token: null, user: null })}>{t.guestMode}</button>
            </>
          ) : null}
          <SearchForm t={t} onResults={setSearchData} onLoading={setLoading} />
          <NLQPanel />
          <BulkSearchPanel user={auth?.user} />
        </div>

        <div className="right-col">
          {loading && <section className="panel"><p>Loading records...</p></section>}
          <ResultsDashboard searchData={searchData} t={t} onSelectCase={setSelectedCnr} />
          <AlertPanel selectedCnr={selectedCnr} canUse={Boolean(auth?.user)} />
        </div>
      </main>
    </div>
  )
}
