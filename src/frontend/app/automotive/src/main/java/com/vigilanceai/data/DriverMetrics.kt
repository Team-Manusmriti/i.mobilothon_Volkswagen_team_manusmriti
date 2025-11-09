package com.vigilanceai.data

data class DriverMetrics(
    val wellnessScore: Int = 94,
    val alertness: Int = 98,
    val stress: String = "Low",
    val fatigue: Int = 12,
    val isDrowsy: Boolean = false,
    val accidentDetected: Boolean = false,
    val perclos: Double = 4.2,
    val heartRate: Int = 72,
    val emotionState: String = "Calm & Focused",
    val emotionConfidence: Int = 85,
    val laneKeeping: String = "Stable",
    val steeringInput: String = "Smooth",
    val speedControl: String = "Steady",
    val tripTime: String = "1h 23m",
    val destination: String = "45 min away"
)

data class EmergencyStatus(
    val isActive: Boolean = true,
    val medicalDetection: String = "Monitoring",
    val collisionDetection: String = "Active",
    val lossOfControl: String = "Tracking"
)

data class CoPilotSuggestion(
    val title: String,
    val description: String,
    val icon: String,
    val primaryAction: String,
    val secondaryAction: String
)

data class InteractionHistory(
    val time: String,
    val message: String
)
