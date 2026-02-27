import React, { useState } from "react";
import axios from "axios";
import SchemeCard from "./SchemeCard";

function FarmerForm() {
  const [form, setForm] = useState({
    state: "",
    crop: "",
    land: "",
    category: "",
    income: ""
  });

  const [schemes, setSchemes] = useState([]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    const res = await axios.post(
      "http://127.0.0.1:5000/recommend",
      form
    );
    setSchemes(res.data);
  };

  return (
    <div>
      <div style={styles.grid}>
        <input name="state" placeholder="State" onChange={handleChange} style={styles.input}/>
        <input name="crop" placeholder="Crop" onChange={handleChange} style={styles.input}/>
        <input name="land" placeholder="Land Size" onChange={handleChange} style={styles.input}/>
        <input name="category" placeholder="Category" onChange={handleChange} style={styles.input}/>
        <input name="income" placeholder="Income" onChange={handleChange} style={styles.input}/>
      </div>

      <button style={styles.searchBtn} onClick={handleSubmit}>
        🔍 Get Schemes
      </button>

      <div style={{ marginTop: "25px" }}>
        {schemes.map((s, index) => (
          <SchemeCard key={index} scheme={s} index={index}/>
        ))}
      </div>
    </div>
  );
}

const styles = {
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
    gap: "10px",
    marginBottom: "15px"
  },
  input: {
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #ccc"
  },
  searchBtn: {
    backgroundColor: "#1976d2",
    color: "white",
    padding: "10px 20px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer"
  }
};

export default FarmerForm;