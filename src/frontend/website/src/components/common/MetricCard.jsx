import React from 'react';

const MetricCard = ({ label, value, color = 'text-cyan-500' }) => (
  <div className="text-center">
    <div className="text-gray-400 text-xs mb-1">{label}</div>
    <div className={`${color} text-lg sm:text-xl lg:text-2xl font-bold`}>{value}</div>
  </div>
);

export default MetricCard;