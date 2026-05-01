import React from "react";

function RouteInfo({ data, onClose }) {
  if (!data) return null;

  return (
    <div className="absolute top-5 right-5 bg-white/90 backdrop-blur-md shadow-lg rounded-xl p-4 w-72 z-[1000] border border-gray-200">
      
      {/* ❌ Close Button */}
      <button
        onClick={onClose}
        className="absolute top-2 right-2 text-gray-500 hover:text-red-500 text-lg"
      >
        ✕
      </button>

      <h2 className="text-lg font-bold mb-3">Route Details</h2>

      <div className="space-y-2 text-sm">
        <p>
          <strong>🚗 Distance:</strong> {data.distance} km
        </p>
        <p>
          <strong>⏱ Duration:</strong> {data.duration} mins
        </p>
        <p>
          <strong>⛽ Fuel Cost:</strong> ₹{data.fuel_cost}
        </p>
      </div>
    </div>
  );
}

export default RouteInfo;