# NinjaRobotV4 Reconstruction Guide

## 1. Introduction

The NinjaRobotV3 is a small, friendly robot powered by a Raspberry Pi. This project is designed to be a fun and engaging way to learn the basics of how hardware (like motors and sensors) and software (the code) work together. The robot can move, see, show emotions, and make sounds. It has an advanced AI "brain" (powered by Google's Gemini) that lets you control it using text or voice commands in a web browser.

This document outlines the plan for reconstructing the NinjaRobot project into a new version, NinjaRobotV4. The goal of this reconstruction is to improve the project's structure, maintainability, and reusability, while retaining all of its current functionalities.

## 2. NinjaRobotV4 Refinements

The NinjaRobotV4 project will incorporate several key refinements compared to the existing NinjaRobotV3:

*   **Consistent Library Naming:** The libraries will be renamed for consistency:
    *   `vl53l0x_pigpio` -> `pi0vl53l0x`
    *   `piservo0` -> `pi0servo`
    *   `pi0ninja_v3` -> `ninja_core`
*   **Shared Utility Library:** A new `ninja_utils` library will be created to consolidate common code, such as the logger and keyboard utilities, and avoid duplication.
*   **Centralized Configuration:** A single `config.json` file will be used to manage the configuration for the entire project, instead of having separate configuration files for each library.
*   **Hardware Abstraction Layer (HAL):** A HAL will be created in the `ninja_core` project to provide a unified interface for all hardware components. This will make the code more modular and easier to maintain.
*   **Code Refactoring:** The code will be refactored to remove redundancies, simplify complex parts, and improve the overall structure.

## 3. Final File Structure of NinjaRobotV4

```
/
├── assets/
│   ├── images/
│   ├── sounds/
│   └── videos/
├── ninja_core/
│   └── src/ninja_core/
│       ├── __init__.py
│       ├── config.py
│       ├── facial_expressions.py
│       ├── hal.py
│       ├── movement_recorder.py
│       ├── ninja_agent.py
│       ├── robot_sound.py
│       └── web_server.py
├── pi0servo/
│   └── src/pi0servo/
│       ├── __init__.py
│       ├── __main__.py
│       ├── command/
│       │   ├── cmd_calib.py
│       │   └── cmd_servo.py
│       └── core/
│           ├── calibrable_servo.py
│           ├── multi_servo.py
│           └── piservo.py
├── pi0disp/
│   └── src/pi0disp/
│       ├── __init__.py
│       ├── __main__.py
│       ├── commands/
│       │   ├── ball_anime.py
│       │   ├── image.py
│       │   └── off.py
│       ├── disp/
│       │   └── st7789v.py
│       ├── fonts/
│       └── utils/
│           ├── image_processor.py
│           ├── performance_core.py
│           └── sprite.py
├── pi0buzzer/
│   └── src/pi0buzzer/
│       ├── __init__.py
│       ├── __main__.py
│       └── driver.py
├── pi0vl53l0x/
│   └── src/pi0vl53l0x/
│       ├── __init__.py
│       ├── __main__.py
│       ├── config_manager.py
│       ├── constants.py
│       └── driver.py
└── ninja_utils/
    └── src/ninja_utils/
        ├── __init__.py
        ├── keyboard.py
        └── my_logger.py
```

## 4. Reconstruction Plan

### Phase 1: Foundational Hardware Libraries & Shared Utilities

**1.1. `ninja_utils` - Shared Utilities**
*   **Objective:** Create a shared utility library to consolidate common code and avoid duplication.
*   **Execution Plan:**
    1.  **`pyproject.toml`:** Define project metadata.
    2.  **`my_logger.py`:**
        *   **Description:** A centralized logging module for consistent logging across the project.
        *   **Reference:** `V3Archive/pi0buzzer/src/pi0buzzer/my_logger.py`
    3.  **`keyboard.py`:**
        *   **`NonBlockingKeyboard` class:**
            *   **Description:** A utility for non-blocking keyboard input, essential for interactive CLI tools.
            *   **Reference:** `V3Archive/pi0ninja_v3/src/pi0ninja_v3/movement_recorder.py` -> `NonBlockingKeyboard` class

**1.2. `pi0buzzer` - Buzzer Control**
*   **Dependencies:** `pigpio`, `click`, `ninja_utils`
*   **Execution Plan:**
    1.  **`pyproject.toml`:** Define project metadata and dependencies.
    2.  **`driver.py`:**
        *   **`Buzzer` class:**
            *   **Description:** A simple driver for controlling a passive buzzer.
            *   **Reference:** `V3Archive/pi0buzzer/src/pi0buzzer/driver.py` -> `Buzzer` class
            *   `__init__(self, pi, pin)`: Initializes the buzzer on a specific GPIO pin.
            *   `play_sound(self, frequency, duration)`: Plays a sound with a given frequency and duration.
            *   `off(self)`: Stops the sound.
        *   **`MusicBuzzer` class:**
            *   **Description:** Extends `Buzzer` with the ability to play pre-defined songs.
            *   **Reference:** `V3Archive/pi0buzzer/src/pi0buzzer/driver.py` -> `MusicBuzzer` class
            *   `__init__`: Initializes the `MusicBuzzer`.
            *   `play_song(self, song)`: Plays a song defined as a list of notes and durations.
    3.  **`__main__.py`:**
        *   **CLI:**
            *   **Reference:** `V3Archive/pi0buzzer/src/pi0buzzer/__main__.py`
            *   `init`: Initializes the buzzer and creates a `buzzer.json` config file.
            *   `beep`: Plays a simple beep.
            *   `playmusic`: Plays a pre-defined song.

**1.3. `pi0vl53l0x` - Distance Sensor**
*   **Dependencies:** `click`, `numpy`, `pigpio`, `ninja_utils`
*   **Execution Plan:**
    1.  **`pyproject.toml`:** Define project metadata and dependencies.
    2.  **`constants.py`:**
        *   **Description:** Contains all the sensor's register addresses and constants.
        *   **Reference:** `V3Archive/vl53l0x_pigpio/src/vl53l0x_pigpio/constants.py`
    3.  **`driver.py`:**
        *   **`VL53L0X` class:**
            *   **Description:** The driver for the VL53L0X distance sensor.
            *   **Reference:** `V3Archive/vl53l0x_pigpio/src/vl53l0x_pigpio/driver.py` -> `VL53L0X` class
            *   `__init__`: Initializes the sensor.
            *   `initialize`: Performs the sensor initialization sequence.
            *   `get_range`: Performs a single distance measurement.
            *   `set_offset`: Sets a calibration offset.
            *   `calibrate`: Calculates the required offset.
            *   I2C helper methods: `read_byte`, `write_byte`, etc.
    4.  **`config_manager.py`:**
        *   **Description:** Manages the sensor's configuration file.
        *   **Reference:** `V3Archive/vl53l0x_pigpio/src/vl53l0x_pigpio/config_manager.py`
        *   `load_config`: Loads the configuration from a JSON file.
        *   `save_config`: Saves the configuration to a JSON file.
    5.  **`__main__.py`:**
        *   **CLI:**
            *   **Reference:** `V3Archive/vl53l0x_pigpio/src/vl53l0x_pigpio/__main__.py`
            *   `get`: Takes distance readings.
            *   `performance`: Measures the sensor's performance.
            *   `calibrate`: Starts the interactive calibration tool.

**1.4. `pi0disp` - Display Driver**
*   **Dependencies:** `click`, `numpy`, `pigpio`, `pillow`, `ninja_utils`
*   **Execution Plan:**
    1.  **`pyproject.toml`:** Define project metadata and dependencies.
    2.  **`performance_core.py`:**
        *   **Description:** Contains optimization classes for high-performance display rendering.
        *   **Reference:** `V3Archive/pi0disp/src/pi0disp/utils/performance_core.py`
        *   `MemoryPool`: Manages a pool of reusable memory buffers.
        *   `LookupTableCache`: Caches lookup tables for color conversion and gamma correction.
        *   `RegionOptimizer`: Merges overlapping or nearby rectangular regions.
        *   `PerformanceMonitor`: Tracks performance metrics like FPS.
        *   `AdaptiveChunking`: Dynamically adjusts data transfer chunk sizes.
        *   `ColorConverter`: Provides fast color space conversion utilities.
    3.  **`disp/st7789v.py`:**
        *   **`ST7789V` class:**
            *   **Description:** The driver for the ST7789V display.
            *   **Reference:** `V3Archive/pi0disp/src/pi0disp/disp/st7789v.py` -> `ST7789V` class
            *   `__init__`: Initializes the display.
            *   `display`: Displays a full PIL Image.
            *   `display_region`: Displays a portion of an image for partial updates.
    4.  **`utils/image_processor.py`:**
        *   **`ImageProcessor` class:**
            *   **Description:** A utility class for image processing tasks.
            *   **Reference:** `V3Archive/pi0disp/src/pi0disp/utils/utils.py` -> `ImageProcessor` class
            *   `resize_with_aspect_ratio`: Resizes an image while maintaining its aspect ratio.
            *   `apply_gamma`: Applies gamma correction to an image.
    5.  **`__main__.py`:**
        *   **CLI:**
            *   **Reference:** `V3Archive/pi0disp/src/pi0disp/__main__.py`
            *   `ball_anime`: Runs a bouncing ball animation.
            *   `image`: Displays an image.
            *   Other test commands.

**1.5. `pi0servo` - Servo Control**
*   **Dependencies:** `pigpio`, `click`, `blessed`, `ninja_utils`
*   **Execution Plan:**
    1.  **`pyproject.toml`:** Define project metadata and dependencies.
    2.  **Core Classes:**
        *   **`PiServo` class:**
            *   **Description:** A base class for controlling a single servo.
            *   **Reference:** `V3Archive/piservo0/piservo0/core/piservo.py` -> `PiServo` class
        *   **`CalibrableServo` class:**
            *   **Description:** Extends `PiServo` with calibration functionality.
            *   **Reference:** `V3Archive/piservo0/piservo0/core/calibrable_servo.py` -> `CalibrableServo` class
        *   **`MultiServo` class:**
            *   **Description:** A class to control multiple servos.
            *   **Reference:** `V3Archive/piservo0/piservo0/core/multi_servo.py` -> `MultiServo` class
            *   `move_all_angles`: Moves all servos to their respective target angles.
            *   `off_all`: Turns off all servos.
            *   `get_all_angles`: Returns the current angles of all servos.
            *   `move_all_angles_sync`: Moves all servos to their target angles synchronously.
    3.  **Asynchronous Control:**
        *   **`ThreadWorker` class:**
            *   **Description:** A thread worker that processes commands from a queue.
            *   **Reference:** `V3Archive/piservo0/piservo0/helper/thread_worker.py` -> `ThreadWorker` class
        *   **`ThreadMultiServo` class:**
            *   **Description:** A thread-safe wrapper around `MultiServo` for asynchronous control.
            *   **Reference:** `V3Archive/piservo0/piservo0/helper/thread_multi_servo.py` -> `ThreadMultiServo` class
    4.  **CLI:**
        *   `calib`: Starts the interactive calibration tool. **Reference:** `V3Archive/piservo0/piservo0/command/cmd_calib.py`
        *   `servo`: Moves a single servo. **Reference:** `V3Archive/piservo0/piservo0/command/cmd_servo.py`

### Phase 2: Main Application (`ninja_core`)

**2.1. Configuration Management**
*   **Objective:** Create a centralized configuration management system.
*   **Execution Plan:**
    1.  **`config.py`:**
        *   **Description:** A module to manage the entire robot's configuration.
        *   Implement a `Config` class that loads and saves configuration from a single `config.json` file. This file will contain settings for all hardware components (servo pins, calibration data, etc.).
        *   **First Run Logic:** If `config.json` does not exist, the module will create it with default values.
    2.  **`__main__.py` (CLI):**
        *   **Description:** A command-line interface for managing the `ninja_core` application.
        *   **`config` command group:**
            *   **`--import-servo` option:**
                *   **Action:** Explicitly imports calibration data from `pi0servo/servo.json` and merges it into the main `ninja_core/config.json`.
                *   **Purpose:** Provides a safe, user-controlled way to update the central configuration after running the standalone servo calibration, preventing accidental overwrites and maintaining a single source of truth for the running application.

**2.2. Hardware Abstraction Layer (HAL)**
*   **Dependencies:** `pi0servo`, `pi0disp`, `pi0buzzer`, `pi0vl53l0x`
*   **Execution Plan:**
    1.  **`hal.py`:**
        *   **Description:** A module that provides a unified interface for all hardware components.
        *   Implement wrapper classes that take the `Config` object and initialize the underlying drivers.

**2.3. Core Application Logic**
*   **Dependencies:** `Pillow`, `ninja_utils`
*   **Execution Plan:**
    1.  **`facial_expressions.py`:**
        *   **`AnimatedFaces` class:**
            *   **Description:** Generates and displays animated facial expressions.
            *   **Reference:** `V3Archive/pi0ninja_v3/src/pi0ninja_v3/facial_expressions.py` -> `AnimatedFaces` class
            *   `play(expression)`: Plays the specified facial expression. Refactor to remove code duplication from the original `play_*` methods.
    2.  **`robot_sound.py`:**
        *   **`RobotSoundPlayer` class:**
            *   **Description:** Plays sounds corresponding to robot emotions.
            *   **Reference:** `V3Archive/pi0ninja_v3/src/pi0ninja_v3/robot_sound.py` -> `RobotSoundPlayer` class
            *   `play(emotion)`: Plays the sound for the given emotion using the `pi0buzzer.MusicBuzzer` from the HAL.
    3.  **`movement_recorder.py`:**
        *   **`MovementRecorder` class:**
            *   **Description:** Records, plays back, and edits servo movement sequences.
            *   **Reference:** `V3Archive/pi0ninja_v3/src/pi0ninja_v3/movement_recorder.py`
            *   `record_new_movement`: Records a new movement sequence.
            *   `execute_movement`: Plays back a saved movement sequence.

**2.4. AI Agent and Web Server**
*   **Dependencies:** `fastapi`, `uvicorn`, `jinja2`, `google-generativeai`, `python-dotenv`, `websockets`, `googlesearch-python`, `pyngrok`, `python-multipart`, `qrcode`
*   **Execution Plan:**
    1.  **`pyproject.toml`:** Define project metadata and all dependencies.
    2.  **`ninja_agent.py`:**
        *   **`NinjaAgent` class:**
            *   **Description:** The AI agent for the NinjaRobot.
            *   **Reference:** `V3Archive/pi0ninja_v3/src/pi0ninja_v3/ninja_agent.py` -> `NinjaAgent` class
            *   `process_command`: Processes a text-based user command.
            *   `process_audio_command`: Processes a voice command.
    3.  **`web_server.py`:**
        *   **FastAPI application:**
            *   **Description:** The main web server for the NinjaRobot.
            *   **Reference:** `V3Archive/pi0ninja_v3/src/pi0ninja_v3/web_server.py`
            *   `lifespan`: Manages the application's startup and shutdown events.
            *   API endpoints: Provide an interface for controlling the robot.
            *   Refactor the business logic out of the endpoints and into the core application logic modules.

**A Note on Testing:**

While this plan does not have a dedicated testing phase, it is highly recommended to write and run unit tests for each library and module as it is being developed. This will help to ensure the quality and correctness of the code.
