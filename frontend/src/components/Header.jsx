export default function Header({ t, language, setLanguage, user, onLogout }) {
  return (
    <header className="portal-header">
      <div>
        <h1>{t.portalTitle}</h1>
        <p>{t.subtitle}</p>
      </div>
      <div className="header-controls">
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="en">English</option>
          <option value="ta">Tamil</option>
        </select>
        {user && (
          <div className="user-chip">
            <span>{user.email || user.username}</span>
            <button onClick={onLogout}>Logout</button>
          </div>
        )}
      </div>
    </header>
  )
}
