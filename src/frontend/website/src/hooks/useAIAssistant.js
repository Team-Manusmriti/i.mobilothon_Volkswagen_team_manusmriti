import { useState, useRef, useEffect } from 'react';
import { useApp } from '../context/AppContext.jsx';

export const useAIAssistant = () => {
  const app = useApp();

  const timeoutsRef = useRef([]);

  useEffect(() => {
    return () => {
      // cleanup any pending timeouts when hook consumer unmounts
      timeoutsRef.current.forEach(t => clearTimeout(t));
      timeoutsRef.current = [];
    };
  }, []);

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
    const action = state.contextActions.find(a => a.id === actionId) || {};
    console.log('Executing action:', action.title);

    // Prepare time and temperature (fallback to app context or compute)
    const now = new Date();
    const timeStr = app?.currentTime || now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    const temp = app?.temperature || 'N/A';

    // Initial interaction entry includes time and temperature
    const newInteraction = {
      time: timeStr,
      msg: `${action.title || 'Action'} - Initiated • Temp: ${temp}`
    };

    setState(prev => ({
      ...prev,
      interactions: [newInteraction, ...prev.interactions].slice(0, 8)
    }));

    // Simulate step updates for the action to appear in recent interactions
    const stepsByAction = {
      'Play Calming Music': ['Starting playlist', 'Adjusting volume', 'Music playing'],
      'Alternate Route': ['Calculating new route', 'Rerouting', 'Navigation started']
    };

    const steps = stepsByAction[action.title] || ['Initiating', 'Executing', 'Completed'];

    // Schedule step updates at 1.5s intervals and prepend them
    steps.forEach((stepText, idx) => {
      const t = setTimeout(() => {
        const stepTime = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        const stepInteraction = { time: stepTime, msg: `${action.title} - ${stepText}` };
        setState(prev => ({ ...prev, interactions: [stepInteraction, ...prev.interactions].slice(0, 8) }));
      }, 1500 * (idx + 1));
      timeoutsRef.current.push(t);
    });
  };

  const dismissSuggestion = () => {
    setState(prev => ({ ...prev, currentSuggestion: null }));
  };

  return { ...state, executeAction, dismissSuggestion };
};