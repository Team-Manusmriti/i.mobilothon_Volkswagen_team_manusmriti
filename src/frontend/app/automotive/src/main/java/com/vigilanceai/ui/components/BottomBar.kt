package com.vigilanceai.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.vigilanceai.ui.theme.*

@Composable
fun BottomBar(
    isSystemActive: Boolean = true,
    vehicleStatus: String = "Connected",
    onSettingsClick: () -> Unit = {}
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(32.dp)
            .padding(horizontal = 48.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Left Side - Status Indicators
        Row(
            horizontalArrangement = Arrangement.spacedBy(24.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // System Status
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Status Dot
                Canvas(modifier = Modifier.size(8.dp)) {
                    drawCircle(
                        color = if (isSystemActive)
                            androidx.compose.ui.graphics.Color(0xFF10B981)
                        else
                            androidx.compose.ui.graphics.Color(0xFFEF4444)
                    )
                }

                Text(
                    text = if (isSystemActive) "System Active" else "System Inactive",
                    style = MaterialTheme.typography.bodyMedium,
                    color = if (isSystemActive) Emerald else Red,
                    fontWeight = FontWeight.Medium
                )
            }

            // Vehicle Status
            Text(
                text = "Vehicle: $vehicleStatus",
                style = MaterialTheme.typography.bodyMedium,
                color = Gray400
            )
        }

        // Right Side - Settings Icon
        IconButton(
            onClick = onSettingsClick,
            modifier = Modifier.size(32.dp)
        ) {
            Icon(
                imageVector = Icons.Default.Settings,
                contentDescription = "Settings",
                tint = Gray500,
                modifier = Modifier.size(16.dp)
            )
        }
    }
}

@Preview(showBackground = true, widthDp = 1920)
@Composable
fun BottomBarPreview() {
    VigilanceAITheme {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(100.dp)
        ) {
            BottomBar()
        }
    }
}

@Preview(showBackground = true, widthDp = 1920)
@Composable
fun BottomBarInactivePreview() {
    VigilanceAITheme {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(100.dp)
        ) {
            BottomBar(
                isSystemActive = false,
                vehicleStatus = "Disconnected"
            )
        }
    }
}