import React from 'react';
import Card from '../common/Card';
import MetricCard from '../common/MetricCard';

const DrivingPatternCard = ({ pattern }) => (
  <Card className="p-8">
    <div className="text-gray-400 text-xs tracking-widest uppercase mb-5">
      DRIVING PATTERN ANALYSIS
    </div>
    <div className="grid grid-cols-3 gap-6">
      <MetricCard 
        label="Lane Keeping" 
        value={pattern.laneKeeping} 
        color="text-emerald-500" 
      />
      <MetricCard 
        label="Steering Input" 
        value={pattern.steeringInput} 
        color="text-cyan-500" 
      />
      <MetricCard 
        label="Speed Control" 
        value={pattern.speedControl} 
        color="text-emerald-500" 
      />
    </div>
  </Card>
);

export default DrivingPatternCard;
