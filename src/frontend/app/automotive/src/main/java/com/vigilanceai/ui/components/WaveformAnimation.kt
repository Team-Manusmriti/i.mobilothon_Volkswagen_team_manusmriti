package com.vigilanceai.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import kotlin.math.*

@Composable
fun WaveformAnimation(
    isListening: Boolean = false,
    modifier: Modifier = Modifier
) {
    val infiniteTransition = rememberInfiniteTransition(label = "waveform")
    
    val waveOffset by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 2 * PI.toFloat(),
        animationSpec = infiniteRepeatable(
            animation = tween(3000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "wave_offset"
    )
    
    val amplitude by infiniteTransition.animateFloat(
        initialValue = if (isListening) 80f else 40f,
        targetValue = if (isListening) 120f else 60f,
        animationSpec = infiniteRepeatable(
            animation = tween(1500, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "amplitude"
    )

    Canvas(modifier = modifier.fillMaxSize()) {
        drawWaveform(
            waveOffset = waveOffset,
            amplitude = amplitude,
            isListening = isListening
        )
    }
}

private fun DrawScope.drawWaveform(
    waveOffset: Float,
    amplitude: Float,
    isListening: Boolean
) {
    val width = size.width
    val height = size.height
    val centerY = height / 2
    
    val azureColor = Color(0xFF007FFF)
    val lightAzure = Color(0xFF4DA6FF)
    val darkAzure = Color(0xFF0066CC)
    
    // Draw multiple wave layers
    val waveCount = if (isListening) 5 else 3
    
    for (i in 0 until waveCount) {
        val layerAmplitude = amplitude * (1f - i * 0.2f)
        val layerAlpha = (1f - i * 0.3f).coerceAtLeast(0.1f)
        val frequency = 0.01f + i * 0.005f
        val phaseShift = i * PI.toFloat() / 3
        
        val path = Path()
        var started = false
        
        for (x in 0..width.toInt() step 4) {
            val normalizedX = x / width
            val wave1 = sin(normalizedX * 4 * PI.toFloat() + waveOffset + phaseShift) * layerAmplitude
            val wave2 = sin(normalizedX * 6 * PI.toFloat() + waveOffset * 1.5f + phaseShift) * layerAmplitude * 0.5f
            val wave3 = sin(normalizedX * 8 * PI.toFloat() + waveOffset * 0.8f + phaseShift) * layerAmplitude * 0.3f
            
            val y = centerY + wave1 + wave2 + wave3
            
            if (!started) {
                path.moveTo(x.toFloat(), y)
                started = true
            } else {
                path.lineTo(x.toFloat(), y)
            }
        }
        
        val waveColor = when (i) {
            0 -> azureColor.copy(alpha = layerAlpha)
            1 -> lightAzure.copy(alpha = layerAlpha)
            else -> darkAzure.copy(alpha = layerAlpha)
        }
        
        drawPath(
            path = path,
            color = waveColor,
            style = androidx.compose.ui.graphics.drawscope.Stroke(
                width = (6f - i * 1f).coerceAtLeast(2f)
            )
        )
    }
    
    // Add particle effects when listening
    if (isListening) {
        repeat(20) { i ->
            val particleX = (width * (i / 20f)) + (sin(waveOffset + i) * 50f)
            val particleY = centerY + (cos(waveOffset * 1.5f + i) * amplitude * 0.5f)
            
            drawCircle(
                color = azureColor.copy(alpha = 0.6f),
                radius = 3f + sin(waveOffset + i) * 2f,
                center = androidx.compose.ui.geometry.Offset(particleX, particleY)
            )
        }
    }
}