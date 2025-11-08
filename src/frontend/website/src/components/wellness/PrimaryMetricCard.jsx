import React from 'react';
import Card from '../common/Card';

const PrimaryMetricCard = ({ label, value, status, borderColor, valueColor }) => (
  <Card variant="accent" borderColor={borderColor} className="p-4 sm:p-6 lg:p-8">
    <div className="text-gray-400 text-xs tracking-widest uppercase mb-3 sm:mb-4">
      {label}
    </div>
    <div className={`${valueColor} text-3xl sm:text-4xl lg:text-5xl font-bold mb-2 sm:mb-3`}>
      {value}
    </div>
    <div className="text-emerald-500 text-xs">{status}</div>
  </Card>
);

export default PrimaryMetricCard;