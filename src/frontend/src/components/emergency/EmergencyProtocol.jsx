import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { useEmergencySystem } from '../../hooks/useEmergencySystem';
import DetectionSystemCard from './DetectionSystemCard';
import ResponseSequenceCard from './ResponseSequenceCard';
import EmergencyContactsCard from './EmergencyContactsCard';

const EmergencyProtocol = () => {
  const emergencyData = useEmergencySystem();

  const handleEmergencyCall = () => {
    console.log('Calling Emergency: 112');
    emergencyData.contactEmergency('emergency');
  };

  const handleFamilyCall = () => {
    console.log('Calling Family Contact');
    emergencyData.contactEmergency('family');
  };

  return (
    <div className="px-12 py-8">
      <div className="flex items-center gap-4 mb-8">
        <div className="w-10 h-10 bg-red-500 rounded-lg flex items-center justify-center">
          <AlertTriangle className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-white text-3xl font-bold">Emergency Protocol</h1>
          <p className="text-gray-400 text-xs">Automated Response System</p>
        </div>
      </div>

      <DetectionSystemCard status={emergencyData.detectionStatus} />
      
      <div className="mt-6">
        <ResponseSequenceCard steps={emergencyData.responseSteps} />
      </div>
      
      <div className="mt-6">
        <EmergencyContactsCard 
          onEmergencyCall={handleEmergencyCall}
          onFamilyCall={handleFamilyCall}
        />
      </div>
    </div>
  );
};

export default EmergencyProtocol;