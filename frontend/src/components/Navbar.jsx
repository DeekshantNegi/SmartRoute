import { useState } from "react";
import logo from "../assets/logo.png";

function Navbar({ onFindRoute }) {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [traffic, setTraffic] = useState("medium");

  const handleSubmit = () => {
    onFindRoute({
      source,
      destination,
      traffic
    });
  };

  return (
    <div className="w-full bg-white shadow-md p-4 flex items-center">

      {/* Logo at extreme left */}
      <img
        src={logo}
        alt="Logo"
        className="h-12 w-auto"
      />

      {/* Center section */}
      <div className="flex gap-4 mx-auto items-center">

        <input
          type="text"
          placeholder="Enter Source"
          className="border px-3 py-2 rounded-lg"
          value={source}
          onChange={(e) => setSource(e.target.value)}
        />

        <input
          type="text"
          placeholder="Enter Destination"
          className="border px-3 py-2 rounded-lg"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
        />

        <select
          className="border px-3 py-2 rounded-lg"
          value={traffic}
          onChange={(e) => setTraffic(e.target.value)}
        >
          <option value="low">Low Traffic</option>
          <option value="medium">Medium Traffic</option>
          <option value="high">High Traffic</option>
        </select>

        <button
          onClick={handleSubmit}
          className="bg-orange-500 text-black px-4 py-2 rounded-lg hover:bg-orange-600"
        >
          Find Route
        </button>

      </div>

    </div>
  );
}

export default Navbar;