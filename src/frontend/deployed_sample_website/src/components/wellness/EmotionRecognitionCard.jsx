import React from 'react';
import Card from '../common/Card';

const EmotionRecognitionCard = ({ emotion, confidence }) => (
  <Card className="p-8">
    <div className="text-gray-400 text-xs tracking-widest uppercase mb-5">
      FACIAL EMOTION RECOGNITION
    </div>
    <div className="flex items-center justify-between">
      <div className="flex-1">
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
      <div className="text-emerald-500 text-3xl font-bold ml-8">
        {confidence}%
      </div>
    </div>
  </Card>
);

export default EmotionRecognitionCard;