import { MapContainer, Polygon, TileLayer } from 'react-leaflet'

export default function ParcelMap({ boundary }) {
  const coordinates = boundary?.coordinates?.[0] || []
  const latLngs = coordinates.map((pair) => [pair[1], pair[0]])
  const center = latLngs[0] || [11.664, 78.128]

  return (
    <div className="map-wrap">
      <MapContainer center={center} zoom={16} scrollWheelZoom={false} style={{ height: '260px', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {latLngs.length > 0 && <Polygon positions={latLngs} pathOptions={{ color: '#a32020' }} />}
      </MapContainer>
    </div>
  )
}
