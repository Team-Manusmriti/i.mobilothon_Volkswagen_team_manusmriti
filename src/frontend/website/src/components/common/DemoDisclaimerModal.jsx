import React from 'react';

const DemoDisclaimerModal = ({ open = false, onClose = () => {} }) => {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      <div className="max-w-2xl w-full bg-gray-900 border border-gray-800 rounded-lg p-6 mx-4">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            <div className="h-12 w-12 rounded-md bg-cyan-600 flex items-center justify-center text-white font-bold">i</div>
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-semibold text-white">Demo - Limited Functionality</h2>
            <p className="text-sm text-gray-300 mt-2">This is a demo website which mimics the app interface and has limited functionalities. For full functionality use the project in a simulated environment with the backend sensors or WebSocket servers.</p>

            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="bg-gray-800 border border-gray-700 p-3 rounded">
                <h3 className="text-sm font-medium text-white">Available in Demo</h3>
                <ul className="text-xs text-gray-300 mt-2 list-disc list-inside space-y-1">
                  <li>Real-time wellness score (simulated)</li>
                  <li>Speed monitoring (simulated if backend missing)</li>
                  <li>Trip time and quick actions</li>
                  <li>AI suggestions and interaction history (demo)</li>
                </ul>
              </div>
              <div className="bg-gray-800 border border-gray-700 p-3 rounded">
                <h3 className="text-sm font-medium text-white">Notes</h3>
                <ul className="text-xs text-gray-300 mt-2 list-disc list-inside space-y-1">
                  <li>WebSocket ports: tries port 8008, falls back to simulated data</li>
                  <li>No external sensors required for demo</li>
                </ul>
              </div>
            </div>

            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => { onClose(); localStorage.setItem('demoDisclaimerSeen', 'true'); }}
                className="px-4 py-2 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-sm"
              >
                Got it — continue
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DemoDisclaimerModal;
