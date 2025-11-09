// Premium AIConversationScreen.kt
// Replace your existing AIConversationScreen.kt with this enhanced version

package com.vigilanceai.ui.screens

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.blur
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.vigilanceai.data.AIConversationState
import com.vigilanceai.service.AIMessage
import com.vigilanceai.ui.components.WaveformAnimation
import com.vigilanceai.ui.theme.*
import kotlinx.coroutines.launch

@Composable
fun AIConversationScreen(
    conversationState: AIConversationState,
    messages: List<AIMessage> = emptyList(),
    onStartListening: () -> Unit = {},
    onStopListening: () -> Unit = {},
    onDismiss: () -> Unit = {}
) {
    val listState = rememberLazyListState()
    val coroutineScope = rememberCoroutineScope()
    
    // Auto-scroll to bottom when new messages arrive
    LaunchedEffect(messages.size) {
        if (messages.isNotEmpty()) {
            coroutineScope.launch {
                listState.animateScrollToItem(messages.size - 1)
            }
        }
    }
    
    // Pulsing animation for active states
    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val pulseScale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1.05f,
        animationSpec = infiniteRepeatable(
            animation = tween(1500, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulse_scale"
    )
    
    val glowAlpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 0.7f,
        animationSpec = infiniteRepeatable(
            animation = tween(2000, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "glow_alpha"
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.verticalGradient(
                    colors = listOf(
                        Color(0xFF0A0E1A),
                        Color(0xFF030712),
                        Color.Black
                    )
                )
            )
    ) {
        // Animated background circles
        Box(
            modifier = Modifier
                .fillMaxSize()
                .blur(100.dp)
        ) {
            // Cyan glow
            Box(
                modifier = Modifier
                    .size(400.dp)
                    .offset(x = (-100).dp, y = 100.dp)
                    .scale(if (conversationState.isListening) pulseScale else 1f)
                    .background(
                        Cyan.copy(alpha = if (conversationState.isListening) glowAlpha else 0.2f),
                        CircleShape
                    )
            )
            
            // Blue glow
            Box(
                modifier = Modifier
                    .size(350.dp)
                    .align(Alignment.TopEnd)
                    .offset(x = 100.dp, y = (-50).dp)
                    .scale(if (conversationState.isSpeaking) pulseScale else 1f)
                    .background(
                        Blue.copy(alpha = if (conversationState.isSpeaking) glowAlpha else 0.15f),
                        CircleShape
                    )
            )
        }
        
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(40.dp)
        ) {
            // Premium Header
            PremiumHeader(
                conversationState = conversationState,
                onDismiss = onDismiss
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Alert Banner (if triggered)
            AnimatedVisibility(
                visible = conversationState.triggerReason.isNotEmpty(),
                enter = slideInVertically() + fadeIn(),
                exit = slideOutVertically() + fadeOut()
            ) {
                AlertBanner(
                    triggerReason = conversationState.triggerReason,
                    message = conversationState.currentMessage
                )
            }
            
            if (conversationState.triggerReason.isNotEmpty()) {
                Spacer(modifier = Modifier.height(24.dp))
            }
            
            // Central AI Visualizer
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(280.dp),
                contentAlignment = Alignment.Center
            ) {
                // Outer glow ring
                if (conversationState.isListening || conversationState.isSpeaking) {
                    Box(
                        modifier = Modifier
                            .size(240.dp)
                            .scale(pulseScale)
                            .border(
                                width = 2.dp,
                                brush = Brush.horizontalGradient(
                                    colors = listOf(
                                        Cyan.copy(alpha = glowAlpha),
                                        Blue.copy(alpha = glowAlpha),
                                        Cyan.copy(alpha = glowAlpha)
                                    )
                                ),
                                shape = CircleShape
                            )
                    )
                }
                
                // Main AI Circle
                Box(
                    modifier = Modifier
                        .size(200.dp)
                        .background(
                            brush = Brush.radialGradient(
                                colors = listOf(
                                    when {
                                        conversationState.isListening -> Cyan.copy(alpha = 0.4f)
                                        conversationState.isSpeaking -> Blue.copy(alpha = 0.4f)
                                        conversationState.isProcessing -> Color(0xFF8B5CF6).copy(alpha = 0.4f)
                                        else -> Gray800.copy(alpha = 0.6f)
                                    },
                                    Color.Transparent
                                )
                            ),
                            shape = CircleShape
                        )
                        .border(
                            width = 1.dp,
                            color = when {
                                conversationState.isListening -> Cyan.copy(alpha = 0.6f)
                                conversationState.isSpeaking -> Blue.copy(alpha = 0.6f)
                                else -> Gray700.copy(alpha = 0.4f)
                            },
                            shape = CircleShape
                        ),
                    contentAlignment = Alignment.Center
                ) {
                    // Waveform or Icon
                    if (conversationState.isListening || conversationState.isSpeaking) {
                        WaveformAnimation(
                            isListening = conversationState.isListening,
                            modifier = Modifier.size(140.dp)
                        )
                    } else {
                        Icon(
                            imageVector = when {
                                conversationState.isProcessing -> Icons.Default.Psychology
                                else -> Icons.Default.Assistant
                            },
                            contentDescription = "AI Status",
                            tint = when {
                                conversationState.isProcessing -> Color(0xFF8B5CF6)
                                else -> Cyan
                            },
                            modifier = Modifier.size(80.dp)
                        )
                    }
                }
                
                // Status Text Below Circle
                Column(
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .offset(y = 40.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = when {
                            conversationState.isListening -> "Listening to you..."
                            conversationState.isProcessing -> "Processing..."
                            conversationState.isSpeaking -> "Speaking..."
                            else -> "Ready to assist"
                        },
                        style = MaterialTheme.typography.titleLarge,
                        color = when {
                            conversationState.isListening -> Cyan
                            conversationState.isSpeaking -> Blue
                            conversationState.isProcessing -> Color(0xFF8B5CF6)
                            else -> Gray400
                        },
                        fontWeight = FontWeight.Bold
                    )
                    
                    if (!conversationState.isListening && !conversationState.isSpeaking) {
                        Text(
                            text = "Say \"VigilanceAI\" or tap microphone",
                            style = MaterialTheme.typography.bodyMedium,
                            color = Gray500,
                            modifier = Modifier.padding(top = 4.dp)
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Conversation History
            if (messages.isNotEmpty()) {
                Text(
                    text = "Conversation",
                    style = MaterialTheme.typography.labelLarge,
                    color = Gray400,
                    letterSpacing = 1.sp,
                    modifier = Modifier.padding(bottom = 12.dp)
                )
                
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                    colors = CardDefaults.cardColors(
                        containerColor = Gray900.copy(alpha = 0.4f)
                    ),
                    shape = RoundedCornerShape(20.dp),
                    border = androidx.compose.foundation.BorderStroke(
                        1.dp,
                        Gray700.copy(alpha = 0.3f)
                    )
                ) {
                    LazyColumn(
                        state = listState,
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(20.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        items(messages) { message ->
                            EnhancedConversationBubble(message)
                        }
                    }
                }
            } else {
                // Empty State
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.RecordVoiceOver,
                            contentDescription = null,
                            tint = Gray600,
                            modifier = Modifier.size(64.dp)
                        )
                        Text(
                            text = "Start a conversation",
                            style = MaterialTheme.typography.titleLarge,
                            color = Gray400,
                            fontWeight = FontWeight.Medium
                        )
                        Text(
                            text = "Your wellness companion is ready to listen",
                            style = MaterialTheme.typography.bodyMedium,
                            color = Gray500,
                            textAlign = TextAlign.Center
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Control Panel
            PremiumControlPanel(
                conversationState = conversationState,
                onStartListening = onStartListening,
                onStopListening = onStopListening
            )
            
            Spacer(modifier = Modifier.height(20.dp))
            
            // Quick Actions
            QuickActionsRow()
        }
    }
}

@Composable
fun PremiumHeader(
    conversationState: AIConversationState,
    onDismiss: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // AI Avatar
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .background(
                        brush = Brush.linearGradient(
                            colors = listOf(Cyan.copy(alpha = 0.3f), Blue.copy(alpha = 0.3f))
                        ),
                        shape = CircleShape
                    )
                    .border(1.dp, Cyan.copy(alpha = 0.5f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.SmartToy,
                    contentDescription = "AI",
                    tint = Cyan,
                    modifier = Modifier.size(32.dp)
                )
            }
            
            Column {
                Text(
                    text = "VigilanceAI",
                    style = MaterialTheme.typography.headlineMedium,
                    color = Color.White,
                    fontWeight = FontWeight.Bold
                )
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .background(Emerald, CircleShape)
                    )
                    Text(
                        text = "Active & Monitoring",
                        style = MaterialTheme.typography.bodyMedium,
                        color = Gray400
                    )
                }
            }
        }
        
        // Close Button
        IconButton(
            onClick = onDismiss,
            modifier = Modifier
                .size(48.dp)
                .background(Gray800.copy(alpha = 0.6f), CircleShape)
        ) {
            Icon(
                imageVector = Icons.Default.Close,
                contentDescription = "Close",
                tint = Gray300
            )
        }
    }
}

@Composable
fun AlertBanner(
    triggerReason: String,
    message: String
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = when (triggerReason) {
                "DROWSINESS", "FATIGUE" -> Red.copy(alpha = 0.15f)
                "STRESS" -> Color(0xFFFFA500).copy(alpha = 0.15f)
                else -> Cyan.copy(alpha = 0.15f)
            }
        ),
        shape = RoundedCornerShape(16.dp),
        border = androidx.compose.foundation.BorderStroke(
            1.dp,
            when (triggerReason) {
                "DROWSINESS", "FATIGUE" -> Red.copy(alpha = 0.4f)
                "STRESS" -> Color(0xFFFFA500).copy(alpha = 0.4f)
                else -> Cyan.copy(alpha = 0.4f)
            }
        )
    ) {
        Row(
            modifier = Modifier.padding(20.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Alert Icon
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .background(
                        when (triggerReason) {
                            "DROWSINESS", "FATIGUE" -> Red.copy(alpha = 0.2f)
                            "STRESS" -> Color(0xFFFFA500).copy(alpha = 0.2f)
                            else -> Cyan.copy(alpha = 0.2f)
                        },
                        CircleShape
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Warning,
                    contentDescription = "Alert",
                    tint = when (triggerReason) {
                        "DROWSINESS", "FATIGUE" -> Red
                        "STRESS" -> Color(0xFFFFA500)
                        else -> Cyan
                    },
                    modifier = Modifier.size(28.dp)
                )
            }
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = triggerReason.replace("_", " "),
                    style = MaterialTheme.typography.titleMedium,
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 0.5.sp
                )
                if (message.isNotEmpty()) {
                    Text(
                        text = message,
                        style = MaterialTheme.typography.bodyMedium,
                        color = Gray300,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }
            }
        }
    }
}

