import { useState } from 'react';

export const useAIAssistant = () => {
  const [state, setState] = useState({
    currentSuggestion: {
      title: 'Time for a break?',
      description: "You've been driving for 2 hours. There's a rest stop 5km ahead with good reviews.",
      icon: 'coffee'
    },
    interactions: [
      { time: '10:30', msg: 'Suggested caffeine break - Accepted' },
      { time: '09:15', msg: 'Played focus playlist - Stress reduced by 15%' },
      { time: '08:45', msg: 'Morning greeting - Trip started' }
    ],
    contextActions: [
      { id: 1, title: 'Play Calming Music', desc: 'Reduce stress levels', icon: 'music' },
      { id: 2, title: 'Alternate Route', desc: 'Avoid heavy traffic', icon: 'navigation' }
    ]
  });

  const executeAction = (actionId) => {
    const action = state.contextActions.find(a => a.id === actionId);
    console.log('Executing action:', action?.title);
    
    // Add to interactions
    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    const newInteraction = { 
      time, 
      msg: `${action?.title} - Initiated` 
    };
    
    setState(prev => ({
      ...prev,
      interactions: [newInteraction, ...prev.interactions].slice(0, 5)
    }));
  };

  const dismissSuggestion = () => {
    setState(prev => ({ ...prev, currentSuggestion: null }));
  };

  return { ...state, executeAction, dismissSuggestion };
};