[app]
# Basic settings
title = ToDo App
package.name = todoapp
package.domain = org.deekshith
source.dir = .
source.include_exts = py,png,jpg,kv,dm
version = 0.1

# Application requirements
requirements = python3,kivy==2.2.0,kivymd==1.2.0,markdown,materialyoucolor,exceptiongroup,asyncgui,asynckivy  # Added all specified packages

# Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET  # Required permissions for storage and internet access

# Orientation settings
orientation = portrait  # Set to 'landscape' if needed

# Application icon
icon.filename = ./icon.png  # Path to your application icon (PNG format)

# Log level
log_level = 2  # 0: none, 1: error, 2: warning, 3: info, 4: debug

# Packaging settings
source.include_exts = py,png,jpg,kv,txt  # Add any other file types you might need
source.exclude_exts = spec  # Exclude unnecessary files

# Android specific settings
android.archs = arm64-v8a  # Specify architectures for APK
android.api = 33  # Set to the minimum SDK version you want to support
android.minapi = 21  # Minimum API level required for your app
android.target = 33  # Target API level (same as or greater than minapi)

# Versioning
version.code = 1  # Version code (used for updates)
version.name = 0.1  # Version name displayed in the app

# Build settings
debug = 1  # Set to 1 to enable debugging
