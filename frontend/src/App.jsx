import { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "./components/Navbar";
import MapView from "./components/MapView";

function App() {
  const [currentPosition, setCurrentPosition] = useState(null);
  const [data, setData] = useState(null);
  const [selectedTraffic, setSelectedTraffic] = useState("all");

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
    <div>
      {/* ✅ Always visible */}
      <Navbar
        onFindRoute={findRoute}
        currentPosition={currentPosition}
        selectedTraffic={selectedTraffic}
        setSelectedTraffic={setSelectedTraffic}
      />

      {/* ✅ Always show map */}
      <MapView data={data} selectedTraffic={selectedTraffic} />
    </div>
  );
}

export default App;