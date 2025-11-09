// VigilanceAIService.kt
// Place in: com/vigilanceai/service/

package com.vigilanceai.service

import android.app.Service
import android.content.Intent
import android.os.Binder
import android.os.IBinder
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.util.Log
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.util.*

class VigilanceAIService : Service(), TextToSpeech.OnInitListener {
    
    companion object {
        private const val TAG = "VigilanceAIService"
        private const val WAKE_WORD = "vigilanceai"
        private const val ALTERNATE_WAKE_WORD = "vigilance"
    }
    
    private val binder = LocalBinder()
    private lateinit var speechRecognizer: SpeechRecognizer
    private lateinit var textToSpeech: TextToSpeech
    private val serviceScope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    
    // State flows for integration with ViewModel
    private val _aiState = MutableStateFlow<AIState>(AIState.IDLE)
    val aiState: StateFlow<AIState> = _aiState
    
    private val _conversationMessages = MutableStateFlow<List<AIMessage>>(emptyList())
    val conversationMessages: StateFlow<List<AIMessage>> = _conversationMessages
    
    private val _isActivated = MutableStateFlow(false)
    val isActivated: StateFlow<Boolean> = _isActivated
    
    private val _currentTranscript = MutableStateFlow("")
    val currentTranscript: StateFlow<String> = _currentTranscript
    
    private var isListening = false
    private var isTTSReady = false
    
    inner class LocalBinder : Binder() {
        fun getService(): VigilanceAIService = this@VigilanceAIService
    }
    
    override fun onBind(intent: Intent): IBinder {
        Log.d(TAG, "Service bound")
        return binder
    }
    
    override fun onCreate() {
        super.onCreate()
        Log.d(TAG, "Service created")
        initializeSpeechRecognizer()
        initializeTextToSpeech()
    }
    
    private fun initializeSpeechRecognizer() {
        if (!SpeechRecognizer.isRecognitionAvailable(this)) {
            Log.e(TAG, "Speech recognition not available on this device")
            return
        }
        
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
        speechRecognizer.setRecognitionListener(object : RecognitionListener {
            override fun onReadyForSpeech(params: Bundle?) {
                Log.d(TAG, "Ready for speech")
                _aiState.value = AIState.LISTENING
            }
            
            override fun onBeginningOfSpeech() {
                Log.d(TAG, "Speech started")
            }
            
            override fun onRmsChanged(rmsdB: Float) {
                // Can be used for visualizing sound level
            }
            
            override fun onBufferReceived(buffer: ByteArray?) {}
            
            override fun onEndOfSpeech() {
                Log.d(TAG, "Speech ended")
                _aiState.value = AIState.PROCESSING
            }
            
            override fun onError(error: Int) {
                val errorMessage = when (error) {
                    SpeechRecognizer.ERROR_AUDIO -> "Audio recording error"
                    SpeechRecognizer.ERROR_CLIENT -> "Client error"
                    SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -> "Insufficient permissions"
                    SpeechRecognizer.ERROR_NETWORK -> "Network error"
                    SpeechRecognizer.ERROR_NETWORK_TIMEOUT -> "Network timeout"
                    SpeechRecognizer.ERROR_NO_MATCH -> "No speech match"
                    SpeechRecognizer.ERROR_RECOGNIZER_BUSY -> "Recognition service busy"
                    SpeechRecognizer.ERROR_SERVER -> "Server error"
                    SpeechRecognizer.ERROR_SPEECH_TIMEOUT -> "No speech input"
                    else -> "Unknown error: $error"
                }
                Log.e(TAG, "Speech recognition error: $errorMessage")
                
                _aiState.value = AIState.ERROR
                
                // Restart listening if activated (except for permission errors)
                if (_isActivated.value && error != SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS) {
                    serviceScope.launch {
                        delay(1000)
                        startContinuousListening()
                    }
                }
            }
            
            override fun onResults(results: Bundle?) {
                results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.let { matches ->
                    val spokenText = matches[0].lowercase(Locale.getDefault())
                    Log.d(TAG, "Recognized: $spokenText")
                    _currentTranscript.value = spokenText
                    
                    // Check for wake word
                    if (!_isActivated.value && (spokenText.contains(WAKE_WORD) || spokenText.contains(ALTERNATE_WAKE_WORD))) {
                        Log.d(TAG, "Wake word detected!")
                        activateAI()
                        return
                    }
                    
                    // Process command if activated
                    if (_isActivated.value) {
                        processVoiceCommand(spokenText)
                    }
                }
                
                // Continue listening
                if (_isActivated.value || !_isActivated.value) {
                    serviceScope.launch {
                        delay(300)
                        startContinuousListening()
                    }
                }
            }
            
            override fun onPartialResults(partialResults: Bundle?) {
                partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.let { matches ->
                    val partialText = matches.firstOrNull() ?: ""
                    _currentTranscript.value = partialText
                    Log.d(TAG, "Partial: $partialText")
                }
            }
            
            override fun onEvent(eventType: Int, params: Bundle?) {}
        })
    }
    
