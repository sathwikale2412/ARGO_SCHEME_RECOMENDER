import React from "react";
import { motion } from "framer-motion";

function calculateMatchScore(scheme, farmerInput) {
  let score = 0;

  if (scheme.state === farmerInput.state) score += 20;
  if (scheme.crop === farmerInput.crop) score += 20;
  if (scheme.category === farmerInput.category) score += 20;

  if (
    farmerInput.land >= scheme.min_land &&
    farmerInput.land <= scheme.max_land
  )
    score += 20;

  if (farmerInput.income <= scheme.income_limit)
    score += 20;

  return score;
}

function SchemeCard({ scheme, farmerInput }) {
  const matchScore = calculateMatchScore(scheme, farmerInput);

  return (
    <motion.div
      className="scheme-card"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      {matchScore >= 80 && (
        <div className="top-badge">⭐ Highly Eligible</div>
      )}

      <h3>{scheme.name}</h3>

      <div className="match-bar-container">
        <div
          className="match-bar"
          style={{ width: `${matchScore}%` }}
        />
      </div>

      <p><strong>Match Score:</strong> {matchScore}%</p>
      <p><strong>Why Recommended:</strong></p>
<ul>
  {scheme.state === farmerInput.state && <li>✔ State Eligible</li>}
  {scheme.crop === farmerInput.crop && <li>✔ Crop Match</li>}
  {scheme.category === farmerInput.category && <li>✔ Category Eligible</li>}
  {farmerInput.land >= scheme.min_land &&
    farmerInput.land <= scheme.max_land && <li>✔ Land Size Eligible</li>}
  {farmerInput.income <= scheme.income_limit && <li>✔ Income Eligible</li>}
</ul>
      <p><strong>Subsidy:</strong> ₹{scheme.subsidy}</p>
      <p><strong>Documents:</strong> {scheme.documents}</p>
      <p><strong>Deadline:</strong> {scheme.deadline}</p>
    </motion.div>
  );
}

export default SchemeCard;