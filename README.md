# NinjaRobotV4

This project is a reconstruction of the NinjaRobotV3, aiming to improve its structure, maintainability, and reusability. 

## Current Status

All foundational hardware libraries (`pi0servo`, `pi0disp`, `pi0vl53l0x`, `pi0buzzer`) are now complete, along with the shared `ninja_utils` library. This marks the successful completion of Phase 1 of the reconstruction plan. The project is now ready to proceed to Phase 2: building the main `ninja_core` application.

## Previous Status

- The `pi0disp` library for the ST7789V display was created, tested, and documented.
- The `pi0vl53l0x` library for the VL53L0X distance sensor was created.
- The `pi0buzzer` library was created.
- The `ninja_utils` library was created, providing shared utilities for logging and non-blocking keyboard input.
