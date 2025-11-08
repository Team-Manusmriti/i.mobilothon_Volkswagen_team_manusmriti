import { useState } from 'react';
import { Menu, X } from 'lucide-react';
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
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

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

  const tabs = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'wellness', label: 'Wellness' },
    { id: 'emergency', label: 'Emergency' },
    { id: 'copilot', label: 'AI Co-Pilot' }
  ];

  return (
    <div className="bg-gray-950 text-white">
      <div className="max-w-[1920px] mx-auto min-h-screen">
        <TopBar />
        
        {/* Navigation */}
        <div className="px-4 sm:px-6 lg:px-12 mt-4">
          {/* Mobile Menu Button */}
          <div className="md:hidden flex justify-between items-center border-b border-gray-800 pb-4">
            <h2 className="text-lg font-medium text-white capitalize">{currentScreen.replace('copilot', 'AI Co-Pilot')}</h2>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-gray-400 hover:text-white transition-colors"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden mt-4 space-y-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => {
                    setCurrentScreen(tab.id as Screen);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                    currentScreen === tab.id
                      ? 'bg-cyan-500/20 text-cyan-500 border border-cyan-500/30'
                      : 'text-gray-400 hover:text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          )}

          {/* Desktop Tabs */}
          <div className="hidden md:flex gap-2 border-b border-gray-800 overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setCurrentScreen(tab.id as Screen)}
                className={`px-4 lg:px-6 py-3 text-sm font-medium transition-colors border-b-2 whitespace-nowrap ${
                  currentScreen === tab.id
                    ? 'border-cyan-500 text-cyan-500'
                    : 'border-transparent text-gray-400 hover:text-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Screen Content */}
        <div className={mobileMenuOpen ? 'hidden md:block' : 'block'}>
          {renderScreen()}
        </div>
        
        <BottomBar />
      </div>
    </div>
  );
}