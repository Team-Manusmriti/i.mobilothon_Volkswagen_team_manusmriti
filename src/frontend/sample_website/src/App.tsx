import { useState } from 'react';
// @ts-ignore
import TopBar from './components/common/TopBar.jsx';
// @ts-ignore
import BottomBar from './components/common/BottomBar.jsx';
// @ts-ignore
import Dashboard from './components/dashboard/Dashboard.jsx';
// @ts-ignore
import WellnessMonitor from './components/wellness/WellnessMonitor.jsx';
// @ts-ignore
import EmergencyProtocol from './components/emergency/EmergencyProtocol.jsx';
// @ts-ignore
import AICoPilot from './components/copilot/AICoPilot.jsx';

type Screen = 'dashboard' | 'wellness' | 'emergency' | 'copilot';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('dashboard');

  const renderScreen = () => {
    switch (currentScreen) {
      case 'dashboard':
        return <Dashboard />;
      case 'wellness':
        return <WellnessMonitor />;
      case 'emergency':
        return <EmergencyProtocol />;
      case 'copilot':
        return <AICoPilot />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="max-w-[1920px] mx-auto">
        <TopBar />
        
        {/* Navigation Tabs */}
        <div className="px-12 mt-4">
          <div className="flex gap-2 border-b border-gray-800">
            <button
              onClick={() => setCurrentScreen('dashboard')}
              className={`px-6 py-3 text-[14px] font-medium transition-colors border-b-2 ${
                currentScreen === 'dashboard'
                  ? 'border-cyan-500 text-cyan-500'
                  : 'border-transparent text-gray-400 hover:text-gray-300'
              }`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setCurrentScreen('wellness')}
              className={`px-6 py-3 text-[14px] font-medium transition-colors border-b-2 ${
                currentScreen === 'wellness'
                  ? 'border-cyan-500 text-cyan-500'
                  : 'border-transparent text-gray-400 hover:text-gray-300'
              }`}
            >
              Wellness Monitor
            </button>
            <button
              onClick={() => setCurrentScreen('emergency')}
              className={`px-6 py-3 text-[14px] font-medium transition-colors border-b-2 ${
                currentScreen === 'emergency'
                  ? 'border-cyan-500 text-cyan-500'
                  : 'border-transparent text-gray-400 hover:text-gray-300'
              }`}
            >
              Emergency Protocol
            </button>
            <button
              onClick={() => setCurrentScreen('copilot')}
              className={`px-6 py-3 text-[14px] font-medium transition-colors border-b-2 ${
                currentScreen === 'copilot'
                  ? 'border-cyan-500 text-cyan-500'
                  : 'border-transparent text-gray-400 hover:text-gray-300'
              }`}
            >
              AI Co-Pilot
            </button>
          </div>
        </div>

        {/* Screen Content */}
        {renderScreen()}
        
        <BottomBar />
      </div>
    </div>
  );
}