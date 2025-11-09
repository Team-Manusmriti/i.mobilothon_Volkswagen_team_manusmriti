package com.vigilanceai.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.vigilanceai.ui.theme.*
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun TopBar(
    time: String = getCurrentTime(),
    temperature: String = "23°C"
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(60.dp)
            .padding(horizontal = 48.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Left Side - Logo and Text
        Row(
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Logo Box
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .background(Cyan, RoundedCornerShape(8.dp)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Shield,
                    contentDescription = "VigilanceAI Logo",
                    tint = Color.White,
                    modifier = Modifier.size(24.dp)
                )
            }

            // Text Stack
            Column {
                Text(
                    text = "VIGILANCE AI",
                    style = MaterialTheme.typography.labelMedium,
                    color = Gray400,
                    letterSpacing = 0.5.sp
                )
                Text(
                    text = "Active Monitoring",
                    style = MaterialTheme.typography.titleLarge,
                    color = Color.White,
                    fontWeight = FontWeight.Medium
                )
            }
        }

        // Right Side - Time and Temperature
        Row(
            horizontalArrangement = Arrangement.spacedBy(32.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = time,
                style = MaterialTheme.typography.bodyLarge,
                color = Gray400
            )
            Text(
                text = temperature,
                style = MaterialTheme.typography.bodyLarge,
                color = Gray400
            )
        }
    }
}

// Helper function to get current time
@Composable
fun getCurrentTime(): String {
    val sdf = SimpleDateFormat("h:mm a", Locale.getDefault())
    return sdf.format(Date())
}

@Preview(showBackground = true, widthDp = 1920)
@Composable
fun TopBarPreview() {
    VigilanceAITheme {
        TopBar()
    }
}