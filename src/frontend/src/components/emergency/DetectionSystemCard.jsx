import React from 'react';
import Card from '../common/Card';

const DetectionSystemCard = ({ status }) => (
  <Card variant="accent" borderColor="border-emerald-500" className="p-8">
    <div className="flex items-center justify-between mb-5">
      <span className="text-white text-sm font-medium">Detection System</span>
      <span className="px-3 py-1 bg-emerald-500 text-white text-xs font-bold rounded tracking-wider">
        ACTIVE
      </span>
    </div>
    <div className="space-y-3">
      <div className="flex justify-between text-sm">
        <span className="text-gray-400">Medical Event Detection</span>
        <span className="text-emerald-500">✓ {status.medical}</span>
      </div>
      <div className="flex justify-between text-sm">
        <span className="text-gray-400">Collision Detection</span>
        <span className="text-emerald-500">✓ {status.collision}</span>
      </div>
      <div className="flex justify-between text-sm">
        <span className="text-gray-400">Loss of Control</span>
        <span className="text-emerald-500">✓ {status.lossOfControl}</span>
      </div>
    </div>
  </Card>
);

export default DetectionSystemCard;