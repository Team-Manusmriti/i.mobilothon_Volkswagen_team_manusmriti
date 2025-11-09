package com.vigilanceai.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.vigilanceai.ui.theme.*
import com.vigilanceai.viewmodel.VigilanceViewModel
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun CoPilotScreen(viewModel: VigilanceViewModel) {
    val suggestion by viewModel.currentSuggestion.collectAsState()
    val interactions by viewModel.interactionHistory.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Gray950)
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 48.dp)
    ) {
        Spacer(modifier = Modifier.height(32.dp))

        // Header
        Row(
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .background(Cyan, RoundedCornerShape(8.dp)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Psychology,
                    contentDescription = "AI",
                    tint = Color.White,
                    modifier = Modifier.size(24.dp)
                )
            }

            Column {
                Text(
                    text = "AI Co-Pilot",
                    style = MaterialTheme.typography.headlineLarge,
                    color = Color.White,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = "Conversational Assistant",
                    style = MaterialTheme.typography.bodyMedium,
                    color = Gray400
                )
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Featured Suggestion Card
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .height(240.dp),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(
                containerColor = Color.Transparent
            )
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        brush = Brush.horizontalGradient(
                            colors = listOf(Cyan, Blue)
                        )
                    )
                    .padding(32.dp)
            ) {
                Column(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Coffee,
                            contentDescription = "Coffee",
                            tint = Color.White,
                            modifier = Modifier.size(24.dp)
                        )

                        Column {
                            Text(
                                text = suggestion.title,
                                style = MaterialTheme.typography.titleLarge.copy(fontSize = 18.sp),
                                color = Color.White,
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier.padding(bottom = 8.dp)
                            )
                            Text(
                                text = suggestion.description,
                                style = MaterialTheme.typography.bodyLarge,
                                color = Color.White.copy(alpha = 0.9f),
                                lineHeight = 21.sp
                            )
                        }
                    }

                    Row(
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Button(
                            onClick = { /* Navigate action */ },
                            modifier = Modifier.height(48.dp),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color.White
                            ),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Text(
                                text = suggestion.primaryAction,
                                style = MaterialTheme.typography.titleLarge,
                                color = Cyan.copy(alpha = 0.8f),
                                fontWeight = FontWeight.Bold
                            )
                        }

                        Button(
                            onClick = { /* Remind action */ },
                            modifier = Modifier.height(48.dp),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Cyan.copy(alpha = 0.3f)
                            ),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Text(
                                text = suggestion.secondaryAction,
                                style = MaterialTheme.typography.titleLarge,
                                color = Color.White,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Context-Aware Actions
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            ActionCard(
                icon = Icons.Default.MusicNote,
                iconColor = Blue,
                title = "Play Calming Music",
                description = "Reduce stress levels",
                modifier = Modifier.weight(1f)
            )

            ActionCard(
                icon = Icons.Default.Navigation,
                iconColor = Emerald,
                title = "Alternate Route",
                description = "Avoid heavy traffic",
                modifier = Modifier.weight(1f)
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Conversation History
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .height(280.dp),
            colors = CardDefaults.cardColors(containerColor = Gray800),
            shape = RoundedCornerShape(12.dp),
            border = androidx.compose.foundation.BorderStroke(1.dp, Gray700)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(24.dp)
            ) {
                Text(
                    text = "RECENT INTERACTIONS",
                    style = MaterialTheme.typography.labelMedium,
                    color = Gray400,
                    letterSpacing = 1.sp,
                    modifier = Modifier.padding(bottom = 20.dp)
                )

                Column(
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    // Show AI conversation messages if available
                    val conversationMessages by viewModel.conversationMessages.collectAsState()
                    val aiConversationState by viewModel.aiConversationState.collectAsState()
                    
                    if (conversationMessages.isNotEmpty()) {
                        // AIMessage uses a Long timestamp and stores text/isAI
                        conversationMessages.takeLast(3).forEach { message ->
                            val timeStr = SimpleDateFormat("HH:mm", Locale.getDefault()).format(Date(message.timestamp))
                            val senderLabel = if (message.isAI) "AI" else "You"
                            InteractionItem(
                                time = timeStr,
                                message = "$senderLabel: ${message.text}"
                            )
                        }
                    } else {
                        // Fallback to regular interactions
                        interactions.takeLast(3).forEach { interaction ->
                            InteractionItem(
                                time = interaction.time,
                                message = interaction.message
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ActionCard(
    icon: ImageVector,
    iconColor: androidx.compose.ui.graphics.Color,
    title: String,
    description: String,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .height(180.dp)
            .clickable { /* Action */ },
        colors = CardDefaults.cardColors(containerColor = Gray800),
        shape = RoundedCornerShape(12.dp),
        border = androidx.compose.foundation.BorderStroke(1.dp, Gray700)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Icon(
                imageVector = icon,
                contentDescription = title,
                tint = iconColor,
                modifier = Modifier.size(20.dp)
            )

            Column {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleLarge,
                    color = Color.White,
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.padding(bottom = 6.dp)
                )
                Text(
                    text = description,
                    style = MaterialTheme.typography.bodyMedium,
                    color = Gray400
                )
            }
        }
    }
}

@Composable
fun InteractionItem(time: String, message: String) {
    Row(
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = time,
            style = MaterialTheme.typography.bodyLarge,
            color = Gray500,
            modifier = Modifier.width(48.dp)
        )
        Text(
            text = message,
            style = MaterialTheme.typography.bodyLarge,
            color = Gray300
        )
    }
}