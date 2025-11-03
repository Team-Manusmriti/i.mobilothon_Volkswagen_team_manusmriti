import React from 'react';
import { useWellnessData } from '../../hooks/useWellnessData';
import { useVehicleConnection } from '../../hooks/useVehicleConnection';
import WellnessScoreCard from './WellnessScoreCard';
import QuickActionsPanel from './QuickActionsPanel';

const Dashboard = () => {
  const wellnessData = useWellnessData();
  const vehicleData = useVehicleConnection();

  return (
    <div className="flex gap-6 px-12 py-8">
      <WellnessScoreCard
        score={wellnessData.wellnessScore}
        condition="Optimal Condition"
        metrics={{
          alertness: wellnessData.alertness,
          stress: wellnessData.stress,
          fatigue: wellnessData.fatigue
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