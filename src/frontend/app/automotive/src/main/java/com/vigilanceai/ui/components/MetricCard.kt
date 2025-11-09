package com.vigilanceai.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import com.vigilanceai.ui.theme.*

/**
 * MetricCard.kt
 * Reusable card components for displaying various metrics across the app
 *
 * Contains 4 main components:
 * 1. MetricItem - Small metric display (Alertness, Stress, Fatigue)
 * 2. QuickActionCard - Action cards with icons (AI Co-Pilot, Trip Time, Destination)
 * 3. DetailedMetricCard - Large metric cards with accent borders (Eye Activity, Heart Rate)
 * 4. DrivingMetric - Driving pattern metrics (Lane Keeping, Steering, Speed)
 */

// ========================================
// 1. METRIC ITEM COMPONENT
// ========================================
/**
 * MetricItem Component
 * Used in Dashboard for displaying wellness metrics
 * Shows label above value in a compact format
 *
 * @param label Text label (e.g., "Alertness")
 * @param value Metric value (e.g., "98%")
 * @param color Color for the value text
 * @param modifier Optional modifier for customization
 *
 * Usage: Dashboard bottom metrics (Alertness, Stress, Fatigue)
 */
@Composable
fun MetricItem(
    label: String,
    value: String,
    color: Color,
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

// ========================================
// 2. QUICK ACTION CARD COMPONENT
// ========================================
/**
 * QuickActionCard Component
 * Used in Dashboard for quick access cards
 * Shows icon at top, label and status at bottom
 *
 * @param icon Material Icon to display
 * @param iconColor Color of the icon
 * @param label Uppercase label text (e.g., "AI CO-PILOT")
 * @param status Status text (e.g., "Ready to assist")
 * @param modifier Optional modifier for customization
 *
 * Usage: Dashboard right panel (AI Co-Pilot, Trip Time, Destination)
 * Size: Full width x 140dp height
 */
@Composable
fun QuickActionCard(
    icon: ImageVector,
    iconColor: Color,
    label: String,
    status: String,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
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
            // Icon at top
            Icon(
                imageVector = icon,
                contentDescription = label,
                tint = iconColor,
                modifier = Modifier.size(24.dp)
            )

            // Label and status at bottom
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
                    color = Color.White,
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }
}

// ========================================
// 3. DETAILED METRIC CARD COMPONENT
// ========================================
/**
 * DetailedMetricCard Component
 * Used in Wellness Screen for primary health metrics
 * Features a thick colored left border for visual emphasis
 *
 * @param label Metric label (e.g., "EYE ACTIVITY (PERCLOS)")
 * @param value Large metric value (e.g., "4.2%")
 * @param status Status message (e.g., "Within safe range")
 * @param accentColor Color for the border and value
 * @param modifier Optional modifier for customization
 *
 * Usage: Wellness Screen top cards (Eye Activity, Heart Rate)
 * Size: 50% width x 180dp height
 * Border: 4px thick accent border on left side
 */
@Composable
fun DetailedMetricCard(
    label: String,
    value: String,
    status: String,
    accentColor: Color,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.height(180.dp),
        colors = CardDefaults.cardColors(containerColor = Gray800),
        shape = RoundedCornerShape(12.dp),
        border = androidx.compose.foundation.BorderStroke(
            width = 4.dp,
            color = accentColor
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(32.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Label at top
            Text(
                text = label,
                style = MaterialTheme.typography.labelMedium,
                color = Gray400,
                letterSpacing = 1.sp
            )

            // Large value in middle
            Text(
                text = value,
                style = MaterialTheme.typography.displayMedium,
                color = accentColor,
                fontWeight = FontWeight.Bold
            )

            // Status at bottom
            Text(
                text = status,
                style = MaterialTheme.typography.bodyMedium,
                color = Emerald
            )
        }
    }
}

// ========================================
// 4. DRIVING METRIC COMPONENT
// ========================================
/**
 * DrivingMetric Component
 * Used in Wellness Screen for driving pattern analysis
 * Simple centered text layout showing label and value
 *
 * @param label Metric name (e.g., "Lane Keeping")
 * @param value Metric status (e.g., "Stable")
 * @param color Color for the value text
 * @param modifier Optional modifier for customization
 *
 * Usage: Wellness Screen Driving Pattern Analysis card
 * Layout: Three columns with equal width
 */
@Composable
fun DrivingMetric(
    label: String,
    value: String,
    color: Color,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium,
            color = Gray400,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        Text(
            text = value,
            style = MaterialTheme.typography.titleLarge.copy(fontSize = 20.sp),
            color = color,
            fontWeight = FontWeight.Bold
        )
    }
}

// ========================================
// PREVIEW FUNCTIONS
// ========================================

/**
 * Preview for MetricItem
 * Shows three metrics in a row (Dashboard style)
 */
