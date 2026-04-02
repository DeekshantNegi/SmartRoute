import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Polyline,
  Marker,
  Popup,
  useMap
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix marker issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
});

// Convert [lon, lat] → [lat, lon]
const convertCoords = (route = []) => {
  return route.map((coord) => [coord[1], coord[0]]);
};

// Auto zoom
function FitBounds({ route = [] }) {
  const map = useMap();

  useEffect(() => {
    if (route.length > 0) {
      const bounds = route.map((coord) => [coord[1], coord[0]]);
      map.fitBounds(bounds);
    }
  }, [route, map]);

  return null;
}

function MapView({ routes, selectedTraffic = "all" }) {
  const [currentPosition, setCurrentPosition] = useState(null);

  useEffect(() => {
    if (!navigator.geolocation) return;

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setCurrentPosition([pos.coords.latitude, pos.coords.longitude]);
      },
      () => {
        setCurrentPosition([30.3165, 78.0322]); // fallback
      }
    );
  }, []);

  // Safe route extraction
  const low = convertCoords(routes?.low || []);
  const medium = convertCoords(routes?.medium || []);
  const high = convertCoords(routes?.high || []);

  const trafficToShow =
    selectedTraffic === "all"
      ? ["low", "medium", "high"]
      : [selectedTraffic];

  return (
    <MapContainer
      center={currentPosition || [30.3165, 78.0322]}
      zoom={10}
      style={{ height: "90vh", width: "100%" }}
    >
      <TileLayer
        attribution="© OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* ROUTES (only if available) */}
      {trafficToShow.includes("low") && low.length > 0 && (
        <>
          <Polyline positions={low} color="green" />
          <FitBounds route={routes?.low || []} />
        </>
      )}

      {trafficToShow.includes("medium") && medium.length > 0 && (
        <Polyline positions={medium} color="orange" />
      )}

      {trafficToShow.includes("high") && high.length > 0 && (
        <Polyline positions={high} color="red" />
      )}

      {/* Start + End markers (only if route exists) */}
      {low.length > 0 && (
        <>
          <Marker position={low[0]}>
            <Popup>Start</Popup>
          </Marker>

          <Marker position={low[low.length - 1]}>
            <Popup>Destination</Popup>
          </Marker>
        </>
      )}

      {/* Current location always visible */}
      {currentPosition && (
        <Marker position={currentPosition}>
          <Popup>Your Location</Popup>
        </Marker>
      )}
    </MapContainer>
  );
}

export default MapView;