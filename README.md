# NinjaRobotV4

This project is a reconstruction of the NinjaRobotV3, aiming to improve its structure, maintainability, and reusability. 

## Current Status

The `movement-tool` in the `ninja_core` library is now **fully functional and robust**. All features, including recording, modifying, and clearing movements, have been implemented. The servo calibration function from `pi0servo` has been seamlessly integrated, and critical bugs related to hardware state and configuration synchronization have been resolved. This completes the implementation and stabilization of the core motion system.

## Previous Status

- The **Motion System** (`movement_controller.py`) was successfully ported and refactored into the `ninja_core` application, integrated with the HAL and central configuration.
- The `perception.py`, `robot_sound.py`, and `facial_expressions.py` modules have been successfully ported and refactored. They are now integrated with the Hardware Abstraction Layer and have been tested successfully.
- The `ninja_core` application now has a Hardware Abstraction Layer (`hal.py`). This module centralizes the initialization and control of all hardware components, reading settings from the `config.json` file.
- All foundational hardware libraries (`pi0servo`, `pi0disp`, `pi0vl53l0x`, `pi0buzzer`) are now complete, along with the shared `ninja_utils` library.