@Composable
fun PremiumControlPanel(
    conversationState: AIConversationState,
    onStartListening: () -> Unit,
    onStopListening: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Main Microphone Button
        Button(
            onClick = if (conversationState.isListening) onStopListening else onStartListening,
            modifier = Modifier.size(88.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = Color.Transparent
            ),
            contentPadding = PaddingValues(0.dp),
            shape = CircleShape
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        brush = Brush.linearGradient(
                            colors = if (conversationState.isListening) {
                                listOf(Red, Color(0xFFDC2626))
                            } else {
                                listOf(Emerald, Color(0xFF059669))
                            }
                        ),
                        shape = CircleShape
                    )
                    .border(
                        width = 3.dp,
                        color = if (conversationState.isListening) {
                            Red.copy(alpha = 0.5f)
                        } else {
                            Emerald.copy(alpha = 0.5f)
                        },
                        shape = CircleShape
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = if (conversationState.isListening) {
                        Icons.Default.Stop
                    } else {
                        Icons.Default.Mic
                    },
                    contentDescription = if (conversationState.isListening) "Stop" else "Listen",
                    tint = Color.White,
                    modifier = Modifier.size(42.dp)
                )
            }
        }
    }
}

@Composable
fun EnhancedConversationBubble(message: AIMessage) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (message.isAI) Arrangement.Start else Arrangement.End
    ) {
        if (message.isAI) {
            // AI Avatar for AI messages
            Box(
                modifier = Modifier
                    .size(36.dp)
                    .background(Cyan.copy(alpha = 0.2f), CircleShape)
                    .border(1.dp, Cyan.copy(alpha = 0.4f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.SmartToy,
                    contentDescription = "AI",
                    tint = Cyan,
                    modifier = Modifier.size(20.dp)
                )
            }
            
            Spacer(modifier = Modifier.width(12.dp))
        }
        
        Card(
            modifier = Modifier.widthIn(max = 500.dp),
            colors = CardDefaults.cardColors(
                containerColor = if (message.isEmergency) {
                    Red.copy(alpha = 0.2f)
                } else if (message.isAI) {
                    Gray800.copy(alpha = 0.6f)
                } else {
                    Cyan.copy(alpha = 0.15f)
                }
            ),
            shape = RoundedCornerShape(
                topStart = 20.dp,
                topEnd = 20.dp,
                bottomStart = if (message.isAI) 4.dp else 20.dp,
                bottomEnd = if (message.isAI) 20.dp else 4.dp
            ),
            border = androidx.compose.foundation.BorderStroke(
                width = 1.dp,
                color = if (message.isEmergency) {
                    Red.copy(alpha = 0.4f)
                } else if (message.isAI) {
                    Gray700.copy(alpha = 0.3f)
                } else {
                    Cyan.copy(alpha = 0.3f)
                }
            )
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                if (message.isEmergency) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Warning,
                            contentDescription = "Emergency",
                            tint = Red,
                            modifier = Modifier.size(14.dp)
                        )
                        Text(
                            text = "EMERGENCY ALERT",
                            style = MaterialTheme.typography.labelSmall,
                            color = Red,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                }
                
                Text(
                    text = message.text,
                    style = MaterialTheme.typography.bodyLarge,
                    color = Color.White,
                    lineHeight = 22.sp
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                Text(
                    text = formatTimestamp(message.timestamp),
                    style = MaterialTheme.typography.bodySmall,
                    color = Gray500
                )
            }
        }
        
        if (!message.isAI) {
            Spacer(modifier = Modifier.width(12.dp))
            
            // User Avatar
            Box(
                modifier = Modifier
                    .size(36.dp)
                    .background(Gray700, CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Person,
                    contentDescription = "User",
                    tint = Gray400,
                    modifier = Modifier.size(20.dp)
                )
            }
        }
    }
}

