import React, { useEffect, useState } from 'react';
import { useWellnessData } from '../../hooks/useWellnessData';
import { useVehicleConnection } from '../../hooks/useVehicleConnection';
import WellnessScoreCard from './WellnessScoreCard';
import QuickActionsPanel from './QuickActionsPanel';

const Dashboard = () => {
  const wellnessData = useWellnessData();
  const vehicleData = useVehicleConnection();

  // Speed state from CARLA WebSocket with fallback
  const [speed, setSpeed] = useState(0);
  const [isConnected, setIsConnected] = useState(false);
  const [useSimulation, setUseSimulation] = useState(false);

  useEffect(() => {
    let ws = null;
    let simulationInterval = null;
    let connectionTimeout = null;

    // Try to connect to WebSocket
    try {
      ws = new WebSocket('ws://localhost:8008/ws/speed');

      // Set timeout for connection
      connectionTimeout = setTimeout(() => {
        if (!isConnected) {
          console.log('WebSocket connection timeout, switching to simulation mode');
          setUseSimulation(true);
          if (ws) ws.close();
        }
      }, 3000);

      ws.onopen = () => {
        console.log('✅ Connected to CARLA WebSocket on port 8008');
        setIsConnected(true);
        setUseSimulation(false);
        clearTimeout(connectionTimeout);
      };

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

      ws.onerror = (error) => {
        console.log('❌ WebSocket Error:', error);
        setUseSimulation(true);
        setIsConnected(false);
      };

      ws.onclose = () => {
        console.log('⏸ WebSocket Closed');
        setIsConnected(false);
        setUseSimulation(true);
      };
    } catch (error) {
      console.log('Failed to create WebSocket:', error);
      setUseSimulation(true);
    }

    // Simulation fallback
    if (useSimulation) {
      simulationInterval = setInterval(() => {
        // Simulate realistic speed changes
        setSpeed(prevSpeed => {
          const variation = (Math.random() - 0.5) * 5;
          const newSpeed = Math.max(0, Math.min(120, prevSpeed + variation));
          return newSpeed || (65 + Math.random() * 10);
        });
      }, 2000);
    }

    return () => {
      if (ws) ws.close();
      if (simulationInterval) clearInterval(simulationInterval);
      if (connectionTimeout) clearTimeout(connectionTimeout);
    };
  }, []);

  return (
    <div className="flex flex-col lg:flex-row gap-4 sm:gap-6 px-4 sm:px-6 lg:px-12 py-4 sm:py-6 lg:py-8">
      <WellnessScoreCard
        score={wellnessData.wellnessScore}
        condition="Optimal Condition"
        metrics={{
          alertness: wellnessData.alertness,
          stress: wellnessData.stress,
          speed: speed.toFixed(2) + ' km/h'
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