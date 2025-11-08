import React from 'react';
import { Heart } from 'lucide-react';
import Card from '../common/Card';
import MetricCard from '../common/MetricCard';

const WellnessScoreCard = ({ score, condition, metrics }) => (
  <Card className="flex-1 p-4 sm:p-6 lg:p-8">
    <div className="flex flex-col sm:flex-row items-start justify-between mb-6 sm:mb-8">
      <div className="mb-4 sm:mb-0">
        <div className="text-gray-400 text-xs tracking-widest uppercase mb-2">
          DRIVER WELLNESS
        </div>
        <div className="text-cyan-500 text-4xl sm:text-5xl lg:text-6xl font-bold mb-2">{score}</div>
        <div className="text-emerald-500 text-sm font-medium">{condition}</div>
      </div>
      <div className="w-16 h-16 sm:w-20 sm:h-20 lg:w-24 lg:h-24 rounded-full border-4 border-cyan-500 flex items-center justify-center">
        <Heart className="w-6 h-6 sm:w-8 sm:h-8 lg:w-10 lg:h-10 text-cyan-500" />
      </div>
    </div>
    
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6 sm:mt-8">
      <MetricCard 
        label="Alertness" 
        value={`${metrics.alertness}%`} 
        color="text-emerald-500" 
      />
      <MetricCard 
        label="Speed" 
        value={`${metrics.speed}`} 
        color="text-emerald-500" 
      />
      <MetricCard 
        label="Stress" 
        value={metrics.stress} 
        color="text-cyan-500" 
      />
    </div>
  </Card>
);

export default WellnessScoreCard;