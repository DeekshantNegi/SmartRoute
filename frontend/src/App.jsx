import { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "./components/Navbar";
import MapView from "./components/MapView";
import RouteInfo from "./components/RouteInfo";

function App() {
  const [currentPosition, setCurrentPosition] = useState(null);
  const [data, setData] = useState(null);

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
      (err) => console.error(err)
    );
  }, []);

  // 🚀 Find route
  const findRoute = async ({ sourceInput, destination }) => {
    if (!destination) {
      alert("Destination missing");
      return;
    }

    try {
      const payload = {
        destination
      };

      if (sourceInput) {
        payload.source = sourceInput;
      } else if (currentPosition) {
        payload.source_coords = currentPosition;
      }

      const res = await axios.post(
        "http://localhost:8000/route",
        payload
      );

      setData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      
      {/* 🔝 Navbar */}
      <div className="flex-shrink-0">
        <Navbar
          onFindRoute={findRoute}
          currentPosition={currentPosition}
        />
      </div>

      {/* 🗺 Map + Overlay */}
      <div className="flex-1 relative">
        <MapView data={data} />

        {/* 📦 Route Info (only when data exists) */}
        {data && (
          <RouteInfo
            data={data}
            onClose={() => setData(null)}
          />
        )}
      </div>

    </div>
  );
}

export default App;