    private fun initializeTextToSpeech() {
        textToSpeech = TextToSpeech(this, this)
        textToSpeech.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) {
                _aiState.value = AIState.SPEAKING
                Log.d(TAG, "TTS started")
            }
            
            override fun onDone(utteranceId: String?) {
                _aiState.value = AIState.IDLE
                Log.d(TAG, "TTS completed")
                
                if (_isActivated.value) {
                    serviceScope.launch {
                        delay(500)
                        startContinuousListening()
                    }
                }
            }
            
            override fun onError(utteranceId: String?) {
                _aiState.value = AIState.ERROR
                Log.e(TAG, "TTS error")
            }
        })
    }
    
    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            val result = textToSpeech.setLanguage(Locale.US)
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                Log.e(TAG, "TTS language not supported")
            } else {
                // Male voice settings - deeper pitch, slightly slower
                textToSpeech.setPitch(0.85f)  // Lower pitch for male voice
                textToSpeech.setSpeechRate(0.95f)  // Slightly slower for clarity
                isTTSReady = true
                Log.d(TAG, "TTS initialized successfully with male voice")
            }
        } else {
            Log.e(TAG, "TTS initialization failed")
        }
    }
    
    fun startContinuousListening() {
        if (!::speechRecognizer.isInitialized) {
            Log.e(TAG, "Speech recognizer not initialized")
            return
        }
        
        if (!isListening) {
            val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
                putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
                putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
            }
            
            try {
                speechRecognizer.startListening(intent)
                isListening = true
                Log.d(TAG, "Started listening")
            } catch (e: Exception) {
                Log.e(TAG, "Failed to start listening", e)
                _aiState.value = AIState.ERROR
            }
        }
    }
    
    fun stopListening() {
        if (isListening) {
            speechRecognizer.stopListening()
            isListening = false
            _isActivated.value = false
            _aiState.value = AIState.IDLE
            Log.d(TAG, "Stopped listening")
        }
    }
    
    private fun activateAI() {
        _isActivated.value = true
        speak("Yes, I'm listening. How can I help you?")
        addMessage(AIMessage(
            text = "VigilanceAI activated",
            isAI = true,
            timestamp = System.currentTimeMillis()
        ))
        Log.d(TAG, "AI activated")
    }
    
    fun deactivateAI() {
        _isActivated.value = false
        speak("I'll be here if you need me. Drive safe.")
        Log.d(TAG, "AI deactivated")
    }
    
    private fun processVoiceCommand(command: String) {
        Log.d(TAG, "Processing command: $command")
        
        addMessage(AIMessage(
            text = command,
            isAI = false,
            timestamp = System.currentTimeMillis()
        ))
        
        serviceScope.launch {
            val response = getAIResponse(command)
            addMessage(AIMessage(
                text = response,
                isAI = true,
                timestamp = System.currentTimeMillis()
            ))
            speak(response)
        }
    }
    
    private suspend fun getAIResponse(input: String): String = withContext(Dispatchers.IO) {
        // Context-aware responses based on driver state
        return@withContext when {
            // Fatigue/tiredness related
            input.contains("tired") || input.contains("sleepy") || input.contains("drowsy") -> {
                "I notice you're feeling tired. Let me find the nearest rest stop for you. It's important to take a break for your safety."
            }
            
            // Stress related
            input.contains("stressed") || input.contains("stress") || input.contains("anxious") -> {
                "I understand you're feeling stressed. Let me help you with some calming music, or I can suggest an alternate route if traffic is the issue."
            }
            
            // Traffic related
            input.contains("traffic") || input.contains("jam") || input.contains("slow") -> {
                "I see traffic is bothering you. Would you like me to find an alternative route? I can also play some relaxing music to help."
            }
            
            // Break/rest related
            input.contains("break") || input.contains("rest") || input.contains("stop") -> {
                "Good idea to take a break. There's a rest area 3 kilometers ahead. Shall I guide you there?"
            }
            
            // Music related
            input.contains("music") || input.contains("song") || input.contains("play") -> {
                "I'll play something for you. What mood are you in? Energizing or calming?"
            }
            
            // Route/navigation
            input.contains("route") || input.contains("direction") || input.contains("way") -> {
                "Let me check the route for you. Where would you like to go?"
            }
            
            // Emergency/help
            input.contains("help") || input.contains("emergency") || input.contains("urgent") -> {
                "I'm here to help. Is everything okay? Do you need me to contact emergency services?"
            }
            
            // Wellness check
            input.contains("fine") || input.contains("good") || input.contains("okay") -> {
                "That's great to hear! I'll keep monitoring and let you know if I notice anything. Just say my name if you need me."
            }
            
            // Dismissal
            input.contains("stop") || input.contains("quiet") || input.contains("silence") -> {
                "Understood. I'll go quiet now, but I'm still monitoring. Say 'VigilanceAI' anytime you need me."
            }
            
            else -> {
                "I'm here for you. Could you tell me more about what you need?"
            }
        }
    }
    
    fun speak(text: String) {
        if (!isTTSReady) {
            Log.e(TAG, "TTS not ready")
            return
        }
        
        val utteranceId = UUID.randomUUID().toString()
        val params = Bundle().apply {
            putString(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, utteranceId)
        }
        
        textToSpeech.speak(text, TextToSpeech.QUEUE_ADD, params, utteranceId)
        Log.d(TAG, "Speaking: $text")
    }
    
    private fun addMessage(message: AIMessage) {
        val currentMessages = _conversationMessages.value
        _conversationMessages.value = currentMessages + message
    }
    
    fun clearConversation() {
        _conversationMessages.value = emptyList()
    }
    
    // Emergency integration
    fun triggerEmergencyResponse(emergencyType: String, details: String) {
        _isActivated.value = true
        
        val emergencyMessage = when (emergencyType.uppercase()) {
            "DROWSINESS", "FATIGUE" -> {
                "Critical drowsiness detected. I strongly recommend you pull over immediately. Your safety is my priority."
            }
            "STRESS" -> {
                "I've detected high stress levels. Let's find you a safe place to take a break and calm down."
            }
            "MEDICAL" -> {
                "Medical distress detected. I'm activating emergency protocols. Please try to pull over safely."
            }
            "COLLISION" -> {
                "Collision detected. Stay calm. Emergency services are being contacted. Are you able to respond?"
            }
            else -> {
                "I've detected an unusual pattern. Are you okay? Please let me know if you need assistance."
            }
        }
        
        speak(emergencyMessage)
        addMessage(AIMessage(
            text = "$emergencyMessage\nDetails: $details",
            isAI = true,
            timestamp = System.currentTimeMillis(),
            isEmergency = true
        ))
        
        Log.d(TAG, "Emergency triggered: $emergencyType - $details")
    }
    
    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "Service destroyed")
        
        if (::speechRecognizer.isInitialized) {
            speechRecognizer.destroy()
        }
        
        if (::textToSpeech.isInitialized) {
            textToSpeech.shutdown()
        }
        
        serviceScope.cancel()
    }
}

// AIState is defined here for use by the service/viewmodel
enum class AIState {
    IDLE,       // Ready to listen
    LISTENING,  // Actively listening to user
    PROCESSING, // Processing the speech
    SPEAKING,   // AI is speaking
    ERROR       // Error state
}