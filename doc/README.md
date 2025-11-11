# VigilanceAI Technical Documentation

Comprehensive technical documentation for VigilanceAI - an AI-Enhanced Driver Wellness Monitoring system that redefines road safety through proactive, intelligent driver care.

## System Overview

VigilanceAI is an intelligent co-pilot that shifts from reactive alerts to proactive, emotionally aware intelligence. It creates a closed-loop system that detects risk and actively supports drivers throughout their journey using multi-modal AI fusion.

## Documentation Structure

### Core System Documentation

| Component | Description | Document |
|----------|-------------|-------------|
| **Setup & Testing** | Complete installation and testing guide | [Installation Guide](installation.md) \| [Testing Guide](testing.md) |
| **Architecture** | Multi-layered system architecture with AI fusion engine | [Architecture.md](architecture.md) |
| **Process Flow** | Proactive monitoring and intervention workflow | [Process_flow.md](process_flow.md) |
| **Implementation** | Technical implementation details and deployment guide | [Implementation.md](implementation.md) |
| **API Reference** | Backend API endpoints and WebSocket specifications | [API_reference.md](api_reference.md) |


### User Interface Documentation

| Component | Description | Document |
|----------|-------------|-------------|
| **Main Dashboard** | Primary dashboard with wellness scoring and vehicle status | [Main_dashboard.md](Main_dashboard.md) |
| **Wellness Monitor** | Real-time driver monitoring with PERCLOS and emotion recognition | [S2_wellness_monitor.md](S2_wellness_monitor.md) |
| **Emergency Protocol** | Automated emergency response and eCall system | [S3_emergency_protocol.md](S3_emergency_protocol.md) |
| **AI Co-Pilot** | Conversational AI co-pilot with context-aware interventions | [S4_Copilot.md](S4_Copilot.md) |


## Platform Availability

VigilanceAI is available on two platforms:
- **Web Application**: React-based dashboard for in-vehicle displays
- **Mobile Application**: Flutter-based companion app for smartphones

## Key Technologies

### AI & Machine Learning
- **Computer Vision**: OpenCV, DeepFace for facial emotion recognition
- **Behavioral Analysis**: Real-time driving pattern analysis and anomaly detection
- **Multi-modal Fusion**: Combines cabin video analytics with vehicle telemetry

### Backend Infrastructure
- **FastAPI**: High-performance Python backend with WebSocket support
- **CARLA Simulator**: Vehicle behavior simulation and testing environment
- **Real-time Processing**: 10Hz update rate for continuous monitoring

### Frontend Platforms
- **React + Vite**: Modern web application with Tailwind CSS
- **Flutter**: Cross-platform mobile application
- **Responsive Design**: Optimized for automotive displays (1920x1080px)

## Quick Navigation

| Component | Description | Documentation |
|-----------|-------------|---------------|
| **System Architecture** | AI fusion engine and component relationships | [View](architecture.md) |
| **Process Flow** | Proactive monitoring and intervention logic | [View](process_flow.md) |
| **Implementation** | Deployment guide and technical specifications | [View](implementation.md) |
| **API Reference** | Backend endpoints and data models | [View](api_reference.md) |

## Core Features

### 1. AI Fusion Driver Model
- Combines cabin video analytics with real-time vehicle behavior
- Multi-dimensional insight into driver wellness and vehicle state
- Continuous learning and personalization

### 2. Proactive Wellness Detection
- **Fatigue Detection**: PERCLOS, yawning, head position analysis
- **Stress Recognition**: Facial emotion recognition and driving aggression
- **Medical Distress**: Early warning system for health emergencies

### 3. Context-Aware Interventions
- Dynamic conversational AI with helpful dialogue
- Personalized suggestions based on driver state and environment
- Non-intrusive alerts that avoid startling the driver

### 4. Emergency Response System
- Automatic critical event detection (medical, collision, rollover)
- Vehicle securement protocol with controlled braking
- Automated eCall with GPS location and event data

## Documentation Navigation

| Category | Description | Document |
|----------|----------|-------------|
| **Project** | Project overview and team information | [Main Project README](../README.md) |
| **Setup** | Complete installation and setup guide | [Installation Guide](installation.md) |
| **Testing** | Testing procedures and script documentation | [Testing Guide](testing.md) |
| **Technical** | Technical deployment and setup | [Implementation Guide](implementation.md) |
| **Technical** | Backend endpoints and data models | [API Reference](api_reference.md) |
| **Interface** | Primary interface specifications | [Main Dashboard](Main_dashboard.md) |
| **Interface** | Real-time monitoring system | [Wellness Monitor](S2_wellness_monitor.md) |
| **Interface** | Automated safety responses | [Emergency Protocol](S3_emergency_protocol.md) |
| **Interface** | Conversational assistant interface | [AI Co-Pilot](S4_Copilot.md) |
| **Source** | React web application | [Frontend Source](../src/frontend/website) |
| **Source** | Kotlin mobile application | [App Source](../src/frontend/app) |
| **Source** | Python backend with CARLA integration | [Backend Source](../src/carla/) |

---

*Part of VigilanceAI - Built with ❤️ for Volkswagen - i.mobilothon-5.0*
---