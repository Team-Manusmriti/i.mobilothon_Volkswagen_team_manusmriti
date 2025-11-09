package com.vigilanceai.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.vigilanceai.ui.theme.*
import com.vigilanceai.viewmodel.VigilanceViewModel

@Composable
fun DashboardScreen(viewModel: VigilanceViewModel) {
    val metrics by viewModel.metrics.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Gray950)
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 48.dp)
    ) {
        Spacer(modifier = Modifier.height(32.dp))

        // Main Content
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            // Left Panel - Wellness Score Card
            Card(
                modifier = Modifier
                    .weight(2f)
                    .height(480.dp),
                colors = CardDefaults.cardColors(containerColor = Gray800),
                shape = RoundedCornerShape(12.dp),
                border = androidx.compose.foundation.BorderStroke(1.dp, Gray700)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(32.dp)
                ) {
                    // Header Section
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.Top
                    ) {
                        // Left Content
                        Column {
                            Text(
                                text = "DRIVER WELLNESS",
                                style = MaterialTheme.typography.labelMedium,
                                color = Gray400,
                                letterSpacing = 1.sp,
                                modifier = Modifier.padding(bottom = 8.dp)
                            )

                            Text(
                                text = metrics.wellnessScore.toString(),
                                style = MaterialTheme.typography.displayLarge,
                                color = Cyan,
                                modifier = Modifier.padding(bottom = 8.dp)
                            )

                            Text(
                                text = "Optimal Condition",
                                style = MaterialTheme.typography.titleLarge,
                                color = Emerald,
                                fontWeight = FontWeight.Medium
                            )
                        }

                        // Right Content - Circle with Heart Icon
                        Box(
                            modifier = Modifier
                                .size(96.dp)
                                .border(4.dp, Cyan, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Favorite,
                                contentDescription = "Heart",
                                tint = Cyan,
                                modifier = Modifier.size(40.dp)
                            )
                        }
                    }

                    Spacer(modifier = Modifier.weight(1f))

                    // Bottom Metrics Grid
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        MetricItem(
                            label = "Alertness",
                            value = "${metrics.alertness}%",
                            color = Emerald,
                            modifier = Modifier.weight(1f)
                        )

                        MetricItem(
                            label = "Stress",
                            value = metrics.stress,
                            color = Cyan,
                            modifier = Modifier.weight(1f)
                        )

                        MetricItem(
                            label = "Fatigue",
                            value = "${metrics.fatigue}%",
                            color = Emerald,
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }

            // Right Panel - Quick Actions
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                QuickActionCard(
                    icon = Icons.Default.Psychology,
                    iconColor = Cyan,
                    label = "AI CO-PILOT",
                    status = "Ready to assist"
                )

                QuickActionCard(
                    icon = Icons.Default.Timeline,
                    iconColor = Emerald,
                    label = "TRIP TIME",
                    status = metrics.tripTime
                )

                QuickActionCard(
                    icon = Icons.Default.Navigation,
                    iconColor = Blue,
                    label = "DESTINATION",
                    status = metrics.destination
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Test Controls
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Button(
                onClick = { viewModel.simulateAccident() },
                modifier = Modifier.weight(1f),
                colors = ButtonDefaults.buttonColors(containerColor = Red)
            ) {
                Text("Test Emergency")
            }
            
            Button(
                onClick = { viewModel.startAIConversation("FATIGUE") },
                modifier = Modifier.weight(1f),
                colors = ButtonDefaults.buttonColors(containerColor = Cyan)
            ) {
                Text("Test AI Chat")
            }
        }

        Spacer(modifier = Modifier.height(32.dp))
    }
}

@Composable
fun MetricItem(
    label: String,
    value: String,
    color: androidx.compose.ui.graphics.Color,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium,
            color = Gray400,
            modifier = Modifier.padding(bottom = 4.dp)
        )
        Text(
            text = value,
            style = MaterialTheme.typography.displayMedium.copy(fontSize = 24.sp),
            color = color,
            fontWeight = FontWeight.Bold
        )
    }
}

@Composable
fun QuickActionCard(
    icon: ImageVector,
    iconColor: androidx.compose.ui.graphics.Color,
    label: String,
    status: String
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(140.dp),
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
                contentDescription = label,
                tint = iconColor,
                modifier = Modifier.size(24.dp)
            )

            Column {
                Text(
                    text = label,
                    style = MaterialTheme.typography.labelMedium,
                    color = Gray400,
                    letterSpacing = 0.5.sp,
                    modifier = Modifier.padding(bottom = 4.dp)
                )

                Text(
                    text = status,
                    style = MaterialTheme.typography.bodyLarge,
                    color = androidx.compose.ui.graphics.Color.White,
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }
}