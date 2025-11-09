plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("kotlin-kapt")
    alias(libs.plugins.compose.compiler)
    // The Compose Compiler plugin is enabled via buildFeatures, not here.
}

android {
    namespace = "com.vigilanceai"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.vigilanceai"
        minSdk = 29
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildFeatures {
        // This enables Compose for your project
        compose = true
    }

    composeOptions {
        // Sets the version of the Kotlin Compiler used for Compose
        kotlinCompilerExtensionVersion = "1.5.3"
    }

    packaging {
        // Add this if you encounter packaging errors related to duplicate META-INF files
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }

    kotlinOptions {
        jvmTarget = "1.8"
    }

    lint {
        abortOnError = false
        checkReleaseBuilds = false
    }
}

dependencies {
    // Compose
    implementation(libs.androidx.ui.v154)
    implementation(libs.androidx.material3.v112)
    implementation(libs.androidx.ui.tooling.preview.v154)
    implementation(libs.androidx.activity.compose.v181)

    // Navigation
    implementation(libs.androidx.navigation.compose.v275)

    // ViewModel
    implementation(libs.androidx.lifecycle.viewmodel.compose.v262)
    implementation(libs.androidx.lifecycle.runtime.ktx)

    // Icons
    implementation(libs.androidx.material.icons.extended)

    // Core
    implementation(libs.androidx.core.ktx.v1120)
    implementation(libs.androidx.junit.ktx)
    implementation(libs.androidx.app)
    implementation(libs.androidx.app.automotive)
    androidTestImplementation(libs.androidx.monitor)

//    // You will also need the Compose UI Tooling for previews in Android Studio
//    debugImplementation(libs.androidx.ui.tooling)
}
