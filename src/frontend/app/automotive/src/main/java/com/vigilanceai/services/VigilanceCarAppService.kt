package com.vigilanceai.services

import android.content.Intent
import androidx.car.app.CarAppService
import androidx.car.app.Screen
import androidx.car.app.Session
import androidx.car.app.validation.HostValidator

/**
 * VigilanceCarAppService
 * Android Auto Car App Service for VigilanceAI
 *
 * This service enables VigilanceAI to run on Android Auto
 * and display driver wellness information on the car's display
 *
 * Requirements:
 * - androidx.car.app:app:1.3.0 dependency
 * - Declared in AndroidManifest.xml
 */
class VigilanceCarAppService : CarAppService() {

    /**
     * Creates a new session for the car app
     * Called when Android Auto connects to your app
     */
    override fun createHostValidator(): HostValidator {
        // Allow all hosts for development
        // In production, use HostValidator.Builder(context).addAllowedHost(...).build()
        return HostValidator.ALLOW_ALL_HOSTS_VALIDATOR
    }

    /**
     * Called when a new session is created
     * Returns the session that manages the car app screens
     */
    override fun onCreateSession(): Session {
        return VigilanceCarAppSession()
    }
}

/**
 * VigilanceCarAppSession
 * Manages the Android Auto session and screen flow
 */
class VigilanceCarAppSession : Session() {

    /**
     * Creates the initial screen shown when app launches in Android Auto
     */
    override fun onCreateScreen(intent: Intent): Screen {
        return VigilanceCarMainScreen(carContext)
    }
}