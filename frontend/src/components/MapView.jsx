import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { useEffect, useState } from "react";
import "leaflet/dist/leaflet.css";

function MapView() {
  const [position, setPosition] = useState([30.3165, 78.0322]); // default Dehradun

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (location) => {
        const lat = location.coords.latitude;
        const lng = location.coords.longitude;

        setPosition([lat, lng]);
      },
      (error) => {
        console.log("Error getting location:", error);
      }
    );
  }, []);

  return (
    <MapContainer center={position} zoom={13} className="h-full w-full">
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="© OpenStreetMap"
      />

      <Marker position={position}>
        <Popup>You are here</Popup>
      </Marker>
    </MapContainer>
  );
}

export default MapView;