import axios from "axios";

export const getRoutes = async ({ source_coords, destination }) => {
  try {
    const res = await axios.post("http://localhost:8000/route", {
      source_coords: source_coords,   // 🔥 GPS coordinates
      destination: destination
    });

    return res.data; // full response (routes + distance + fuel_cost)
    console.log("API RESPONSE:", res.data);
  } catch (err) {
    console.error("API Error:", err);
    return { error: true };
  }
};