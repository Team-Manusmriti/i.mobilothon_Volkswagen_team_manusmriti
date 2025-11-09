// Safe VigilanceViewModel.kt
// Use this if you're still having issues with the previous version

package com.vigilanceai.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.vigilanceai.data.AIConversationState
import com.vigilanceai.data.EmergencyActivation
import com.vigilanceai.data.DriverMetrics
import com.vigilanceai.data.EmergencyStatus
import com.vigilanceai.data.CoPilotSuggestion
import com.vigilanceai.data.InteractionHistory
import com.vigilanceai.service.AIMessage
import com.vigilanceai.service.AIState
import com.vigilanceai.service.VigilanceAIService
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

class VigilanceViewModel : ViewModel() {
    
    // Reference to AI Service (will be set from MainActivity)
    private var aiService: VigilanceAIService? = null
    
    // Existing metrics flow (Driver-facing aggregated metrics expected by UI)
    private val _metrics = MutableStateFlow(DriverMetrics())
    val metrics: StateFlow<DriverMetrics> = _metrics.asStateFlow()
    
    // Existing emergency activation flow
    private val _emergencyActivation = MutableStateFlow(EmergencyActivation())
    val emergencyActivation: StateFlow<EmergencyActivation> = _emergencyActivation.asStateFlow()

    // Emergency system status (detection subsystems)
    private val _emergencyStatus = MutableStateFlow(EmergencyStatus())
    val emergencyStatus: StateFlow<EmergencyStatus> = _emergencyStatus.asStateFlow()
    
    // AI Conversation State
    private val _aiConversationState = MutableStateFlow(AIConversationState())
    val aiConversationState: StateFlow<AIConversationState> = _aiConversationState.asStateFlow()
    
    // Local copy of conversation messages to avoid StateFlow issues
    private val _conversationMessages = MutableStateFlow<List<AIMessage>>(emptyList())
    val conversationMessages: StateFlow<List<AIMessage>> = _conversationMessages.asStateFlow()
    
    // AI activation state
    private val _isAIActivated = MutableStateFlow(false)
    val isAIActivated: StateFlow<Boolean> = _isAIActivated.asStateFlow()
    
    // AI state
    private val _aiState = MutableStateFlow(AIState.IDLE)
    val aiState: StateFlow<AIState> = _aiState.asStateFlow()
    
    init {
        // Start simulated metric updates
        startMetricSimulation()
        
        // Start monitoring for fatigue detection
        startFatigueMonitoring()
    }
    
    // Bind AI Service
    fun bindAIService(service: VigilanceAIService) {
        aiService = service
        
        // Observe AI state changes
        viewModelScope.launch {
            service.aiState.collect { state ->
                _aiState.value = state
                updateAIConversationState(state)
            }
        }
        
        // Observe activation changes
        viewModelScope.launch {
            service.isActivated.collect { isActivated ->
                _isAIActivated.value = isActivated
                _aiConversationState.update { it.copy(isActive = isActivated) }
            }
        }
        
        // Observe conversation messages
        viewModelScope.launch {
            service.conversationMessages.collect { messages ->
                _conversationMessages.value = messages
            }
        }
        
        // Start continuous listening for wake word
        service.startContinuousListening()
    }

    // Co-pilot suggestions and interaction history for the CoPilot UI
    private val _currentSuggestion = MutableStateFlow(
        CoPilotSuggestion(
            title = "Take a Break",
            description = "Short rest can improve alertness",
            icon = "coffee",
            primaryAction = "Navigate",
            secondaryAction = "Remind me"
        )
    )
    val currentSuggestion: StateFlow<CoPilotSuggestion> = _currentSuggestion.asStateFlow()

    private val _interactionHistory = MutableStateFlow<List<InteractionHistory>>(emptyList())
    val interactionHistory: StateFlow<List<InteractionHistory>> = _interactionHistory.asStateFlow()

    // Helper used by UI tests to simulate an accident
    fun simulateAccident() {
        triggerEmergency("COLLISION", "Simulated location")
    }

    // Backwards-compatible name used in several UI screens
    fun startAIConversation(reason: String) {
        triggerAIConversation(reason)
    }
    
    private fun updateAIConversationState(state: AIState) {
        _aiConversationState.update { 
            it.copy(
                isListening = state == AIState.LISTENING,
                isProcessing = state == AIState.PROCESSING,
                isSpeaking = state == AIState.SPEAKING
            )
        }
    }
    
    // Voice interaction controls
    fun startListening() {
        aiService?.startContinuousListening()
    }
    
    fun stopListening() {
        aiService?.stopListening()
    }
    
    fun dismissAIConversation() {
        aiService?.deactivateAI()
        _aiConversationState.update { it.copy(isActive = false) }
    }
    
    // Trigger AI conversation with specific reason
    fun triggerAIConversation(reason: String, message: String = "") {
        _aiConversationState.update {
            it.copy(
                isActive = true,
                triggerReason = reason,
                currentMessage = message.ifEmpty {
                    when (reason) {
                        "FATIGUE" -> "I've noticed you might need a break. Let's talk about how you're feeling."
                        "DROWSINESS" -> "I've detected signs of drowsiness. Your safety is important. How are you feeling?"
                        "STRESS" -> "I sense you might be stressed. Would you like to talk about it?"
                        else -> "I'm here to help. How can I assist you?"
                    }
                }
            )
        }
        
        // Also trigger the AI service emergency response
        aiService?.triggerEmergencyResponse(reason, message)
    }
    
