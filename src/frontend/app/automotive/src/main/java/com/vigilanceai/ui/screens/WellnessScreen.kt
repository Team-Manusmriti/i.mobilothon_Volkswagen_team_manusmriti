package com.vigilanceai.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.vigilanceai.ui.components.DetailedMetricCard
import com.vigilanceai.ui.components.DrivingMetric
import com.vigilanceai.ui.theme.*
import com.vigilanceai.viewmodel.VigilanceViewModel

/**
 * Wellness Monitor Screen
 * Displays detailed health and wellness metrics for the driver including:
 * - Eye Activity (PERCLOS) monitoring
 * - Heart Rate tracking
 * - Facial Emotion Recognition
 * - Driving Pattern Analysis (Lane keeping, Steering, Speed control)
 */
@Composable
fun WellnessScreen(viewModel: VigilanceViewModel) {
    // Collect metrics from ViewModel's StateFlow
    val metrics by viewModel.metrics.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Gray950)
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 48.dp)
    ) {
        Spacer(modifier = Modifier.height(32.dp))

        // Header Section
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Wellness Monitor",
                style = MaterialTheme.typography.headlineLarge,
                color = Color.White,
                fontWeight = FontWeight.Bold
            )

            Text(
                text = "Real-time Analysis",
                style = MaterialTheme.typography.labelMedium,
                color = Gray400,
                letterSpacing = 0.5.sp
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Primary Metrics Row - Eye Activity & Heart Rate
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            // Eye Activity Card (PERCLOS)
            DetailedMetricCard(
                label = "EYE ACTIVITY (PERCLOS)",
                value = "${metrics.perclos}%",
                status = "Within safe range",
                accentColor = Cyan,
                modifier = Modifier.weight(1f)
            )

            // Heart Rate Card
            DetailedMetricCard(
                label = "HEART RATE",
                value = "${metrics.heartRate} BPM",
                status = "Normal rhythm",
                accentColor = Blue,
                modifier = Modifier.weight(1f)
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Facial Emotion Recognition Card
        EmotionRecognitionCard(
            emotionState = metrics.emotionState,
            emotionConfidence = metrics.emotionConfidence
        )

        Spacer(modifier = Modifier.height(24.dp))

        // Driving Pattern Analysis Card
        DrivingPatternCard(
            laneKeeping = metrics.laneKeeping,
            steeringInput = metrics.steeringInput,
            speedControl = metrics.speedControl
        )
    }
}

/**
 * Emotion Recognition Card Component
 * Shows facial emotion analysis with progress bar
 */
@Composable
fun EmotionRecognitionCard(
    emotionState: String,
    emotionConfidence: Int
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(160.dp),
        colors = CardDefaults.cardColors(containerColor = Gray800),
        shape = RoundedCornerShape(12.dp),
        border = androidx.compose.foundation.BorderStroke(1.dp, Gray700)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(32.dp)
        ) {
            // Card Title
            Text(
                text = "FACIAL EMOTION RECOGNITION",
                style = MaterialTheme.typography.labelMedium,
                color = Gray400,
                letterSpacing = 1.sp,
                modifier = Modifier.padding(bottom = 20.dp)
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Left Section - Emotion State and Progress Bar
                Column(
                    modifier = Modifier.weight(0.8f)
                ) {
                    // Emotion State with Indicator Dot
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.padding(bottom = 8.dp)
                    ) {
                        // Green indicator dot
                        Box(
                            modifier = Modifier
                                .size(12.dp)
                                .clip(CircleShape)
                                .background(Emerald)
                        )

                        Spacer(modifier = Modifier.width(8.dp))

                        Text(
                            text = emotionState,
                            style = MaterialTheme.typography.titleLarge,
                            color = Color.White,
                            fontWeight = FontWeight.Medium
                        )
                    }

                    // Progress Bar Background
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(8.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .background(Gray700)
                    ) {
                        // Progress Bar Fill
                        Box(
                            modifier = Modifier
                                .fillMaxWidth(emotionConfidence / 100f)
                                .fillMaxHeight()
                                .clip(RoundedCornerShape(4.dp))
                                .background(Emerald)
                        )
                    }
                }

                // Right Section - Confidence Percentage
                Text(
                    text = "$emotionConfidence%",
                    style = MaterialTheme.typography.headlineLarge,
                    color = Emerald,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}

/**
 * Driving Pattern Analysis Card Component
 * Shows lane keeping, steering input, and speed control metrics
 */
@Composable
fun DrivingPatternCard(
    laneKeeping: String,
    steeringInput: String,
    speedControl: String
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(200.dp),
        colors = CardDefaults.cardColors(containerColor = Gray800),
        shape = RoundedCornerShape(12.dp),
        border = androidx.compose.foundation.BorderStroke(1.dp, Gray700)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(32.dp)
        ) {
            // Card Title
            Text(
                text = "DRIVING PATTERN ANALYSIS",
                style = MaterialTheme.typography.labelMedium,
                color = Gray400,
                letterSpacing = 1.sp,
                modifier = Modifier.padding(bottom = 20.dp)
            )

            // Three Column Metrics Layout
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(24.dp)
            ) {
                // Lane Keeping Metric
                DrivingMetric(
                    label = "Lane Keeping",
                    value = laneKeeping,
                    color = Emerald,
                    modifier = Modifier.weight(1f)
                )

                // Steering Input Metric
                DrivingMetric(
                    label = "Steering Input",
                    value = steeringInput,
                    color = Cyan,
                    modifier = Modifier.weight(1f)
                )

                // Speed Control Metric
                DrivingMetric(
                    label = "Speed Control",
                    value = speedControl,
                    color = Emerald,
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

/**
 * Preview for WellnessScreen
 * Shows the screen at 1920x1080 resolution (automotive display)
 */
@Preview(showBackground = true, widthDp = 1920, heightDp = 1080)
@Composable
fun WellnessScreenPreview() {
    VigilanceAITheme {
        WellnessScreen(viewModel = VigilanceViewModel())
    }
}

/**
 * Preview for Emotion Recognition Card only
 */
@Preview(showBackground = true, widthDp = 800)
@Composable
fun EmotionRecognitionCardPreview() {
    VigilanceAITheme {
        EmotionRecognitionCard(
            emotionState = "Calm & Focused",
            emotionConfidence = 85
        )
    }
}

/**
 * Preview for Driving Pattern Card only
 */
@Preview(showBackground = true, widthDp = 800)
@Composable
fun DrivingPatternCardPreview() {
    VigilanceAITheme {
        DrivingPatternCard(
            laneKeeping = "Stable",
            steeringInput = "Smooth",
            speedControl = "Steady"
        )
    }
}