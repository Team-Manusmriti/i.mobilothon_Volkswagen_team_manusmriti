import React from 'react';

const Card = ({ children, variant = 'default', borderColor, className = '' }) => {
  const variants = {
    default: 'bg-gray-800 border border-gray-700',
    accent: `bg-gray-800 border-l-4 ${borderColor || 'border-cyan-500'}`,
    gradient: 'bg-gradient-to-r from-cyan-500 to-blue-500'
  };

  return (
    <div className={`${variants[variant]} rounded-xl ${className}`}>
      {children}
    </div>
  );
};

export default Card;