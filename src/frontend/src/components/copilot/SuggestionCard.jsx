import React from 'react';
import { Coffee } from 'lucide-react';
import Card from '../common/Card';

const SuggestionCard = ({ title, description, onNavigate, onRemind }) => (
  <Card variant="gradient" className="p-8">
    <div className="flex items-start gap-4 mb-6">
      <Coffee className="w-6 h-6 text-white flex-shrink-0 mt-1" />
      <div>
        <h3 className="text-white text-lg font-bold mb-2">{title}</h3>
        <p className="text-white/90 text-sm leading-relaxed">{description}</p>
      </div>
    </div>
    <div className="flex gap-3">
      <button
        onClick={onNavigate}
        className="px-6 h-12 bg-white text-cyan-800 font-bold rounded-lg hover:bg-gray-100 transition-colors shadow-lg"
      >
        Navigate
      </button>
      <button
        onClick={onRemind}
        className="px-6 h-12 bg-cyan-500/30 text-white font-medium rounded-lg hover:bg-cyan-500/40 transition-colors"
      >
        Remind in 30min
      </button>
    </div>
  </Card>
);

export default SuggestionCard;
