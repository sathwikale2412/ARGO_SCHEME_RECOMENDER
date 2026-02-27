import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    state: "",
    crop: "",
    land: "",
    category: "",
    income: "",
  });

  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(false);

  const [chatOpen, setChatOpen] = useState(false);
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState([]);

  // ✅ All States + Crops
  const statesCrops = {
    "Punjab": ["Wheat", "Rice", "Maize"],
    "Maharashtra": ["Sugarcane", "Cotton", "Soybean"],
    "Karnataka": ["Rice", "Ragi", "Sugarcane"],
    "Tamil Nadu": ["Rice", "Coconut", "Sugarcane"],
    "Uttar Pradesh": ["Wheat", "Rice", "Sugarcane"],
    "Gujarat": ["Cotton", "Groundnut", "Bajra"],
    "Kerala": ["Coconut", "Rubber", "Spices"],
    "West Bengal": ["Rice", "Jute", "Tea"],
    "Bihar": ["Rice", "Wheat", "Maize"],
    "Rajasthan": ["Bajra", "Wheat", "Mustard"],
    "Madhya Pradesh": ["Soybean", "Wheat", "Pulses"],
    "Andhra Pradesh": ["Rice", "Chilli", "Cotton"],
    "Telangana": ["Rice", "Cotton", "Maize"],
    "Odisha": ["Rice", "Pulses", "Oilseeds"],
    "Haryana": ["Wheat", "Rice", "Cotton"],
    "Chhattisgarh": ["Rice", "Maize", "Pulses"],
    "Assam": ["Tea", "Rice", "Mustard"],
    "Jharkhand": ["Rice", "Maize", "Pulses"],
    "Himachal Pradesh": ["Apple", "Maize", "Wheat"],
    "Uttarakhand": ["Rice", "Wheat", "Millets"],
    "Goa": ["Rice", "Coconut", "Cashew"],
    "Tripura": ["Rice", "Rubber", "Tea"],
    "Manipur": ["Rice", "Maize", "Pulses"],
    "Meghalaya": ["Rice", "Potato", "Maize"],
    "Mizoram": ["Rice", "Oilseeds", "Maize"],
    "Nagaland": ["Rice", "Maize", "Millets"],
    "Sikkim": ["Cardamom", "Maize", "Rice"],
    "Arunachal Pradesh": ["Rice", "Maize", "Millets"]
  };

  // ✅ Dynamic Crop Background
  const cropBackgrounds = {
    Rice: "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=1600&q=80",
    Wheat: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1600&q=80",
    Sugarcane: "https://images.unsplash.com/photo-1600431521340-491eca880813?auto=format&fit=crop&w=1600&q=80",
    Cotton: "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?auto=format&fit=crop&w=1600&q=80"
  };

  const getBackgroundImage = () => {
    return (
      cropBackgrounds[formData.crop] ||
      "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1600&q=80"
    );
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    // Reset crop if state changes
    if (name === "state") {
      setFormData({
        ...formData,
        state: value,
        crop: ""
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/get_schemes",
        formData
      );
      setSchemes(response.data);
    } catch (error) {
      alert("Server not connected.");
    }

    setLoading(false);
  };

  const sendMessage = async () => {
  if (!chatInput.trim()) return;

  const userMessage = {
    sender: "user",
    text: chatInput
  };

  setChatMessages(prev => [...prev, userMessage]);

  try {
    const response = await axios.post(
      "http://127.0.0.1:5000/chat",
      { message: chatInput }
    );

    const botMessage = {
      sender: "bot",
      text: response.data.reply,
      schemes: response.data.schemes || []   // 🔥 THIS IS THE FIX
    };

    setChatMessages(prev => [...prev, botMessage]);

  } catch (error) {
    setChatMessages(prev => [
      ...prev,
      { sender: "bot", text: "Server error." }
    ]);
  }

  setChatInput("");
};

  return (
    <div
      className="app"
      style={{
        background: `linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url(${getBackgroundImage()})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundAttachment: "fixed",
        minHeight: "100vh",
        transition: "background 0.6s ease"
      }}
    >
      <nav className="navbar">
        <div className="logo">🌾 AgroScheme AI</div>
      </nav>

      <section className="hero">
        <h1>Smart Government Scheme Finder</h1>
        <p>AI-powered agricultural assistance platform</p>
      </section>

      <div className="main-container">
        <div className="form-card">
          <h2>Find Your Eligible Schemes</h2>

          <form onSubmit={handleSubmit}>
            <div className="form-grid">

              {/* State */}
              <select
                name="state"
                value={formData.state}
                onChange={handleChange}
              >
                <option value="">Select State</option>
                {Object.keys(statesCrops).map((state) => (
                  <option key={state} value={state}>
                    {state}
                  </option>
                ))}
              </select>

              {/* Crop */}
              <select
                name="crop"
                value={formData.crop}
                onChange={handleChange}
                disabled={!formData.state}
              >
                <option value="">Select Crop</option>
                {formData.state &&
                  statesCrops[formData.state].map((crop) => (
                    <option key={crop} value={crop}>
                      {crop}
                    </option>
                  ))}
              </select>

              <input
                name="land"
                type="number"
                placeholder="Land (acres)"
                value={formData.land}
                onChange={handleChange}
              />

              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
              >
                <option value="">Select Category</option>
                <option value="General">General</option>
                <option value="OBC">OBC</option>
                <option value="SC">SC</option>
                <option value="ST">ST</option>
              </select>

              <input
                name="income"
                type="number"
                placeholder="Annual Income"
                value={formData.income}
                onChange={handleChange}
              />
            </div>

            <button className="primary-btn">
              {loading ? "Analyzing..." : "🚀 Get Schemes"}
            </button>
          </form>
        </div>
      </div>
      {/* Results Section */}
<div className="results-section">
  {schemes.length > 0 && <h2>Recommended Schemes</h2>}

  {schemes.map((scheme, index) => (
    <div key={index} className="scheme-card">
      <h3>{scheme.name}</h3>
      <p><strong>Subsidy:</strong> ₹{scheme.subsidy}</p>
      <p><strong>Documents:</strong> {scheme.documents}</p>
      <p><strong>Deadline:</strong> {scheme.deadline}</p>
    </div>
  ))}
</div>

      {/* Chatbot */}
      <div className="chatbot">
        <button
          className="chat-toggle"
          onClick={() => setChatOpen(!chatOpen)}
        >
          🤖
        </button>

        {chatOpen && (
          <div className="chat-window">
            <div className="chat-header">AI Scheme Assistant</div>

            <div className="chat-messages">
  {chatMessages.map((msg, index) => (
    <div key={index} className={`chat-message ${msg.sender}`}>
      
      <p>{msg.text}</p>

      {msg.schemes && msg.schemes.length > 0 && (
        <>
          {msg.schemes.map((scheme, i) => (
            <div key={i}>
              <strong>{scheme.name}</strong>
              <div>₹{scheme.subsidy} | {scheme.deadline}</div>
            </div>
          ))}
        </>
      )}

    </div>
  ))}
</div>
            <div className="chat-input">
              <input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Ask about schemes..."
              />
              <button onClick={sendMessage}>Send</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;