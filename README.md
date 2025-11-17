# NinjaRobotV4

This project is a reconstruction of the NinjaRobotV3, aiming to improve its structure, maintainability, and reusability. 

## Current Status

The `facial_expressions.py` module has been successfully ported and refactored. It is now integrated with the Hardware Abstraction Layer and has been tested successfully, allowing the robot to display a range of animated faces. This completes Sub-Phase 2.4.1 of the reconstruction plan.

## Previous Status

- The `ninja_core` application now has a Hardware Abstraction Layer (`hal.py`). This module centralizes the initialization and control of all hardware components, reading settings from the `config.json` file. This completes step 2.3 of the reconstruction plan.
- All foundational hardware libraries (`pi0servo`, `pi0disp`, `pi0vl53l0x`, `pi0buzzer`) are now complete, along with the shared `ninja_utils` library. This marks the successful completion of Phase 1 of the reconstruction plan.
- The `pi0disp` library for the ST7789V display was created, tested, and documented.
- The `pi0vl53l0x` library for the VL53L0X distance sensor was created.
- The `pi0buzzer` library was created.
- The `ninja_utils` library was created, providing shared utilities for logging and non-blocking keyboard input.
