import { useEffect, useRef, useState } from 'react';

// useWebSocketWithFallback
// - Tries to open a WebSocket to `url`.
// - Waits `timeoutMs` (default 3000) for onopen. If not opened -> starts simulation.
// - Accepts an onMessage callback which receives parsed data objects.
// - Accepts a fallbackGenerator function that returns an object representing a message.
// - Returns { mode: 'live'|'simulated', connected, send }.

export function useWebSocketWithFallback(url, { onMessage, fallbackGenerator, intervalMs = 1000, timeoutMs = 3000 } = {}) {
  const wsRef = useRef(null);
  const simIntervalRef = useRef(null);
  const timeoutRef = useRef(null);
  const [mode, setMode] = useState('connecting'); // 'connecting' | 'live' | 'simulated'
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    let closed = false;

    try {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        if (closed) return;
        clearTimeout(timeoutRef.current);
        setMode('live');
        setConnected(true);
        console.log(`✅ WebSocket connected to ${url}`);
      };

      ws.onmessage = (ev) => {
        try {
          const data = JSON.parse(ev.data);
          if (onMessage) onMessage(data);
        } catch (e) {
          // pass raw
          if (onMessage) onMessage(ev.data);
        }
      };

      ws.onerror = (err) => {
        console.log('❌ WebSocket error', err);
      };

      ws.onclose = () => {
        console.log('⚠️ WebSocket closed', url);
        setConnected(false);
        if (!closed && mode !== 'simulated') {
          // fallback to simulation
          startSimulation();
        }
      };

      // wait for open, otherwise fallback
      timeoutRef.current = setTimeout(() => {
        if (ws && ws.readyState !== WebSocket.OPEN) {
          console.log(`⏱️ WebSocket ${url} did not open in ${timeoutMs}ms — starting simulation`);
          // close real ws if any
          try { ws.close(); } catch (e) {}
          startSimulation();
        }
      }, timeoutMs);
    } catch (e) {
      console.log('WebSocket construction failed, falling back to simulation', e);
      startSimulation();
    }

    function startSimulation() {
      if (closed) return;
      setMode('simulated');
      setConnected(false);
      if (simIntervalRef.current) return;
      // Immediately send one
      if (fallbackGenerator && onMessage) {
        try { onMessage(fallbackGenerator()); } catch (e) { console.error(e); }
      }
      simIntervalRef.current = setInterval(() => {
        if (fallbackGenerator && onMessage) {
          try { onMessage(fallbackGenerator()); } catch (e) { console.error(e); }
        }
      }, intervalMs);
    }

    return () => {
      closed = true;
      clearTimeout(timeoutRef.current);
      if (wsRef.current) {
        try { wsRef.current.close(); } catch (e) {}
      }
      if (simIntervalRef.current) clearInterval(simIntervalRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url]);

  const send = (obj) => {
    if (mode === 'live' && wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      try { wsRef.current.send(JSON.stringify(obj)); } catch (e) { console.error(e); }
    } else {
      console.log('Simulated mode — send ignored', obj);
    }
  };

  return { mode, connected, send };
}

// Small helper fallback generators for common use cases
export function speedFallbackGenerator(prev = 50) {
  // produce a realistic speed around 50-100 km/h
  const base = typeof prev === 'number' ? prev : 60;
  const next = Math.max(0, Math.min(140, Math.round(base + (Math.random() - 0.5) * 6)));
  return { speed: next };
}

export function emotionFallbackGenerator() {
  const emotions = ['Calm', 'Focused', 'Distracted', 'Drowsy', 'Stressed'];
  const e = emotions[Math.floor(Math.random() * emotions.length)];
  const state = e === 'Drowsy' ? 'low' : 'normal';
  return { emotion: e, state };
}
