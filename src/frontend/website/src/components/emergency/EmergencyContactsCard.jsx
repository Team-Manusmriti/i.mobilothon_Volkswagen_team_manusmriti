import React from 'react';
import Card from '../common/Card';

const EmergencyContactsCard = ({ onEmergencyCall, onFamilyCall }) => (
  <Card className="p-4 sm:p-6 lg:p-8">
    <h3 className="text-white text-sm font-medium mb-4 sm:mb-5">
      Emergency Contacts
    </h3>
    <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
      <button 
        onClick={onEmergencyCall}
        className="flex-1 h-10 sm:h-12 bg-red-500 hover:bg-red-600 text-white font-bold rounded-lg transition-colors text-sm sm:text-base"
      >
        Emergency: 112
      </button>
      <button 
        onClick={onFamilyCall}
        className="flex-1 h-10 sm:h-12 bg-gray-700 hover:bg-gray-600 text-white font-bold rounded-lg transition-colors text-sm sm:text-base"
      >
        Family Contact
      </button>
    </div>
  </Card>
);

export default EmergencyContactsCard;

