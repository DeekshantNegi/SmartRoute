import { useEffect, useState } from "react";
import { getRoutes } from "./api";
import MapView from "./MapView"; // 🔥 IMPORTANT

function App() {
  const [routes, setRoutes] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getRoutes({
          source: "Dehradun",
          destination: "Mussoorie"
        });

        console.log("API RESPONSE:", data);

        if (!data.error) {
          setRoutes(data.routes);
        }
      } catch (err) {
        console.error("API Error:", err);
      }
    };

    fetchData();
  }, []);

  console.log("ROUTES STATE:", routes);

  return (
    <>
      {!routes ? (
        <div style={{ padding: "20px" }}>Loading route...</div>
      ) : (
        <MapView routes={routes} selectedTraffic="all" />
      )}
    </>
  );
}

export default App;