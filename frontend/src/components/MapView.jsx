import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Polyline,
  Marker,
  Tooltip,
  useMap
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// 🔥 Fix default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
});

// 🔁 Convert [lon, lat] → [lat, lon]
const convertCoords = (route = []) =>
  route.map(([lon, lat]) => [lat, lon]);

// 📍 Get midpoint
const getMidPoint = (route) => {
  if (!route || route.length === 0) return null;
  return route[Math.floor(route.length / 2)];
};

// 🔥 Invisible icon (for fuel labels)
const invisibleIcon = L.divIcon({
  className: "",
});

// 🔥 Fit map to route
function FitBounds({ route }) {
  const map = useMap();

  useEffect(() => {
    if (route && route.length > 0) {
      map.fitBounds(route);
    }
  }, [route, map]);

  return null;
}

function MapView({ data }) {
  const [currentPosition, setCurrentPosition] = useState(null);

  // 📍 Get user location
  useEffect(() => {
    if (!navigator.geolocation) return;

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setCurrentPosition([
          pos.coords.latitude,
          pos.coords.longitude
        ]);
      },
      () => {
        setCurrentPosition([30.3165, 78.0322]); // fallback (Dehradun)
      }
    );
  }, []);

  // 🧠 Extract single route
  const route = convertCoords(data?.route || []);

  // 📍 Midpoint
  const midPoint = getMidPoint(route);

  // 📍 Start & End
  const start = route.length > 0 ? route[0] : null;
  const end = route.length > 0 ? route[route.length - 1] : null;

  return (
    <MapContainer
      center={start || currentPosition || [30.3165, 78.0322]}
      zoom={10}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution="© OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* 🔥 AUTO FIT */}
      {route.length > 0 && <FitBounds route={route} />}

      {/* 🔵 ROUTE */}
      {route.length > 0 && (
        <>
          <Polyline positions={route} color="blue" />

          {/* 💰 Fuel Cost */}
          {midPoint && (
            <Marker position={midPoint} icon={invisibleIcon}>
              <Tooltip permanent direction="top">
                <div className="bg-white px-2 py-1 rounded-md shadow-md text-xs font-semibold border border-gray-300">
                  ₹{data?.fuel_cost}
                </div>
              </Tooltip>
            </Marker>
          )}
        </>
      )}

      {/* 📍 START */}
      {start && (
        <Marker position={start}>
          <Tooltip>Start</Tooltip>
        </Marker>
      )}

      {/* 🎯 DESTINATION */}
      {end && (
        <Marker position={end}>
          <Tooltip>Destination</Tooltip>
        </Marker>
      )}

      {/* 📍 CURRENT LOCATION */}
      {currentPosition && (
        <Marker position={currentPosition}>
          <Tooltip>Your Location</Tooltip>
        </Marker>
      )}
    </MapContainer>
  );
}

export default MapView;