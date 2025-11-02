import React from 'react';
import { Brain, Activity, Navigation } from 'lucide-react';
import Card from '../common/Card';

const QuickActionsPanel = ({ copilotStatus, tripTime, destination }) => (
  <div className="w-80 flex flex-col gap-4">
    <Card className="p-6">
      <Brain className="w-6 h-6 text-cyan-500 mb-3" />
      <div className="text-gray-400 text-xs tracking-wider uppercase mb-1">
        AI CO-PILOT
      </div>
      <div className="text-white text-sm">{copilotStatus}</div>
    </Card>
    
    <Card className="p-6">
      <Activity className="w-6 h-6 text-emerald-500 mb-3" />
      <div className="text-gray-400 text-xs tracking-wider uppercase mb-1">
        TRIP TIME
      </div>
      <div className="text-white text-base font-medium">{tripTime}</div>
    </Card>
    
    <Card className="p-6">
      <Navigation className="w-6 h-6 text-blue-500 mb-3" />
      <div className="text-gray-400 text-xs tracking-wider uppercase mb-1">
        DESTINATION
      </div>
      <div className="text-white text-sm">{destination}</div>
    </Card>
  </div>
);

export default QuickActionsPanel;
