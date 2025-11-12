declare module './AppContext.jsx' {
  import * as React from 'react';
  
  interface AppContextType {
    activeScreen: string;
    setActiveScreen: (screen: string) => void;
    systemActive: boolean;
    setSystemActive: (active: boolean) => void;
    currentTime: string;
    setCurrentTime: (time: string) => void;
    temperature: string;
  }
  
  export const AppProvider: React.FC<{ children: React.ReactNode }>;
  export const useApp: () => AppContextType;
}