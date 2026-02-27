import React, { useState } from "react";

function AIChat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = () => {
    if (question.toLowerCase().includes("sugarcane")) {
      setAnswer(
        "For Sugarcane farmers, Drip Irrigation and Modernization Schemes are highly recommended."
      );
    } else if (question.toLowerCase().includes("rice")) {
      setAnswer(
        "For Rice farmers, PM-KISAN and Crop Insurance Yojana are suitable."
      );
    } else {
      setAnswer(
        "Please mention crop or state for better AI recommendation."
      );
    }
  };

  return (
    <div style={{ marginTop: "40px" }}>
      <h3>🤖 AI Assistant</h3>

      <input
        type="text"
        placeholder="Ask: Which scheme is best for sugarcane?"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px",
          borderRadius: "8px",
          border: "1px solid #ddd"
        }}
      />

      <button
        className="primary-btn"
        onClick={handleAsk}
      >
        Ask AI
      </button>

      {answer && (
        <div
          style={{
            marginTop: "15px",
            padding: "15px",
            background: "#f0f0f0",
            borderRadius: "8px"
          }}
        >
          {answer}
        </div>
      )}
    </div>
  );
}

export default AIChat;