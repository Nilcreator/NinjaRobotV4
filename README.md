# NinjaRobotV4

This project is a reconstruction of the NinjaRobotV3, aiming to improve its structure, maintainability, and reusability. 

## Current Status

The **Motion System** (`movement_controller.py`) has been successfully ported and refactored into the `ninja_core` application. This complex module, which handles multi-servo interpolated movements and interactive recording, is now integrated with the HAL and central configuration. A `movement-tool` has been added to the core CLI for developers. This completes Sub-Phase 2.4.4 of the reconstruction plan.

## Previous Status

- The `perception.py`, `robot_sound.py`, and `facial_expressions.py` modules have been successfully ported and refactored. They are now integrated with the Hardware Abstraction Layer and have been tested successfully.
- The `ninja_core` application now has a Hardware Abstraction Layer (`hal.py`). This module centralizes the initialization and control of all hardware components, reading settings from the `config.json` file. This completes step 2.3 of the reconstruction plan.
- All foundational hardware libraries (`pi0servo`, `pi0disp`, `pi0vl53l0x`, `pi0buzzer`) are now complete, along with the shared `ninja_utils` library. This marks the successful completion of Phase 1 of the reconstruction plan.
- The `pi0disp` library for the ST7789V display was created, tested, and documented.
- The `pi0vl53l0x` library for the VL53L0X distance sensor was created.
- The `pi0buzzer` library was created.
- The `ninja_utils` library was created, providing shared utilities for logging and non-blocking keyboard input.
