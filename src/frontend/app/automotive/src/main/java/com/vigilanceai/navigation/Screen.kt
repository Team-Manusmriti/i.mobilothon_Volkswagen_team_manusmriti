package com.vigilanceai.navigation

/**
 * Sealed class defining all navigation routes in the app
 * Using sealed class ensures type safety and prevents invalid routes
 */
sealed class Screen(val route: String) {
    /**
     * Dashboard Screen - Main screen showing driver wellness overview
     * Route: "dashboard"
     */
    object Dashboard : Screen("dashboard")

    /**
     * Wellness Monitor Screen - Detailed health metrics
     * Route: "wellness"
     */
    object Wellness : Screen("wellness")

    /**
     * Emergency Protocol Screen - Emergency response system
     * Route: "emergency"
     */
    object Emergency : Screen("emergency")

    /**
     * AI Co-Pilot Screen - Conversational assistant
     * Route: "copilot"
     */
    object CoPilot : Screen("copilot")
}

/**
 * List of all screens for easy iteration
 * Useful for creating navigation tabs
 */
val allScreens = listOf(
    Screen.Dashboard,
    Screen.Wellness,
    Screen.Emergency,
    Screen.CoPilot
)

/**
 * Screen display names for UI
 */
fun Screen.displayName(): String {
    return when (this) {
        is Screen.Dashboard -> "Dashboard"
        is Screen.Wellness -> "Wellness Monitor"
        is Screen.Emergency -> "Emergency Protocol"
        is Screen.CoPilot -> "AI Co-Pilot"
    }
}

