import { useState } from "react";
import logo from "../assets/logo.png";

function Navbar({ onFindRoute, currentPosition }) {
  const [sourceInput, setSourceInput] = useState("");
  const [destination, setDestination] = useState("");

  const handleSubmit = () => {
    if (!destination) {
      alert("Please enter a destination!");
      return;
    }

    onFindRoute({ sourceInput, destination });
  };

  return (
    <div className="w-full bg-white shadow-md p-4 flex items-center">
      {/* Logo */}
      <img src={logo} alt="Logo" className="h-12 w-auto" />

      {/* Center inputs */}
      <div className="flex gap-4 mx-auto items-center">
        <input
          type="text"
          placeholder="Enter Source (optional)"
          className="border px-3 py-2 rounded-lg"
          value={sourceInput}
          onChange={(e) => setSourceInput(e.target.value)}
        />

        <input
          type="text"
          placeholder="Enter Destination"
          className="border px-3 py-2 rounded-lg"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
        />

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