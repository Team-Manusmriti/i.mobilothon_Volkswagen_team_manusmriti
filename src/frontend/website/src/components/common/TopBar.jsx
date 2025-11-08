import React from 'react';
import { Shield } from 'lucide-react';

const TopBar = ({ currentTime = '14:32', temperature = '22°C' }) => (
  <div className="flex items-center justify-between px-4 sm:px-6 lg:px-12 pt-6 sm:pt-8 lg:pt-12 pb-4 sm:pb-6">
    <div className="flex items-center gap-3 sm:gap-4 lg:gap-6">
      <div className="w-8 h-8 sm:w-10 sm:h-10 bg-cyan-500 rounded-lg flex items-center justify-center">
        <Shield className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
      </div>
      <div>
        <div className="text-gray-400 text-xs tracking-wider uppercase">VIGILANCE AI</div>
        <div className="text-white text-xs sm:text-sm font-medium">Active Monitoring</div>
      </div>
    </div>
    <div className="flex items-center gap-4 sm:gap-6 lg:gap-8 text-gray-400 text-xs sm:text-sm">
      <span className="hidden sm:inline">{currentTime}</span>
      <span>{temperature}</span>
    </div>
  </div>
);

export default TopBar;