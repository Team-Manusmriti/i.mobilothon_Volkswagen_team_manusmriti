import React from 'react';
import { Brain } from 'lucide-react';
import { useAIAssistant } from '../../hooks/useAIAssistant';
import SuggestionCard from './SuggestionCard';
import ActionGrid from './ActionGrid';
import ConversationHistory from './ConversationHistory';

const AICoPilot = () => {
  const aiData = useAIAssistant();

  const handleNavigate = () => {
    console.log('Navigating to rest stop...');
  };

  const handleRemind = () => {
    console.log('Setting reminder for 30 minutes...');
  };

  return (
    <div className="px-4 sm:px-6 lg:px-12 py-4 sm:py-6 lg:py-8">
      <div className="flex items-center gap-3 sm:gap-4 mb-6 sm:mb-8">
        <div className="w-8 h-8 sm:w-10 sm:h-10 bg-cyan-500 rounded-lg flex items-center justify-center">
          <Brain className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
        </div>
        <div>
          <h1 className="text-white text-2xl sm:text-3xl font-bold">AI Co-Pilot</h1>
          <p className="text-gray-400 text-xs">Conversational Assistant</p>
        </div>
      </div>

      <SuggestionCard
        title={aiData.currentSuggestion.title}
        description={aiData.currentSuggestion.description}
        onNavigate={handleNavigate}
        onRemind={handleRemind}
      />

      <div className="mt-4 sm:mt-6">
        <ActionGrid 
          actions={aiData.contextActions} 
          onActionClick={aiData.executeAction} 
        />
      </div>

      <div className="mt-4 sm:mt-6">
        <ConversationHistory interactions={aiData.interactions} />
      </div>
    </div>
  );
};

export default AICoPilot;