import React from 'react';
import Card from '../common/Card';

const EmotionRecognitionCard = ({ emotion, confidence }) => (
  <Card className="p-4 sm:p-6 lg:p-8">
    <div className="text-gray-400 text-xs tracking-widest uppercase mb-4 sm:mb-5">
      FACIAL EMOTION RECOGNITION
    </div>
    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 sm:gap-0">
      <div className="flex-1 w-full sm:w-auto">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-3 h-3 rounded-full bg-emerald-500" />
          <span className="text-white text-sm font-medium">{emotion}</span>
        </div>
        <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
          <div 
            className="h-full bg-emerald-500 rounded-full transition-all duration-500" 
            style={{ width: `${confidence}%` }} 
          />
        </div>
      </div>
      <div className="text-emerald-500 text-2xl sm:text-3xl font-bold sm:ml-6 lg:ml-8">
        {confidence}%
      </div>
    </div>
  </Card>
);

export default EmotionRecognitionCard;