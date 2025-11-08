import React from 'react';
import Card from '../common/Card';

const DetectionSystemCard = ({ status }) => (
  <Card variant="accent" borderColor="border-emerald-500" className="p-4 sm:p-6 lg:p-8">
    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-4 sm:mb-5 gap-2 sm:gap-0">
      <span className="text-white text-sm font-medium">Detection System</span>
      <span className="px-3 py-1 bg-emerald-500 text-white text-xs font-bold rounded tracking-wider">
        ACTIVE
      </span>
    </div>
    <div className="space-y-3">
      <div className="flex flex-col sm:flex-row justify-between text-sm gap-1 sm:gap-0">
        <span className="text-gray-400">Medical Event Detection</span>
        <span className="text-emerald-500">✓ {status.medical}</span>
      </div>
      <div className="flex flex-col sm:flex-row justify-between text-sm gap-1 sm:gap-0">
        <span className="text-gray-400">Collision Detection</span>
        <span className="text-emerald-500">✓ {status.collision}</span>
      </div>
      <div className="flex flex-col sm:flex-row justify-between text-sm gap-1 sm:gap-0">
        <span className="text-gray-400">Loss of Control</span>
        <span className="text-emerald-500">✓ {status.lossOfControl}</span>
      </div>
    </div>
  </Card>
);

export default DetectionSystemCard;