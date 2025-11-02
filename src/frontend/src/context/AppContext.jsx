import React, { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [activeScreen, setActiveScreen] = useState('dashboard');
  const [systemActive, setSystemActive] = useState(true);
  const [currentTime, setCurrentTime] = useState('12:45 PM');
  const [temperature] = useState('23°C');

  const value = {
    activeScreen,
    setActiveScreen,
    systemActive,
    setSystemActive,
    currentTime,
    setCurrentTime,
    temperature
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};