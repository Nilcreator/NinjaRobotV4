# NinjaRobotV4

This project is a reconstruction of the NinjaRobotV3, aiming to improve its structure, maintainability, and reusability. 

## Current Status

The **AI Agent** (`ninja_agent.py`) has been successfully implemented and integrated into `ninja_core`. The robot now features a fully interactive chat interface powered by **Google Gemini**, capable of nuanced semantic understanding, multilingual communication, and real-time web search. 

Key enhancements include:
- **Obstacle Avoidance**: A safety reflex that stops movement and reacts when objects are too close (< 50mm).
- **Automatic Expressions**: The robot automatically displays emotions and "speaking" animations during interaction.
- **Chat Enhancements**: Includes welcome greetings and auto-idle behavior for a more natural user experience.
- **CLI Tools**: New `chat` and `config set-key` commands for easy operation.

## Previous Status

- The `movement-tool` in the `ninja_core` library is fully functional and robust. All features, including recording, modifying, and clearing movements, have been implemented. The servo calibration function has been seamlessly integrated.
- The **Motion System** (`movement_controller.py`) was successfully ported and refactored into the `ninja_core` application, integrated with the HAL and central configuration.
- The `perception.py`, `robot_sound.py`, and `facial_expressions.py` modules have been successfully ported and refactored. They are now integrated with the Hardware Abstraction Layer and have been tested successfully.
- The `ninja_core` application now has a Hardware Abstraction Layer (`hal.py`). This module centralizes the initialization and control of all hardware components, reading settings from the `config.json` file.
- All foundational hardware libraries (`pi0servo`, `pi0disp`, `pi0vl53l0x`, `pi0buzzer`) are now complete, along with the shared `ninja_utils` library.
