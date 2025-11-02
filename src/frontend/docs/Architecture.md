# VigilanceAI Project Structure 

vigilance-ai/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── TopBar.jsx
│   │   │   ├── NavigationBar.jsx
│   │   │   ├── BottomBar.jsx
│   │   │   ├── Card.jsx
│   │   │   └── MetricCard.jsx
│   │   ├── dashboard/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── WellnessScoreCard.jsx
│   │   │   └── QuickActionsPanel.jsx
│   │   ├── wellness/
│   │   │   ├── WellnessMonitor.jsx
│   │   │   ├── PrimaryMetricCard.jsx
│   │   │   ├── EmotionRecognitionCard.jsx
│   │   │   └── DrivingPatternCard.jsx
│   │   ├── emergency/
│   │   │   ├── EmergencyProtocol.jsx
│   │   │   ├── DetectionSystemCard.jsx
│   │   │   ├── ResponseSequenceCard.jsx
│   │   │   └── EmergencyContactsCard.jsx
│   │   └── copilot/
│   │       ├── AICoPilot.jsx
│   │       ├── SuggestionCard.jsx
│   │       ├── ActionGrid.jsx
│   │       └── ConversationHistory.jsx
│   ├── hooks/
│   │   ├── useWellnessData.js
│   │   ├── useVehicleConnection.js
│   │   ├── useAIAssistant.js
│   │   └── useEmergencySystem.js
│   ├── context/
│   │   └── AppContext.jsx
│   ├── styles/
│   │   └── index.css
│   ├── App.jsx
│   └── main.jsx
├── .gitignore
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── index.html
└── README.md