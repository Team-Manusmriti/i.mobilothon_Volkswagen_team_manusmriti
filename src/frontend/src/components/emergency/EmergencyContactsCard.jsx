import React from 'react';
import Card from '../common/Card';

const EmergencyContactsCard = ({ onEmergencyCall, onFamilyCall }) => (
  <Card className="p-8">
    <h3 className="text-white text-sm font-medium mb-5">
      Emergency Contacts
    </h3>
    <div className="flex gap-4">
      <button 
        onClick={onEmergencyCall}
        className="flex-1 h-12 bg-red-500 hover:bg-red-600 text-white font-bold rounded-lg transition-colors"
      >
        Emergency: 112
      </button>
      <button 
        onClick={onFamilyCall}
        className="flex-1 h-12 bg-gray-700 hover:bg-gray-600 text-white font-bold rounded-lg transition-colors"
      >
        Family Contact
      </button>
    </div>
  </Card>
);

export default EmergencyContactsCard;

