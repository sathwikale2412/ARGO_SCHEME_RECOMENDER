import React, { useState } from "react";
import axios from "axios";
import SchemeCard from "./SchemeCard";
import AIChat from "./AIChat";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function FarmerForm() {
  const [form, setForm] = useState({
    state: "Karnataka",
    crop: "Rice",
    land: 5,
    category: "General",
    income: 400000
  });

  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

const handleSubmit = async () => {
  setLoading(true);
  const res = await axios.post(
    "http://127.0.0.1:5000/recommend",
    form
  );
  setSchemes(res.data);
  setLoading(false);
};

  return (
    <div>
      {/* Filters */}
      <div className="filter-grid">
        <select name="state" onChange={handleChange}>
          <option>Karnataka</option>
          <option>Maharashtra</option>
        </select>

        <select name="crop" onChange={handleChange}>
          <option>Rice</option>
          <option>Sugarcane</option>
        </select>

        <input
          type="number"
          name="land"
          placeholder="Land Size"
          onChange={handleChange}
        />

        <select name="category" onChange={handleChange}>
          <option>General</option>
          <option>OBC</option>
        </select>

        <input
          type="number"
          name="income"
          placeholder="Income"
          onChange={handleChange}
        />
      </div>

    <button className="primary-btn" onClick={handleSubmit}>
  {loading ? "Analyzing..." : "🔍 Get Schemes"}
</button>

      {/* Total Counter */}
      {schemes.length > 0 && (
        <h3 style={{ marginTop: "20px" }}>
          📊 Total Schemes Found: {schemes.length}
        </h3>
      )}

      {/* Scheme Cards */}
      <div style={{ marginTop: "20px" }}>
        {schemes.map((s, index) => (
          <SchemeCard
            key={index}
            scheme={s}
            farmerInput={form}
          />
        ))}
      </div>
      {schemes.length > 0 && (
  <div style={{ marginTop: 20 }}>
    <h3>📊 Insights</h3>
    <p>✔ {schemes.length} Eligible Schemes Found</p>
    <p>
      ✔ Highest Subsidy: ₹
      {Math.max(...schemes.map(s => s.subsidy))}
    </p>
  </div>
)}

      {/* Chart */}
      {schemes.length > 0 && (
        <div style={{ height: 300, marginTop: 40 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={schemes}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="subsidy" fill="#ff5a5f" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* AI Chat */}
      <AIChat />
    </div>
  );
}

export default FarmerForm;