@Preview(showBackground = true, widthDp = 800)
@Composable
fun MetricItemPreview() {
    VigilanceAITheme {
        Row(modifier = Modifier.padding(16.dp)) {
            MetricItem(
                label = "Alertness",
                value = "98%",
                color = Emerald,
                modifier = Modifier.weight(1f)
            )
            MetricItem(
                label = "Stress",
                value = "Low",
                color = Cyan,
                modifier = Modifier.weight(1f)
            )
            MetricItem(
                label = "Fatigue",
                value = "12%",
                color = Emerald,
                modifier = Modifier.weight(1f)
            )
        }
    }
}

/**
 * Preview for QuickActionCard
 * Shows a single action card with AI Co-Pilot example
 */
@Preview(showBackground = true, widthDp = 400)
@Composable
fun QuickActionCardPreview() {
    VigilanceAITheme {
        QuickActionCard(
            icon = Icons.Default.Psychology,
            iconColor = Cyan,
            label = "AI CO-PILOT",
            status = "Ready to assist"
        )
    }
}

/**
 * Preview for QuickActionCard - Trip Time
 */
@Preview(showBackground = true, widthDp = 400)
@Composable
fun QuickActionCardTripTimePreview() {
    VigilanceAITheme {
        QuickActionCard(
            icon = Icons.Default.Timeline,
            iconColor = Emerald,
            label = "TRIP TIME",
            status = "1h 23m"
        )
    }
}

/**
 * Preview for QuickActionCard - Destination
 */
@Preview(showBackground = true, widthDp = 400)
@Composable
fun QuickActionCardDestinationPreview() {
    VigilanceAITheme {
        QuickActionCard(
            icon = Icons.Default.Navigation,
            iconColor = Blue,
            label = "DESTINATION",
            status = "45 min away"
        )
    }
}

/**
 * Preview for DetailedMetricCard
 * Shows Eye Activity card with cyan accent
 */
@Preview(showBackground = true, widthDp = 600)
@Composable
fun DetailedMetricCardPreview() {
    VigilanceAITheme {
        DetailedMetricCard(
            label = "EYE ACTIVITY (PERCLOS)",
            value = "4.2%",
            status = "Within safe range",
            accentColor = Cyan
        )
    }
}

/**
 * Preview for DetailedMetricCard - Heart Rate
 */
@Preview(showBackground = true, widthDp = 600)
@Composable
fun DetailedMetricCardHeartRatePreview() {
    VigilanceAITheme {
        DetailedMetricCard(
            label = "HEART RATE",
            value = "72 BPM",
            status = "Normal rhythm",
            accentColor = Blue
        )
    }
}

/**
 * Preview for DrivingMetric
 * Shows three driving metrics in a row
 */
@Preview(showBackground = true, widthDp = 800)
@Composable
fun DrivingMetricPreview() {
    VigilanceAITheme {
        Row(modifier = Modifier.padding(16.dp)) {
            DrivingMetric(
                label = "Lane Keeping",
                value = "Stable",
                color = Emerald,
                modifier = Modifier.weight(1f)
            )
            DrivingMetric(
                label = "Steering Input",
                value = "Smooth",
                color = Cyan,
                modifier = Modifier.weight(1f)
            )
            DrivingMetric(
                label = "Speed Control",
                value = "Steady",
                color = Emerald,
                modifier = Modifier.weight(1f)
            )
        }
    }
}

/**
 * Preview showing all components together
 */
@Preview(showBackground = true, widthDp = 1200, heightDp = 800)
@Composable
fun AllMetricCardsPreview() {
    VigilanceAITheme {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(Gray950)
                .padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                text = "Metric Components Showcase",
                style = MaterialTheme.typography.headlineLarge,
                color = Color.White
            )

            // MetricItems
            Row {
                MetricItem("Alertness", "98%", Emerald, Modifier.weight(1f))
                MetricItem("Stress", "Low", Cyan, Modifier.weight(1f))
                MetricItem("Fatigue", "12%", Emerald, Modifier.weight(1f))
            }

            // QuickActionCards
            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                QuickActionCard(
                    Icons.Default.Psychology,
                    Cyan,
                    "AI CO-PILOT",
                    "Ready to assist",
                    Modifier.weight(1f)
                )
                QuickActionCard(
                    Icons.Default.Timeline,
                    Emerald,
                    "TRIP TIME",
                    "1h 23m",
                    Modifier.weight(1f)
                )
            }

            // DetailedMetricCards
            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                DetailedMetricCard(
                    "EYE ACTIVITY",
                    "4.2%",
                    "Safe range",
                    Cyan,
                    Modifier.weight(1f)
                )
                DetailedMetricCard(
                    "HEART RATE",
                    "72 BPM",
                    "Normal rhythm",
                    Blue,
                    Modifier.weight(1f)
                )
            }

            // DrivingMetrics
            Row {
                DrivingMetric("Lane Keeping", "Stable", Emerald, Modifier.weight(1f))
                DrivingMetric("Steering", "Smooth", Cyan, Modifier.weight(1f))
                DrivingMetric("Speed", "Steady", Emerald, Modifier.weight(1f))
            }
        }
    }
}