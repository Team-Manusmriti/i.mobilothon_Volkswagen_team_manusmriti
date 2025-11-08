
import { useWellnessData } from '../../hooks/useWellnessData';
import PrimaryMetricCard from './PrimaryMetricCard';
import EmotionRecognitionCard from './EmotionRecognitionCard';
import DrivingPatternCard from './DrivingPatternCard';
import { useEffect, useState } from 'react';

const WellnessMonitor = () => {
  const wellnessData = useWellnessData();
  const [emotion, setEmotion] = useState("unknown");
  const [state, setState] = useState("unknown");

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8008/ws/emotion");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Received Emotion WebSocket data:", data);
      setEmotion(data.emotion);
      setState(data.state);
    };

    ws.onopen = () => console.log("✅ Emotion WebSocket Connected on port 8008");
    ws.onerror = (err) => console.log("❌ WebSocket Error", err);
    return () => ws.close();
  }, []);

  return (
    <div className="px-4 sm:px-6 lg:px-12 py-4 sm:py-6 lg:py-8">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6">
        <h1 className="text-white text-2xl sm:text-3xl font-bold mb-2 sm:mb-0">Wellness Monitor</h1>
        <span className="text-gray-400 text-xs">Real-time Analysis</span>
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