package com.vigilanceai.navigation

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.vigilanceai.ui.components.BottomBar
import com.vigilanceai.ui.components.TopBar
import com.vigilanceai.ui.screens.*
import com.vigilanceai.ui.theme.*
import com.vigilanceai.viewmodel.VigilanceViewModel

/**
 * SAFE MINIMAL VERSION - Guaranteed to work
 * Use this version if the app is crashing
 */
@Composable
fun NavGraph(
    navController: NavHostController,
    viewModel: VigilanceViewModel
) {
    var currentScreen by remember { mutableStateOf("Dashboard") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF030712))
    ) {
        // Top Bar
        TopBar()

        Spacer(modifier = Modifier.height(16.dp))

        // Simple Navigation Buttons (instead of tabs)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 48.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Button(
                onClick = {
                    currentScreen = "Dashboard"
                    navController.navigate(Screen.Dashboard.route)
                },
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (currentScreen == "Dashboard")
                        Color(0xFF06B6D4) else Color(0xFF374151)
                )
            ) {
                Text("Dashboard")
            }

            Button(
                onClick = {
                    currentScreen = "Wellness"
                    navController.navigate(Screen.Wellness.route)
                },
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (currentScreen == "Wellness")
                        Color(0xFF06B6D4) else Color(0xFF374151)
                )
            ) {
                Text("Wellness")
            }

            Button(
                onClick = {
                    currentScreen = "Emergency"
                    navController.navigate(Screen.Emergency.route)
                },
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (currentScreen == "Emergency")
                        Color(0xFF06B6D4) else Color(0xFF374151)
                )
            ) {
                Text("Emergency")
            }

            Button(
                onClick = {
                    currentScreen = "CoPilot"
                    navController.navigate(Screen.CoPilot.route)
                },
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (currentScreen == "CoPilot")
                        Color(0xFF06B6D4) else Color(0xFF374151)
                )
            ) {
                Text("Co-Pilot")
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Content Area
        Box(modifier = Modifier.weight(1f)) {
            NavHost(
                navController = navController,
                startDestination = Screen.Dashboard.route
            ) {
                composable(Screen.Dashboard.route) {
                    DashboardScreen(viewModel)
                }
                composable(Screen.Wellness.route) {
                    WellnessScreen(viewModel)
                }
                composable(Screen.Emergency.route) {
                    EmergencyScreen(viewModel)
                }
                composable(Screen.CoPilot.route) {
                    CoPilotScreen(viewModel)
                }
            }
        }

        // Bottom Bar
        BottomBar()
    }

    // Overlay Screens
    val emergencyState by viewModel.emergencyActivation.collectAsState()
    val aiConversationState by viewModel.aiConversationState.collectAsState()

    // Emergency Activation Overlay
    if (emergencyState.isTriggered) {
        EmergencyActivationScreen(
            emergencyData = emergencyState,
            onCancelEmergency = { viewModel.cancelEmergency() },
            onConfirmEmergency = { /* Confirm emergency action */ }
        )
    }

    // AI Conversation Overlay
    if (aiConversationState.isActive) {
        AIConversationScreen(
            conversationState = aiConversationState,
            onStartListening = { viewModel.startListening() },
            onStopListening = { viewModel.stopListening() },
            onDismiss = { viewModel.dismissAIConversation() }
        )
    }
}