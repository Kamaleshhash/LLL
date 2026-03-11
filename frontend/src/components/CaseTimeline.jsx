export default function CaseTimeline({ events }) {
  if (!events?.length) return <p>No timeline events.</p>

  return (
    <ol className="timeline">
      {events.map((event) => (
        <li key={`${event.event_date}-${event.title}`}>
          <strong>{event.event_date}</strong> - {event.title}
          <p>{event.description}</p>
        </li>
      ))}
    </ol>
  )
}
