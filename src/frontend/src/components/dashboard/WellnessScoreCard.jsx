import React from 'react';
import { Heart } from 'lucide-react';
import Card from '../common/Card';
import MetricCard from '../common/MetricCard';

const WellnessScoreCard = ({ score, condition, metrics }) => (
  <Card className="flex-1 p-8">
    <div className="flex items-start justify-between mb-8">
      <div>
        <div className="text-gray-400 text-xs tracking-widest uppercase mb-2">
          DRIVER WELLNESS
        </div>
        <div className="text-cyan-500 text-6xl font-bold mb-2">{score}</div>
        <div className="text-emerald-500 text-sm font-medium">{condition}</div>
      </div>
      <div className="w-24 h-24 rounded-full border-4 border-cyan-500 flex items-center justify-center">
        <Heart className="w-10 h-10 text-cyan-500" />
      </div>
    </div>
    
    <div className="grid grid-cols-3 gap-4 mt-8">
      <MetricCard 
        label="Alertness" 
        value={`${metrics.alertness}%`} 
        color="text-emerald-500" 
      />
      <MetricCard 
        label="Stress" 
        value={metrics.stress} 
        color="text-cyan-500" 
      />
      <MetricCard 
        label="Fatigue" 
        value={`${metrics.fatigue}%`} 
        color="text-emerald-500" 
      />
    </div>
  </Card>
);

export default WellnessScoreCard;