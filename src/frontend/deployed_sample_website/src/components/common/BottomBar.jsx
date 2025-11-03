import React from 'react';
import { Settings } from 'lucide-react';

const BottomBar = ({ systemActive, vehicleConnected }) => (
  <div className="flex items-center justify-between px-12 py-4">
    <div className="flex items-center gap-6">
      <div className="flex items-center gap-2">
        <div className={`w-2 h-2 rounded-full ${systemActive ? 'bg-emerald-500' : 'bg-gray-500'}`} />
        <span className={`text-xs font-medium ${systemActive ? 'text-emerald-500' : 'text-gray-500'}`}>
          System {systemActive ? 'Active' : 'Inactive'}
        </span>
      </div>
      <span className="text-gray-400 text-xs">
        Vehicle: {vehicleConnected ? 'Connected' : 'Disconnected'}
      </span>
    </div>
    <Settings className="w-4 h-4 text-gray-500 cursor-pointer hover:text-gray-300 transition-colors" />
  </div>
);

export default BottomBar;