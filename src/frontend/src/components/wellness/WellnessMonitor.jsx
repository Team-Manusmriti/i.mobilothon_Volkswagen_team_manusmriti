
import { useWellnessData } from '../../hooks/useWellnessData';
import PrimaryMetricCard from './PrimaryMetricCard';
import EmotionRecognitionCard from './EmotionRecognitionCard';
import DrivingPatternCard from './DrivingPatternCard';

const WellnessMonitor = () => {
  const wellnessData = useWellnessData();

  return (
    <div className="px-12 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-white text-3xl font-bold">Wellness Monitor</h1>
        <span className="text-gray-400 text-xs">Real-time Analysis</span>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-6">
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
        emotion={wellnessData.emotion.name}
        confidence={wellnessData.emotion.confidence}
      />
      
      <div className="mt-6">
        <DrivingPatternCard pattern={wellnessData.drivingPattern} />
      </div>
    </div>
  );
};

export default WellnessMonitor;