package com.vigilanceai.service

import android.app.Service
import android.content.Intent
import android.os.Binder
import android.os.Bundle
import android.os.IBinder
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.text.SimpleDateFormat
import java.util.*

// This file previously contained a lightweight stub of VigilanceAIService
// To avoid duplicate class declarations with the full-featured implementation
// in 'com.vigilanceai.services.VigilanceAIService', this placeholder has
// been converted into a no-op stub class with a different name. If you
// intentionally need a local stub, rename and implement it accordingly.

class VigilanceAIServiceStub : Service() {
    private val binder = object : Binder() {}

    override fun onBind(intent: Intent): IBinder? = binder

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // No-op stub
        return START_NOT_STICKY
    }
}