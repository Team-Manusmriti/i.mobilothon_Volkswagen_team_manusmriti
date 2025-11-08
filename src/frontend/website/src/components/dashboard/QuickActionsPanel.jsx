import React from 'react';
import { Brain, Activity, Navigation } from 'lucide-react';
import Card from '../common/Card';

const QuickActionsPanel = ({ copilotStatus, tripTime, destination }) => (
  <div className="w-full lg:w-80 grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-1 gap-4">
    <Card className="p-4 sm:p-6">
      <Brain className="w-5 h-5 sm:w-6 sm:h-6 text-cyan-500 mb-3" />
      <div className="text-gray-400 text-xs tracking-wider uppercase mb-1">
        AI CO-PILOT
      </div>
      <div className="text-white text-sm">{copilotStatus}</div>
    </Card>
    
    <Card className="p-4 sm:p-6">
      <Activity className="w-5 h-5 sm:w-6 sm:h-6 text-emerald-500 mb-3" />
      <div className="text-gray-400 text-xs tracking-wider uppercase mb-1">
        TRIP TIME
      </div>
      <div className="text-white text-base font-medium">{tripTime}</div>
    </Card>
    
    <Card className="p-4 sm:p-6">
      <Navigation className="w-5 h-5 sm:w-6 sm:h-6 text-blue-500 mb-3" />
      <div className="text-gray-400 text-xs tracking-wider uppercase mb-1">
        DESTINATION
      </div>
      <div className="text-white text-sm">{destination}</div>
    </Card>
  </div>
);

export default QuickActionsPanel;
