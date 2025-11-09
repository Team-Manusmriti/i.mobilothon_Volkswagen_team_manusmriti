package com.vigilanceai.data

// Data models used across the app

data class AIConversationState(
    val isActive: Boolean = false,
    val isListening: Boolean = false,
    val isProcessing: Boolean = false,
    val isSpeaking: Boolean = false,
    val triggerReason: String = "",
    val currentMessage: String = ""
)

data class EmergencyActivation(
    val isTriggered: Boolean = false,
    val triggerType: String = "",
    val location: String = "Unknown",
    val timestamp: String = "",
    val emergencyContacted: Boolean = false,
    val responseTime: String = ""
)

data class WellnessMetrics(
    val perclos: Int = 12,
    val heartRate: Int = 72,
    val emotionState: String = "Calm & Focused",
    val emotionConfidence: Int = 85,
    val laneKeeping: String = "Stable",
    val steeringInput: String = "Smooth",
    val speedControl: String = "Steady"
)