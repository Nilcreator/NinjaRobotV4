# NinjaRobotV4

This project is a reconstruction of the NinjaRobotV3, aiming to improve its structure, maintainability, and reusability. 

## Current Status

The **Web Server & Remote Access** module has been successfully implemented. The robot now hosts a FastAPI-based web interface that allows for complete control and interaction from any device.

Key features include:
-   **Remote Access**: Integrated `ngrok` support with automatic tunnel creation and QR code display on the robot's screen for easy connection.
-   **Interactive Web Interface**: A responsive UI for controlling servo movements, facial expressions, and sounds.
-   **Voice & Multilingual Chat**: The web interface supports **Voice Input** (via Web Speech API) and text chat in **English**, **Japanese**, **Traditional Chinese**, and **Simplified Chinese**.
-   **Real-time Telemetry**: WebSocket-based real-time distance sensor readings.
-   **Safety Integration**: Obstacle avoidance is active during web-triggered movements.

## Previous Status

- The **AI Agent** (`ninja_agent.py`) has been successfully implemented and integrated into `ninja_core`. The robot now features a fully interactive chat interface powered by **Google Gemini**, capable of nuanced semantic understanding, multilingual communication, and real-time web search.
- The `movement-tool` in the `ninja_core` library is fully functional and robust. All features, including recording, modifying, and clearing movements, have been implemented. The servo calibration function has been seamlessly integrated.
- The **Motion System** (`movement_controller.py`) was successfully ported and refactored into the `ninja_core` application, integrated with the HAL and central configuration.
- The `perception.py`, `robot_sound.py`, and `facial_expressions.py` modules have been successfully ported and refactored. They are now integrated with the Hardware Abstraction Layer and have been tested successfully.
- The `ninja_core` application now has a Hardware Abstraction Layer (`hal.py`). This module centralizes the initialization and control of all hardware components, reading settings from the `config.json` file.
- All foundational hardware libraries (`pi0servo`, `pi0disp`, `pi0vl53l0x`, `pi0buzzer`) are now complete, along with the shared `ninja_utils` library.
