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
    <div className="px-4 sm:px-6 lg:px-12 py-4 sm:py-6 lg:py-8">
      <div className="flex items-center gap-3 sm:gap-4 mb-6 sm:mb-8">
        <div className="w-8 h-8 sm:w-10 sm:h-10 bg-red-500 rounded-lg flex items-center justify-center">
          <AlertTriangle className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
        </div>
        <div>
          <h1 className="text-white text-2xl sm:text-3xl font-bold">Emergency Protocol</h1>
          <p className="text-gray-400 text-xs">Automated Response System</p>
        </div>
      </div>

      <DetectionSystemCard status={emergencyData.detectionStatus} />
      
      <div className="mt-4 sm:mt-6">
        <ResponseSequenceCard steps={emergencyData.responseSteps} />
      </div>
      
      <div className="mt-4 sm:mt-6">
        <EmergencyContactsCard 
          onEmergencyCall={handleEmergencyCall}
          onFamilyCall={handleFamilyCall}
        />
      </div>
    </div>
  );
};

export default EmergencyProtocol;