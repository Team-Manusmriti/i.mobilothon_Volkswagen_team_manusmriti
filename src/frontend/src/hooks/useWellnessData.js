import { useState, useEffect } from 'react';

export const useWellnessData = () => {
  const [data, setData] = useState({
    wellnessScore: 94,
    perclos: 4.2,
    heartRate: 72,
    alertness: 98,
    stress: 'Low',
    fatigue: 12,
    emotion: { name: 'Calm & Focused', confidence: 85 },
    drivingPattern: {
      laneKeeping: 'Stable',
      steeringInput: 'Smooth',
      speedControl: 'Steady'
    }
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refresh = () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setData(prev => ({
        ...prev,
        wellnessScore: Math.floor(90 + Math.random() * 10),
        perclos: (3 + Math.random() * 2).toFixed(1),
        heartRate: Math.floor(68 + Math.random() * 8),
        alertness: Math.floor(95 + Math.random() * 5)
      }));
      setLoading(false);
    }, 500);
  };

  // Auto-refresh every 5 seconds
  useEffect(() => {
    const interval = setInterval(refresh, 5000);
    return () => clearInterval(interval);
  }, []);

  return { ...data, loading, error, refresh };
};