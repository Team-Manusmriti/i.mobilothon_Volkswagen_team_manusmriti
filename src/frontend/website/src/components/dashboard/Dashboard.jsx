import React, { useEffect, useState } from 'react';
import { useWellnessData } from '../../hooks/useWellnessData';
import { useVehicleConnection } from '../../hooks/useVehicleConnection';
import WellnessScoreCard from './WellnessScoreCard';
import QuickActionsPanel from './QuickActionsPanel';

const Dashboard = () => {
  const wellnessData = useWellnessData();
  const vehicleData = useVehicleConnection();

  // Speed state from CARLA WebSocket
  const [speed, setSpeed] = useState(0);

  useEffect(() => {
    // ✅ Create WebSocket only once when component loads
    const ws = new WebSocket('ws://localhost:8008/ws/speed');

    // ✅ Listen for incoming messages
    ws.onmessage = (event) => {
      try {
        console.log('Received WebSocket data:', event.data);
        const data = JSON.parse(event.data);
        if (data?.speed !== undefined) {
          setSpeed(data.speed);
        }
      } catch (error) {
        console.log('Error parsing WebSocket data:', error);
      }
    };

    // ✅ On WebSocket open
    ws.onopen = () => {
      console.log('✅ Connected to CARLA WebSocket');
    };

    // ✅ On Error
    ws.onerror = (error) => {
      console.log('❌ WebSocket Error:', error);
    };

    // ✅ Cleanup WebSocket on component unmount
    return () => {
      ws.close();
      console.log('❎ WebSocket Closed');
    };
  }, []); // Empty dependency → runs only once

  return (
    <div className="flex flex-col lg:flex-row gap-4 sm:gap-6 px-4 sm:px-6 lg:px-12 py-4 sm:py-6 lg:py-8">
      <WellnessScoreCard
        score={wellnessData.wellnessScore}
        condition="Optimal Condition"
        metrics={{
          alertness: wellnessData.alertness,
          stress: wellnessData.stress,
          speed: speed.toFixed(2) + ' km/h'  // ✅ Display speed neatly
        }}
      />
      <QuickActionsPanel
        copilotStatus="Ready to assist"
        tripTime={vehicleData.tripTime}
        destination={vehicleData.destination}
      />
    </div>
  );
};

export default Dashboard;
