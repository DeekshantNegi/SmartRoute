import { useState } from "react";
import Navbar from "./components/Navbar";
import MapView from "./components/MapView";

function App() {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");

  return (
    <div className="h-screen w-screen flex flex-col">

      <Navbar
        source={source}
        setSource={setSource}
        destination={destination}
        setDestination={setDestination}
      />

      <div className="flex-1">
        <MapView />
      </div>

    </div>
  );
}

export default App;