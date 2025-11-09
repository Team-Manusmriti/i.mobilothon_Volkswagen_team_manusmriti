package com.vigilanceai.services

import androidx.car.app.CarContext
import androidx.car.app.Screen
import androidx.car.app.model.*
import androidx.lifecycle.DefaultLifecycleObserver
import androidx.lifecycle.LifecycleOwner

private lateinit var message: String

/**
 * VigilanceCarMainScreen
 * Main screen displayed on Android Auto
 *
 * Shows driver wellness information optimized for car displays:
 * - Wellness score
 * - Alertness level
 * - Fatigue status
 * - Quick actions
 */
class VigilanceCarMainScreen(carContext: CarContext) : Screen(carContext), DefaultLifecycleObserver {

    init {
        lifecycle.addObserver(this)
    }

    /**
     * Called when the screen needs to be rendered
     * Returns the Template to display on the car screen
     */
    override fun onGetTemplate(): Template {
        return PaneTemplate.Builder(createPane())
            .build()
    }

    /**
     * Creates the main content pane with driver wellness information
     */
    private fun createPane(): Pane {
        return Pane.Builder()
            .addRow(createWellnessRow())
            .addRow(createAlertnessRow())
            .addRow(createFatigueRow())
            .addAction(createTakeBreakAction())
            .build()
    }

    /**
     * Wellness Score Row
     */
    private fun createWellnessRow(): Row {
        return Row.Builder()
            .setTitle("Wellness Score")
            .addText("94 - Optimal Condition")
            .setImage(
                CarIcon.Builder(
                    androidx.car.app.model.CarIcon.ALERT
                ).build(),
                Row.IMAGE_TYPE_ICON
            )
            .build()
    }

    /**
     * Alertness Level Row
     */
    private fun createAlertnessRow(): Row {
        return Row.Builder()
            .setTitle("Alertness")
            .addText("98% - Highly Alert")
            .build()
    }

    /**
     * Fatigue Status Row
     */
    private fun createFatigueRow(): Row {
        return Row.Builder()
            .setTitle("Fatigue Level")
            .addText("12% - Low Fatigue")
            .build()
    }

    /**
     * Take Break Action Button
     */
    private fun createTakeBreakAction(): Action {
        return Action.Builder()
            .setTitle("Find Rest Stop")
            .setOnClickListener {
                // Handle finding nearby rest stop
                screenManager.push(VigilanceRestStopScreen(carContext))
            }
            .build()
    }

    override fun onCreate(owner: LifecycleOwner) {
        // Called when screen is created
    }

    override fun onStart(owner: LifecycleOwner) {
        // Called when screen starts
    }

    override fun onResume(owner: LifecycleOwner) {
        // Called when screen resumes
        // Refresh data here
    }

    override fun onPause(owner: LifecycleOwner) {
        // Called when screen pauses
    }

    override fun onStop(owner: LifecycleOwner) {
        // Called when screen stops
    }

    override fun onDestroy(owner: LifecycleOwner) {
        // Called when screen is destroyed
    }
}

/**
 * VigilanceRestStopScreen
 * Screen showing nearby rest stops
 */
/**
 * VigilanceRestStopScreen
 * Screen showing nearby rest stops
 */
class VigilanceRestStopScreen(carContext: CarContext) : Screen(carContext) {

    override fun onGetTemplate(): Template {
        return MessageTemplate.Builder("Looking for rest stops nearby...")
            .addAction(
                Action.Builder()
                    .setTitle("Navigate")
                    .setOnClickListener {
                        // Handle navigation
                        screenManager.pop()
                    }
                    .build()
            )
            .build()
    }
}