    // Emergency handling
    fun triggerEmergency(type: String, location: String = "Unknown") {
        val timestamp = SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(Date())
        
        _emergencyActivation.value = EmergencyActivation(
            isTriggered = true,
            triggerType = type,
            location = location,
            timestamp = timestamp,
            emergencyContacted = false,
            responseTime = "Estimating..."
        )
        
        // Trigger AI emergency response
        aiService?.triggerEmergencyResponse(type, "Emergency detected at $location")
        
        // Simulate emergency services contact
        viewModelScope.launch {
            kotlinx.coroutines.delay(2000)
            _emergencyActivation.update {
                it.copy(
                    emergencyContacted = true,
                    responseTime = "5-7 minutes"
                )
            }
        }
    }
    
    fun cancelEmergency() {
        _emergencyActivation.value = EmergencyActivation()
        aiService?.speak("Emergency cancelled. Glad you're okay. Let me know if you need anything.")
    }
    
    // Fatigue monitoring with AI integration
    private fun startFatigueMonitoring() {
        viewModelScope.launch {
            metrics.collect { currentMetrics ->
                // Check PERCLOS (eye closure) - only trigger if not already active
                if (!_aiConversationState.value.isActive) {
                    when {
                        currentMetrics.perclos > 70 -> {
                            triggerAIConversation(
                                "DROWSINESS",
                                "Critical drowsiness detected. PERCLOS at ${currentMetrics.perclos}%"
                            )
                        }
                        currentMetrics.perclos > 50 -> {
                            triggerAIConversation(
                                "FATIGUE",
                                "Elevated drowsiness detected. PERCLOS at ${currentMetrics.perclos}%"
                            )
                        }
                    }
                }
                
                // Check emotion state for stress
                if (!_aiConversationState.value.isActive) {
                    if (currentMetrics.emotionState.contains("Stressed", ignoreCase = true) ||
                        currentMetrics.emotionState.contains("Anxious", ignoreCase = true)) {
                        triggerAIConversation(
                            "STRESS",
                            "High stress levels detected in facial analysis"
                        )
                    }
                }
                
                // Check heart rate
                if (!_aiConversationState.value.isActive) {
                    if (currentMetrics.heartRate > 100) {
                        triggerAIConversation(
                            "STRESS",
                            "Elevated heart rate detected: ${currentMetrics.heartRate} BPM"
                        )
                    }
                }
            }
        }
    }
    
    // Simulate real-time metrics (replace with actual sensor data)
    private fun startMetricSimulation() {
        viewModelScope.launch {
            var perclosValue = 12.0
            var heartRate = 72
            var emotionIndex = 0
            val emotions = listOf(
                "Calm & Focused" to 85,
                "Alert" to 92,
                "Slightly Tired" to 75,
                "Calm" to 88
            )

            while (true) {
                kotlinx.coroutines.delay(5000) // Update every 5 seconds

                // Simulate varying metrics
                perclosValue = (perclosValue + (-3..3).random()).coerceIn(4.0, 90.0)
                heartRate = (heartRate + (-2..2).random()).coerceIn(60, 120)

                val (emotion, confidence) = emotions[emotionIndex % emotions.size]
                emotionIndex++

                // Update driver-focused metrics used by the UI
                _metrics.value = DriverMetrics(
                    wellnessScore = (80 + (-5..5).random()),
                    alertness = (80 + (-10..10).random()),
                    stress = if (confidence < 80) "Elevated" else "Low",
                    fatigue = perclosValue.toInt().coerceIn(0, 100),
                    isDrowsy = perclosValue > 70,
                    accidentDetected = false,
                    perclos = perclosValue,
                    heartRate = heartRate,
                    emotionState = emotion,
                    emotionConfidence = confidence,
                    laneKeeping = if (perclosValue < 30) "Stable" else "Drifting",
                    steeringInput = if (perclosValue < 40) "Smooth" else "Erratic",
                    speedControl = "Steady",
                    tripTime = "1h ${1 + (0..59).random()}m",
                    destination = "Destination"
                )
            }
        }
    }
    
    // Manual AI activation (for testing or user-initiated)
    fun activateAI() {
        aiService?.let { service ->
            if (_isAIActivated.value) {
                // Already activated, just open conversation
                _aiConversationState.update { it.copy(isActive = true) }
            } else {
                // Activate and open conversation
                service.startContinuousListening()
                _aiConversationState.update {
                    it.copy(
                        isActive = true,
                        currentMessage = "How can I assist you today?"
                    )
                }
            }
        }
    }
    
    // Speak through AI
    fun speakToDriver(message: String) {
        aiService?.speak(message)
    }
    
    override fun onCleared() {
        super.onCleared()
        // Clean up if needed
        aiService?.stopListening()
    }
}