@Composable
fun QuickActionsRow() {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        QuickActionChip(
            text = "I'm fine",
            icon = Icons.Default.ThumbUp,
            onClick = { /* TODO */ }
        )
        QuickActionChip(
            text = "Need break",
            icon = Icons.Default.LocalCafe,
            onClick = { /* TODO */ }
        )
        QuickActionChip(
            text = "Find rest stop",
            icon = Icons.Default.LocalParking,
            onClick = { /* TODO */ }
        )
    }
}

@Composable
fun RowScope.QuickActionChip(
    text: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    onClick: () -> Unit
) {
    Button(
        onClick = onClick,
        modifier = Modifier
            .weight(1f)
            .height(48.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = Gray800.copy(alpha = 0.6f)
        ),
        shape = RoundedCornerShape(12.dp),
        border = androidx.compose.foundation.BorderStroke(1.dp, Gray700.copy(alpha = 0.4f))
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = Cyan,
            modifier = Modifier.size(18.dp)
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text(
            text = text,
            style = MaterialTheme.typography.bodyMedium,
            color = Color.White
        )
    }
}

private fun formatTimestamp(timestamp: Long): String {
    val now = System.currentTimeMillis()
    val diff = now - timestamp
    
    return when {
        diff < 60000 -> "Just now"
        diff < 3600000 -> "${diff / 60000}m ago"
        diff < 86400000 -> "${diff / 3600000}h ago"
        else -> "${diff / 86400000}d ago"
    }
}