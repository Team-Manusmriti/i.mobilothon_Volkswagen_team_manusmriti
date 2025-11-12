import React, { useState } from 'react';
import { Coffee, Music, Navigation, X } from 'lucide-react';
import Card from '../common/Card';

const AIAssistant = () => {
  const [suggestion, setSuggestion] = useState({
    title: 'Time for a break?',
    description: "You've been driving for 2 hours. There's a rest stop 5km ahead with good reviews.",
    icon: 'coffee'
  });
  
  const [interactions, setInteractions] = useState([
    { time: '10:30', msg: 'Suggested caffeine break - Accepted' },
    { time: '09:15', msg: 'Played focus playlist - Stress reduced by 15%' },
    { time: '08:45', msg: 'Morning greeting - Trip started' }
  ]);

  const [musicPlaying, setMusicPlaying] = useState(null);
  const [routeModal, setRouteModal] = useState(false);
  const [selectedRoute, setSelectedRoute] = useState('current');

  const musicPlaylists = [
    { id: 'calm', name: 'Calming Waves', duration: '45 min', tracks: 12, mood: 'Relaxing' },
    { id: 'focus', name: 'Focus Drive', duration: '60 min', tracks: 15, mood: 'Concentrated' },
    { id: 'energy', name: 'Energy Boost', duration: '30 min', tracks: 10, mood: 'Energetic' }
  ];

  const routes = [
    { 
      id: 'current', 
      name: 'Current Route', 
      distance: '45 km', 
      time: '45 min', 
      traffic: 'Moderate',
      trafficColor: 'text-yellow-500'
    },
    { 
      id: 'scenic', 
      name: 'Scenic Route', 
      distance: '52 km', 
      time: '55 min', 
      traffic: 'Light',
      trafficColor: 'text-emerald-500'
    },
    { 
      id: 'fastest', 
      name: 'Fastest Route', 
      distance: '43 km', 
      time: '40 min', 
      traffic: 'Heavy',
      trafficColor: 'text-red-500'
    }
  ];

  const actions = [
    { id: 1, title: 'Play Calming Music', desc: 'Reduce stress levels', icon: 'music' },
    { id: 2, title: 'Alternate Route', desc: 'Avoid heavy traffic', icon: 'navigation' }
  ];

  const executeAction = (actionId) => {
    const action = actions.find(a => a.id === actionId);
    
    if (actionId === 1) {
      setMusicPlaying(musicPlaylists[0]);
    } else if (actionId === 2) {
      setRouteModal(true);
    }
    
    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    const newInteraction = { time, msg: `${action?.title} - Initiated` };
    setInteractions(prev => [newInteraction, ...prev].slice(0, 5));
  };

  const selectMusic = (playlist) => {
    setMusicPlaying(playlist);
    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    setInteractions(prev => [
      { time, msg: `Playing "${playlist.name}" - ${playlist.mood} mood activated` },
      ...prev
    ].slice(0, 5));
  };

  const stopMusic = () => {
    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    setInteractions(prev => [
      { time, msg: `Stopped "${musicPlaying.name}"` },
      ...prev
    ].slice(0, 5));
    setMusicPlaying(null);
  };

  const changeRoute = (route) => {
    setSelectedRoute(route.id);
    setRouteModal(false);
    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    setInteractions(prev => [
      { time, msg: `Switched to ${route.name} - ETA: ${route.time}` },
      ...prev
    ].slice(0, 5));
  };

  return (
    <div className="px-4 sm:px-6 lg:px-12 py-4 sm:py-6 lg:py-8">
      <h1 className="text-white text-2xl sm:text-3xl font-bold mb-6">AI Assistant</h1>

      {/* AI Suggestion Card */}
      {suggestion && (
        <Card className="p-4 sm:p-6 mb-6 border-2 border-cyan-500">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 bg-cyan-500 rounded-lg flex items-center justify-center flex-shrink-0">
              <Coffee className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h3 className="text-white text-lg font-semibold mb-2">{suggestion.title}</h3>
              <p className="text-gray-400 text-sm mb-4">{suggestion.description}</p>
              <div className="flex gap-3">
                <button className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg text-sm font-medium transition-colors">
                  Accept
                </button>
                <button 
                  onClick={() => setSuggestion(null)}
                  className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm font-medium transition-colors"
                >
                  Dismiss
                </button>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Music Player - Now Playing */}
      {musicPlaying && (
        <Card className="p-4 sm:p-6 mb-6 border-2 border-purple-500">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center animate-pulse">
                <Music className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-white text-base sm:text-lg font-semibold">Now Playing</h3>
                <p className="text-gray-400 text-xs">Mood: {musicPlaying.mood}</p>
              </div>
            </div>
            <button
              onClick={stopMusic}
              className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-white" />
            </button>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-white font-medium text-sm sm:text-base">{musicPlaying.name}</span>
              <span className="text-gray-400 text-xs sm:text-sm">{musicPlaying.duration}</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-gray-400 mb-3">
              <span>{musicPlaying.tracks} tracks</span>
            </div>
            
            {/* Progress bar with animation */}
            <div className="w-full h-1 bg-gray-700 rounded-full overflow-hidden">
              <div 
                className="h-full bg-purple-500 rounded-full transition-all duration-1000"
                style={{ 
                  width: '40%',
                  animation: 'progress 3s ease-in-out infinite'
                }} 
              />
            </div>
          </div>
        </Card>
      )}

      {/* Context-Aware Actions */}
      <Card className="p-4 sm:p-6 mb-6">
        <h3 className="text-white text-sm font-medium mb-4">Context-Aware Actions</h3>
        <div className="space-y-3">
          {actions.map(action => (
            <button
              key={action.id}
              onClick={() => executeAction(action.id)}
              className="w-full p-4 bg-gray-800 hover:bg-gray-700 rounded-lg text-left transition-colors"
            >
              <div className="flex items-center gap-3">
                {action.icon === 'music' ? (
                  <Music className="w-5 h-5 text-cyan-500 flex-shrink-0" />
                ) : (
                  <Navigation className="w-5 h-5 text-cyan-500 flex-shrink-0" />
                )}
                <div>
                  <div className="text-white text-sm font-medium">{action.title}</div>
                  <div className="text-gray-400 text-xs">{action.desc}</div>
                </div>
              </div>
            </button>
          ))}
        </div>
      </Card>

      {/* Music Library */}
      {!musicPlaying && (
        <Card className="p-4 sm:p-6 mb-6">
          <h3 className="text-white text-sm font-medium mb-4">Music Library</h3>
          <div className="space-y-3">
            {musicPlaylists.map(playlist => (
              <button
                key={playlist.id}
                onClick={() => selectMusic(playlist)}
                className="w-full p-4 bg-gray-800 hover:bg-gray-700 rounded-lg text-left transition-colors group"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-purple-500 bg-opacity-20 rounded-lg flex items-center justify-center group-hover:bg-opacity-30 transition-colors">
                      <Music className="w-5 h-5 text-purple-500" />
                    </div>
                    <div>
                      <div className="text-white text-sm font-medium">{playlist.name}</div>
                      <div className="text-gray-400 text-xs">{playlist.tracks} tracks • {playlist.duration}</div>
                    </div>
                  </div>
                  <div className="text-xs text-gray-500 px-2 py-1 bg-gray-700 rounded">
                    {playlist.mood}
                  </div>
                </div>
              </button>
            ))}
          </div>
        </Card>
      )}

      {/* Current Route Info */}
      <Card className="p-4 sm:p-6 mb-6 border-2 border-blue-500">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-white text-sm font-medium">Current Route</h3>
          <button
            onClick={() => setRouteModal(true)}
            className="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white text-xs font-medium rounded transition-colors"
          >
            Change Route
          </button>
        </div>
        {routes.find(r => r.id === selectedRoute) && (
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-white font-medium text-sm sm:text-base">
                {routes.find(r => r.id === selectedRoute).name}
              </span>
              <span className={`text-xs font-medium ${routes.find(r => r.id === selectedRoute).trafficColor}`}>
                {routes.find(r => r.id === selectedRoute).traffic} Traffic
              </span>
            </div>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-400 text-xs">Distance</span>
                <div className="text-white font-medium">{routes.find(r => r.id === selectedRoute).distance}</div>
              </div>
              <div>
                <span className="text-gray-400 text-xs">ETA</span>
                <div className="text-white font-medium">{routes.find(r => r.id === selectedRoute).time}</div>
              </div>
            </div>
          </div>
        )}
      </Card>

      {/* Recent Interactions */}
      <Card className="p-4 sm:p-6">
        <h3 className="text-white text-sm font-medium mb-4">Recent Interactions</h3>
        <div className="space-y-3">
          {interactions.map((item, idx) => (
            <div key={idx} className="flex flex-col sm:flex-row justify-between items-start sm:items-center text-sm pb-3 border-b border-gray-800 last:border-0 gap-1 sm:gap-0">
              <span className="text-gray-400 text-xs sm:text-sm">{item.time}</span>
              <span className="text-white text-xs sm:text-sm sm:text-right flex-1 sm:ml-4">{item.msg}</span>
            </div>
          ))}
        </div>
      </Card>

      {/* Route Selection Modal */}
      {routeModal && (
        <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border-2 border-blue-500 rounded-lg max-w-lg w-full p-6 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-white text-xl font-bold">Select Route</h2>
              <button
                onClick={() => setRouteModal(false)}
                className="p-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-white" />
              </button>
            </div>

            <div className="space-y-3">
              {routes.map(route => (
                <button
                  key={route.id}
                  onClick={() => changeRoute(route)}
                  className={`w-full p-4 rounded-lg text-left transition-colors ${
                    selectedRoute === route.id
                      ? 'bg-blue-500 bg-opacity-20 border-2 border-blue-500'
                      : 'bg-gray-800 hover:bg-gray-700 border-2 border-transparent'
                  }`}
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-white font-semibold">{route.name}</span>
                    <span className={`text-xs font-medium px-2 py-1 rounded ${
                      route.traffic === 'Light' ? 'bg-emerald-500 bg-opacity-20 text-emerald-500' :
                      route.traffic === 'Moderate' ? 'bg-yellow-500 bg-opacity-20 text-yellow-500' :
                      'bg-red-500 bg-opacity-20 text-red-500'
                    }`}>
                      {route.traffic} Traffic
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-400 text-xs">Distance</span>
                      <div className="text-white font-medium">{route.distance}</div>
                    </div>
                    <div>
                      <span className="text-gray-400 text-xs">Time</span>
                      <div className="text-white font-medium">{route.time}</div>
                    </div>
                  </div>
                </button>
              ))}
            </div>

            <div className="mt-6 p-4 bg-gray-800 rounded-lg">
              <div className="flex items-start gap-2">
                <Navigation className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                <p className="text-gray-400 text-xs">
                  Route recommendations are based on real-time traffic data and your current driving conditions.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes progress {
          0% { width: 0%; }
          50% { width: 60%; }
          100% { width: 0%; }
        }
      `}</style>
    </div>
  );
};

export default AIAssistant;