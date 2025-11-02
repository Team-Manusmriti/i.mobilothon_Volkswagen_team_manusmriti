import React from 'react';
import Card from '../common/Card';

const ConversationHistory = ({ interactions }) => (
  <Card className="p-6">
    <div className="text-gray-400 text-xs tracking-widest uppercase mb-5">
      RECENT INTERACTIONS
    </div>
    <div className="space-y-4">
      {interactions.map((interaction, idx) => (
        <div key={idx} className="flex gap-3 text-sm">
          <span className="text-gray-500 min-w-[48px]">{interaction.time}</span>
          <span className="text-gray-300">{interaction.msg}</span>
        </div>
      ))}
    </div>
  </Card>
);

export default ConversationHistory;