package com.vigilanceai

import android.Manifest
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.ServiceConnection
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.IBinder
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.compose.runtime.Composable
import androidx.core.content.ContextCompat
import androidx.navigation.compose.rememberNavController
import com.vigilanceai.navigation.NavGraph
import com.vigilanceai.service.VigilanceAIService
import com.vigilanceai.ui.theme.VigilanceAITheme
import com.vigilanceai.viewmodel.VigilanceViewModel

class MainActivity : ComponentActivity() {
    
    companion object {
        private const val TAG = "MainActivity"
    }
    
    private val viewModel: VigilanceViewModel by viewModels()
    
    // AI Service binding
    private var aiService: VigilanceAIService? = null
    private var serviceBound = false
    
    private val serviceConnection = object : ServiceConnection {
        override fun onServiceConnected(name: ComponentName?, service: IBinder?) {
            Log.d(TAG, "AI Service connected")
            val binder = service as VigilanceAIService.LocalBinder
            aiService = binder.getService()
            serviceBound = true
            
            // Bind service to ViewModel
            viewModel.bindAIService(binder.getService())
            
            // Service will automatically start listening for wake word
        }
        
        override fun onServiceDisconnected(name: ComponentName?) {
            Log.d(TAG, "AI Service disconnected")
            aiService = null
            serviceBound = false
        }
    }
    
    // Permission launcher
    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        val allGranted = permissions.entries.all { it.value }
        if (allGranted) {
            Log.d(TAG, "All permissions granted")
            startAIService()
        } else {
            Log.e(TAG, "Some permissions denied")
            // Show dialog explaining why permissions are needed
            showPermissionRationale()
        }
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        Log.d(TAG, "MainActivity created")
        
        // Request permissions
        requestNecessaryPermissions()
        
        setContent {
            VigilanceAITheme {
                MainContent()
            }
        }
    }
    
    @Composable
    private fun MainContent() {
        val navController = rememberNavController()
        NavGraph(
            navController = navController,
            viewModel = viewModel
        )
    }
    
    private fun requestNecessaryPermissions() {
        val permissions = arrayOf(
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.CAMERA,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )
        
        // Optional permissions (nice to have for emergency features)
        val optionalPermissions = arrayOf(
            Manifest.permission.CALL_PHONE,
            Manifest.permission.SEND_SMS
        )
        
        val allPermissions = permissions + optionalPermissions
        
        val permissionsToRequest = allPermissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }
        
        if (permissionsToRequest.isNotEmpty()) {
            Log.d(TAG, "Requesting permissions: ${permissionsToRequest.joinToString()}")
            permissionLauncher.launch(permissionsToRequest.toTypedArray())
        } else {
            Log.d(TAG, "All permissions already granted")
            startAIService()
        }
    }
    
    private fun startAIService() {
        Log.d(TAG, "Starting AI Service")
        Intent(this, VigilanceAIService::class.java).also { intent ->
            // Start service
            startService(intent)
            // Bind to service
            bindService(intent, serviceConnection, Context.BIND_AUTO_CREATE)
        }
    }
    
    private fun showPermissionRationale() {
        // TODO: Show a dialog explaining why permissions are needed
        // For now, just log
        Log.w(TAG, "Please grant necessary permissions for VigilanceAI to function properly")
        
        // You can show an AlertDialog here explaining:
        // - RECORD_AUDIO: For voice commands and wake word detection
        // - CAMERA: For drowsiness and emotion detection
        // - LOCATION: For finding nearby rest stops and emergency services
        // - PHONE/SMS: For emergency contact features
    }
    
    override fun onResume() {
        super.onResume()
        Log.d(TAG, "MainActivity resumed")
        
        // Restart listening if service is bound
        if (serviceBound && aiService != null) {
            aiService?.startContinuousListening()
        }
    }
    
    override fun onPause() {
        super.onPause()
        Log.d(TAG, "MainActivity paused")
        // Keep listening in background for safety
    }
    
    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "MainActivity destroyed")
        
        if (serviceBound) {
            unbindService(serviceConnection)
            serviceBound = false
        }
        
        // Keep service running for continuous monitoring
        // Service will be stopped when app is completely closed
    }
    
    override fun onBackPressed() {
        // Handle back press
        if (viewModel.aiConversationState.value.isActive) {
            // If AI conversation is active, dismiss it first
            viewModel.dismissAIConversation()
        } else if (viewModel.emergencyActivation.value.isTriggered) {
            // Don't allow back press during emergency
            return
        } else {
            super.onBackPressed()
        }
    }
}