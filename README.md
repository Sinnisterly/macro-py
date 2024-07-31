# Macro Tool

## Overview

The **Macro Tool** is a Python application designed to facilitate the recording, playback, and management of macros. It features a graphical user interface (GUI) built with PySide6, providing a modern and dark-themed user experience. This tool is ideal for users who want to automate repetitive tasks through macros, enabling quick execution with customizable hotkeys.

## Features

- **Macro Recording**: Record keystrokes and mouse actions to create detailed macros that can replicate user actions precisely.
- **Macro Playback**: Play back recorded macros, with options for looping to repeat actions continuously.
- **Hotkey Assignment**: Currently not implimented. Assign hotkeys to macros for quick execution. The tool supports global hotkeys, allowing macros to be triggered even when the application is not in focus.
- **Macro Management**: Save, edit, delete, and organize macros efficiently. The tool provides a list view for easy management and retrieval of stored macros.
- **OTA Updates**: Built-in over-the-air (OTA) update functionality checks for and applies updates, ensuring the application remains up-to-date with the latest features and bug fixes.
- **Settings Dialog**: Customize the application settings, including selecting the target application for macros and configuring playback options like looping.

## Installation

To set up the Macro Tool, install the necessary dependencies using the following command:

```bash
pip install PySide6 requests appdirs pynput pygetwindow pywin32
```

### Dependency Overview

- **PySide6**: Provides the Qt bindings for the GUI, enabling the creation of a native-looking application.
- **requests**: A simple HTTP library for Python, used for checking and downloading updates.
- **appdirs**: Determines appropriate platform-specific directories for storing user data.
- **pynput**: Allows the control and monitoring of input devices, crucial for recording and playing back macros.
- **pygetwindow**: Provides functionality to interact with window properties, useful for targeting specific applications.
- **pywin32**: Extends the capabilities of Python to interact with Windows APIs, essential for simulating keystrokes and other system-level actions.

## Main Components

### About Dialog
A modal dialog that provides information about the application, including its name, description, and links to the developer's GitHub and Discord server for support and updates.

### Database Manager
This component manages the storage of macros and hotkeys using SQLite. It includes functionality for creating tables, saving macros and hotkeys, retrieving them, and deleting records. The database manager ensures that all macros and hotkeys are stored persistently and can be easily accessed and modified.

### Hotkey Assigner
The hotkey assigner allows users to set up custom hotkeys for triggering macros. It uses the `pynput` library to listen for specific key combinations globally. This component also manages the validation and parsing of hotkeys to ensure they are correctly recognized by the system.

### Key Translator
Converts virtual key codes to human-readable string representations and vice versa. It supports a wide range of keys, including special and OEM keys, and handles key combinations involving modifiers like Shift, Ctrl, and Alt.

### Macro Recorder and Player
The macro recorder captures the user's actions, including keystrokes and mouse movements, and saves them as macros. The macro player then executes these actions in sequence, optionally targeting a specific application window. It supports both normal and looped playback.

### OTA Updater
Handles checking for and applying updates to the application. It downloads update packages, extracts them, and replaces the old files with new ones, ensuring the application is always up-to-date.

## Usage

1. **Recording a Macro**:
   - Start the application and type a name in the macro name field.
   - Click 'Record' and perform the actions you want to automate.
   - Click 'Stop' to finish recording. The macro is saved automatically.

2. **Playing a Macro**:
   - Select a macro from the list.
   - Click 'Play' to execute the macro. Looping can be enabled if needed.

3. **Assigning Hotkeys**:
   - Open the settings dialog and select a macro.
   - Press the desired key combination to set it as a hotkey for the macro.

4. **Checking for Updates**:
   - Use the 'Check for Updates' feature to download and install the latest version.

### Selecting the Application to Inject Macros

5. **Selecting the Application to Inject Macros**:
   - Open the **Settings** dialog in the application.
   - In the "Select Target Application" section, choose the desired application from the dropdown list. This list is populated with the names of currently running applications with visible windows.
   - The selected application will be the target where the macros are injected during playback. If no application is selected, the macros will execute globally.
   - This setting can be adjusted at any time, allowing users to change the target application as needed.
