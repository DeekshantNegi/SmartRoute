import { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "./components/Navbar";
import MapView from "./components/MapView";

function App() {
  const [currentPosition, setCurrentPosition] = useState(null);
  const [routes, setRoutes] = useState({
    low: [],
    medium: [],
    high: [],
  });
  const [selectedTraffic, setSelectedTraffic] = useState("medium"); // default

  // Get user's current location on mount
  useEffect(() => {
    if (!navigator.geolocation) return;

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setCurrentPosition([pos.coords.latitude, pos.coords.longitude]);
      },
      (err) => console.error("Error getting location:", err)
    );
  }, []);

  // Function called when user clicks "Find Route"
  const findRoute = async ({ sourceInput, destination }) => {

  if (!sourceInput || !destination) {
    alert("Source or destination missing");
    return;
  }

  try {
    const res = await axios.post("http://localhost:8000/route", {
      source: sourceInput,
      destination: destination
    });

    setRoutes(res.data.routes);

  } catch (err) {
    console.error(err);
  }
};

  return (
    <div>
      <Navbar
        onFindRoute={findRoute}
        currentPosition={currentPosition}
        selectedTraffic={selectedTraffic}
        setSelectedTraffic={setSelectedTraffic}
      />
      <MapView routes={routes} selectedTraffic="all" />
    </div>
  );
}

export default App;