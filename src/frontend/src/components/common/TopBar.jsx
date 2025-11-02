import React from 'react';
import { Shield } from 'lucide-react';

const TopBar = ({ currentTime, temperature }) => (
  <div className="flex items-center justify-between px-12 pt-12 pb-6">
    <div className="flex items-center gap-6">
      <div className="w-10 h-10 bg-cyan-500 rounded-lg flex items-center justify-center">
        <Shield className="w-6 h-6 text-white" />
      </div>
      <div>
        <div className="text-gray-400 text-xs tracking-wider uppercase">VIGILANCE AI</div>
        <div className="text-white text-sm font-medium">Active Monitoring</div>
      </div>
    </div>
    <div className="flex items-center gap-8 text-gray-400 text-sm">
      <span>{currentTime}</span>
      <span>{temperature}</span>
    </div>
  </div>
);

export default TopBar;