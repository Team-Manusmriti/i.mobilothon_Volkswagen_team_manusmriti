import React, { useState, useEffect } from 'react';
// Use the AppProvider at the root (main.tsx) — do not re-wrap here
// @ts-ignore
import Dashboard from './components/dashboard/Dashboard';
// @ts-ignore
import WellnessMonitor from './components/wellness/WellnessMonitor';
// @ts-ignore
import EmergencyProtocol from './components/emergency/EmergencyProtocol';
// @ts-ignore
import AIAssistant from './components/copilot/AICoPilot';
import { Brain, AlertTriangle, X } from 'lucide-react';

// Use the shared DemoDisclaimerModal component
// @ts-ignore
import DemoDisclaimerModal from './components/common/DemoDisclaimerModal.jsx';

// debug: confirm App renders
console.log('App component initializing');

const App = () => {
  const [showDisclaimer, setShowDisclaimer] = useState(true);
  const [activeScreen, setActiveScreen] = useState('dashboard');
  const [currentTime, setCurrentTime] = useState('12:45 PM');

  // Update time every minute
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const hours = now.getHours();
      const minutes = now.getMinutes();
      const ampm = hours >= 12 ? 'PM' : 'AM';
      const displayHours = hours % 12 || 12;
      setCurrentTime(`${displayHours}:${minutes.toString().padStart(2, '0')} ${ampm}`);
    };

    updateTime();
    const interval = setInterval(updateTime, 60000);
    return () => clearInterval(interval);
  }, []);

  // Check if disclaimer should be shown (check localStorage)
  useEffect(() => {
    const seen = localStorage.getItem('demoDisclaimerSeen') || localStorage.getItem('hasSeenDisclaimer');
    if (seen === 'true') setShowDisclaimer(false);
  }, []);

  const handleCloseDisclaimer = () => {
    setShowDisclaimer(false);
    localStorage.setItem('demoDisclaimerSeen', 'true');
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'wellness', label: 'Wellness' },
    { id: 'assistant', label: 'AI Assistant' },
    { id: 'emergency', label: 'Emergency' }
  ];

  return (
      <div className="min-h-screen bg-black">
        {showDisclaimer && <DemoDisclaimerModal open={showDisclaimer} onClose={handleCloseDisclaimer} />}
        
        {/* Header */}
        <div className="bg-gray-900 border-b border-gray-800 px-4 sm:px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-lg flex items-center justify-center">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-white text-lg sm:text-xl font-bold">VigilanceAI</h1>
                <p className="text-gray-400 text-xs">Driver Wellness System</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="text-right hidden sm:block">
                <div className="text-white text-sm font-medium">{currentTime}</div>
                <div className="text-gray-400 text-xs">23°C</div>
              </div>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="bg-gray-900 border-b border-gray-800 px-4 sm:px-6">
          <div className="flex gap-1 overflow-x-auto">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => setActiveScreen(item.id)}
                className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors ${
                  activeScreen === item.id
                    ? 'text-cyan-500 border-b-2 border-cyan-500'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="pb-8">
          {activeScreen === 'dashboard' && <Dashboard />}
          {activeScreen === 'wellness' && <WellnessMonitor />}
          {activeScreen === 'assistant' && <AIAssistant />}
          {activeScreen === 'emergency' && <EmergencyProtocol />}
        </div>
        </div>
  );
};

export default App;