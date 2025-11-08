import React from 'react';
import { Coffee } from 'lucide-react';
import Card from '../common/Card';

const SuggestionCard = ({ title, description, onNavigate, onRemind }) => (
  <Card variant="gradient" className="p-4 sm:p-6 lg:p-8">
    <div className="flex items-start gap-3 sm:gap-4 mb-4 sm:mb-6">
      <Coffee className="w-5 h-5 sm:w-6 sm:h-6 text-white flex-shrink-0 mt-1" />
      <div>
        <h3 className="text-white text-base sm:text-lg font-bold mb-2">{title}</h3>
        <p className="text-white/90 text-sm leading-relaxed">{description}</p>
      </div>
    </div>
    <div className="flex flex-col sm:flex-row gap-3">
      <button
        onClick={onNavigate}
        className="px-4 sm:px-6 h-10 sm:h-12 bg-white text-cyan-800 font-bold rounded-lg hover:bg-gray-100 transition-colors shadow-lg text-sm sm:text-base"
      >
        Navigate
      </button>
      <button
        onClick={onRemind}
        className="px-4 sm:px-6 h-10 sm:h-12 bg-cyan-500/30 text-white font-medium rounded-lg hover:bg-cyan-500/40 transition-colors text-sm sm:text-base"
      >
        Remind in 30min
      </button>
    </div>
  </Card>
);

export default SuggestionCard;
