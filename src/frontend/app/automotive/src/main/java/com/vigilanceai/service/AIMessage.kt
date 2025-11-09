package com.vigilanceai.service

// Unified message model used by the service and UI
data class AIMessage(
    val text: String,
    val isAI: Boolean,
    val timestamp: Long,
    val isEmergency: Boolean = false
)