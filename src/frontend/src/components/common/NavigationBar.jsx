import React from 'react';

const NavigationBar = ({ activeScreen, onScreenChange, screens }) => (
  <div className="flex gap-8 px-12 border-b border-gray-800">
    {screens.map((screen) => {
      const screenKey = screen.toLowerCase().replace(' ', '-');
      const isActive = activeScreen === screenKey;
      return (
        <button
          key={screenKey}
          onClick={() => onScreenChange(screenKey)}
          className={`pb-4 text-sm font-medium transition-colors relative ${
            isActive ? 'text-cyan-500' : 'text-gray-400 hover:text-gray-200'
          }`}
        >
          {screen}
          {isActive && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-cyan-500" />
          )}
        </button>
      );
    })}
  </div>
);

export default NavigationBar;