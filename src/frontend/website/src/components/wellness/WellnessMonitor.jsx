import { useWellnessData } from '../../hooks/useWellnessData';
import PrimaryMetricCard from './PrimaryMetricCard';
import EmotionRecognitionCard from './EmotionRecognitionCard';
import DrivingPatternCard from './DrivingPatternCard';
import { useEffect, useState } from 'react';

const WellnessMonitor = () => {
  const wellnessData = useWellnessData();
  const [emotion, setEmotion] = useState("unknown");
  const [state, setState] = useState("unknown");
  const [isConnected, setIsConnected] = useState(false);
  const [useSimulation, setUseSimulation] = useState(false);

  useEffect(() => {
    let ws = null;
    let simulationInterval = null;
    let connectionTimeout = null;

    // Try to connect to WebSocket
    try {
      ws = new WebSocket("ws://localhost:8008/ws/emotion");

      // Set timeout for connection
      connectionTimeout = setTimeout(() => {
        if (!isConnected) {
          console.log('Emotion WebSocket connection timeout, switching to simulation mode');
          setUseSimulation(true);
          if (ws) ws.close();
        }
      }, 3000);

      ws.onopen = () => {
        console.log("✅ Emotion WebSocket Connected on port 8008");
        setIsConnected(true);
        setUseSimulation(false);
        clearTimeout(connectionTimeout);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log("Received Emotion WebSocket data:", data);
          if (data?.emotion) setEmotion(data.emotion);
          if (data?.state) setState(data.state);
        } catch (error) {
          console.log("Error parsing emotion data:", error);
        }
      };

      ws.onerror = (err) => {
        console.log("❌ Emotion WebSocket Error", err);
        setUseSimulation(true);
        setIsConnected(false);
      };

      ws.onclose = () => {
        console.log("⏸ Emotion WebSocket Closed");
        setIsConnected(false);
        setUseSimulation(true);
      };
    } catch (error) {
      console.log('Failed to create emotion WebSocket:', error);
      setUseSimulation(true);
    }

    // Simulation fallback
    if (useSimulation) {
      const emotions = ['Calm & Focused', 'Alert', 'Relaxed', 'Concentrated', 'Happy'];
      const states = ['normal', 'attentive', 'focused'];
      
      simulationInterval = setInterval(() => {
        setEmotion(emotions[Math.floor(Math.random() * emotions.length)]);
        setState(states[Math.floor(Math.random() * states.length)]);
      }, 5000);
    }

    return () => {
      if (ws) ws.close();
      if (simulationInterval) clearInterval(simulationInterval);
      if (connectionTimeout) clearTimeout(connectionTimeout);
    };
  }, []);

  return (
    <div className="px-4 sm:px-6 lg:px-12 py-4 sm:py-6 lg:py-8">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6">
        <h1 className="text-white text-2xl sm:text-3xl font-bold mb-2 sm:mb-0">Wellness Monitor</h1>
        <div className="flex items-center gap-2">
          <span className="text-gray-400 text-xs">Real-time Analysis</span>
          {useSimulation && (
            <span className="px-2 py-1 bg-yellow-500 bg-opacity-20 border border-yellow-500 rounded text-yellow-500 text-xs font-medium">
              Simulated
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6">
        <PrimaryMetricCard
          label="EYE ACTIVITY (PERCLOS)"
          value={`${wellnessData.perclos}%`}
          status="Within safe range"
          borderColor="border-cyan-500"
          valueColor="text-cyan-500"
        />
        <PrimaryMetricCard
          label="HEART RATE"
          value={`${wellnessData.heartRate} BPM`}
          status="Normal rhythm"
          borderColor="border-blue-500"
          valueColor="text-blue-500"
        />
      </div>

      <EmotionRecognitionCard
        emotion={emotion}
        confidence={wellnessData.emotion.confidence}
      />
      
      <div className="mt-4 sm:mt-6">
        <DrivingPatternCard pattern={wellnessData.drivingPattern} />
      </div>
    </div>
  );
};

export default WellnessMonitor;