import React from 'react';
import Card from '../common/Card';

const ResponseSequenceCard = ({ steps }) => (
  <Card className="p-8">
    <h3 className="text-white text-sm font-medium mb-6">
      Automatic Response Sequence
    </h3>
    <div className="space-y-5">
      {steps.map((step) => (
        <div key={step.num} className="flex items-start gap-4">
          <div className="w-8 h-8 rounded-full bg-cyan-500 flex items-center justify-center flex-shrink-0">
            <span className="text-white text-sm font-bold">{step.num}</span>
          </div>
          <div>
            <div className="text-white text-sm font-medium mb-1">
              {step.title}
            </div>
            <div className="text-gray-400 text-xs">{step.desc}</div>
          </div>
        </div>
      ))}
    </div>
  </Card>
);

export default ResponseSequenceCard;