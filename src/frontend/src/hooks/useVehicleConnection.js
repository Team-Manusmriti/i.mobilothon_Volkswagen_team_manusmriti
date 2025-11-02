import { useState, useEffect } from 'react';

export const useVehicleConnection = () => {
  const [state, setState] = useState({
    connected: true,
    tripTime: '1h 23m',
    destination: '45 min away',
    vehicleData: { speed: 65, fuel: 75, engineTemp: 90 }
  });

  const [connectionError, setConnectionError] = useState(null);

  const reconnect = () => {
    console.log('Attempting to reconnect to vehicle...');
    setState(prev => ({ ...prev, connected: true }));
    setConnectionError(null);
  };

  useEffect(() => {
    // Simulate connection monitoring
    const interval = setInterval(() => {
      // Update trip time
      setState(prev => {
        const [hours, minutes] = prev.tripTime.split('h ');
        const totalMinutes = parseInt(hours) * 60 + parseInt(minutes);
        const newTotal = totalMinutes + 1;
        const newHours = Math.floor(newTotal / 60);
        const newMinutes = newTotal % 60;
        return {
          ...prev,
          tripTime: `${newHours}h ${newMinutes}m`
        };
      });
    }, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  return { ...state, connectionError, reconnect };
};