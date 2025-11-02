import React from 'react';
import { Music, Navigation } from 'lucide-react';
import Card from '../common/Card';

const ActionGrid = ({ actions, onActionClick }) => (
  <div className="grid grid-cols-2 gap-6">
    {actions.map((action) => (
      <Card
        key={action.id}
        className="p-6 cursor-pointer border border-gray-700 hover:border-cyan-500 transition-colors"
        onClick={() => onActionClick(action.id)}
      >
        {action.icon === 'music' ? (
          <Music className="w-5 h-5 text-blue-500 mb-4" />
        ) : (
          <Navigation className="w-5 h-5 text-emerald-500 mb-4" />
        )}
        <h4 className="text-white text-sm font-medium mb-1">{action.title}</h4>
        <p className="text-gray-400 text-xs">{action.desc}</p>
      </Card>
    ))}
  </div>
);

export default ActionGrid;