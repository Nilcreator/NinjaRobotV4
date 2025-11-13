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
│       ├── __main__.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── display_agent.py
│       │   ├── movement_agent.py
│       │   ├── perception_agent.py
│       │   └── sound_agent.py
│       ├── config.py
│       ├── hal.py
│       ├── ninja_agent.py
│       ├── tools.py
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

**2.1. Project Setup & Dependencies**
*   **Objective:** Create the `ninja_core` project structure and define all necessary dependencies.
*   **Execution Plan:**
    1.  Create the `ninja_core` directory with a `src/ninja_core` subdirectory.
    2.  Create a `pyproject.toml` file inside `ninja_core`.
    3.  Add the following dependencies identified from the V3 project:
        *   `fastapi`: For the web server.
        *   `uvicorn[standard]`: For running the web server.
        *   `jinja2`: For HTML templating.
        *   `google-generativeai`: For the Gemini AI agent.
        *   `python-dotenv`: For managing the API key.
        *   `websockets`: For real-time communication.
        *   `googlesearch-python`: For the agent's web search tool.
        *   `pyngrok`: For creating a public URL.
        *   `python-multipart`: For handling file uploads (voice commands).
        *   `qrcode[pil]`: For generating and displaying the QR code.
        *   `Pillow`: For image manipulation (facial expressions, QR code).
        *   `click`: For the CLI.
        *   Local path dependencies on `pi0servo`, `pi0disp`, `pi0buzzer`, `pi0vl53l0x`, and `ninja_utils`.

**2.2. Centralized Configuration (`config.py`)**
*   **Objective:** Manage all robot settings from a single, unified configuration file.
*   **Execution Plan:**
    1.  **`config.py`:**
        *   Implement a `NinjaConfig` class to load, manage, and save settings from a `config.json` file in the `ninja_core` root.
        *   The class should handle the creation of a default `config.json` on first run.
        *   It will store hardware pinouts, servo calibration data, and API keys.
    2.  **`__main__.py` (CLI):**
        *   Create a `config` command group.
        *   Implement a `config import-all` command that automatically finds and merges `servo.json` from `pi0servo` and `buzzer.json` from `pi0buzzer` into the main `config.json`. This provides a clear, one-step process for updating the central configuration after hardware calibration.

**2.3. Hardware Abstraction Layer (`hal.py`)**
*   **Objective:** Create a single, consistent interface for all hardware components.
*   **Execution Plan:**
    1.  **`hal.py`:**
        *   Implement a `HardwareAbstractionLayer` class.
        *   The `__init__` method will take the `NinjaConfig` object.
        *   It will initialize all hardware driver classes (`pi0servo.MultiServo`, `pi0disp.ST7789V`, `pi0buzzer.MusicBuzzer`, `pi0vl53l0x.VL53L0X`) using the settings from the config object.
        *   Expose all hardware instances (e.g., `self.servos`, `self.display`) as properties of the HAL.

**2.4. Core Application Logic**
*   **Objective:** Re-implement the robot's primary behaviors (faces, sounds, movements).
*   **Execution Plan:**
    1.  **`facial_expressions.py`:**
        *   **`AnimatedFaces` class:** Port from V3 (`V3Archive/pi0ninja_v3/src/pi0ninja_v3/facial_expressions.py`). Refactor the multiple `play_*` methods into a single `play(expression_name)` method to reduce code duplication. It will take the `display` driver from the HAL as an argument.
    2.  **`robot_sound.py`:**
        *   **`RobotSoundPlayer` class:** Port from V3 (`V3Archive/pi0ninja_v3/src/pi0ninja_v3/robot_sound.py`). It will take the `buzzer` driver from the HAL as an argument.
    3.  **`movement_recorder.py`:**
        *   **`MovementController` class:** Port the `ServoController` from V3 (`V3Archive/pi0ninja_v3/src/pi0ninja_v3/movement_recorder.py`) and rename it. It will take the `servos` driver from the HAL as an argument.

**2.5. AI Agent (`ninja_agent.py`)**
*   **Objective:** Implement the AI agent with both text and voice chat capabilities.
*   **Execution Plan:**
    1.  **`ninja_agent.py`:**
        *   **`NinjaAgent` class:** Port from V3 (`V3Archive/pi0ninja_v3/src/pi0ninja_v3/ninja_agent.py`).
        *   **`__init__`:** Modify to accept the `NinjaConfig` object to get the API key.
        *   **`_load_robot_capabilities`:** Update to load available movements, faces, and sounds from the `config.json` file instead of separate files.
        *   **`process_command` (Text):** Keep the existing logic for processing text commands.
        *   **`process_audio_command` (Voice):** Port the existing logic. It will receive a path to a temporary audio file (e.g., `.webm`), read the bytes, and send them to the Gemini API for transcription and processing.

**2.6. Web Server & Remote Access (`web_server.py`)**
*   **Objective:** Create the FastAPI web server, including remote access via ngrok and a QR code display.
*   **Execution Plan:**
    1.  **`web_server.py`:**
        *   **`lifespan` Manager (Startup Logic):**
            1.  Initialize the `NinjaConfig`, `HardwareAbstractionLayer`, and `NinjaAgent`.
            2.  Start `ngrok` to create a public URL. Retry a few times if it fails.
            3.  If `ngrok` succeeds, generate a QR code from the public URL.
            4.  Use the `pi0disp` driver (via the HAL) to display the QR code on the ST7789V screen.
            5.  If `ngrok` fails, display an error message on the screen.
        *   **`lifespan` Manager (Shutdown Logic):**
            1.  Gracefully shut down all hardware via the HAL.
            2.  Kill the `ngrok` process.
        *   **API Endpoints:**
            *   `/api/agent/chat` (POST): For text-based commands.
            *   `/api/agent/chat_voice` (POST): For voice commands (as file uploads). This endpoint will save the uploaded audio to a temporary file and pass the path to the `NinjaAgent`.
            *   `/` (GET): Serve the main HTML, CSS, and JavaScript for the web interface.
            *   `/ws/distance` (WebSocket): Stream distance sensor data to the client.
        *   **First Interaction Handling:** Implement the logic from V3 where the initial QR code is cleared from the display and replaced with the idle face upon the first user request to the server.
        *   **Reference:** The overall structure and logic should be based on `V3Archive/pi0ninja_v3/src/pi0ninja_v3/web_server.py`.

**2.7. Main Entry Point (`__main__.py`)**
*   **Objective:** Provide a simple way to start the application.
*   **Execution Plan:**
    1.  **`__main__.py`:**
        *   Create a main function that initializes and runs the `uvicorn` server for the FastAPI application defined in `web_server.py`.
        *   This will be the primary entry point, callable via `uv run ninja_core`.

**A Note on Testing:**

While this plan does not have a dedicated testing phase, it is highly recommended to write and run unit tests for each library and module as it is being developed. This will help to ensure the quality and correctness of the code.

### Phase 3: Advanced Multi-Agent Architecture

**Objective:** To refactor `ninja_core` into a multi-agent system where a central Orchestration Agent delegates tasks to specialized, function-specific agents, enabling more complex and coordinated robot behaviors.

**3.1. New `ninja_core` File Structure**

First, we will introduce a new `agents` directory and a `tools.py` file to better organize the code.

```
ninja_core/
└── src/ninja_core/
    ├── __init__.py
    ├── __main__.py
    ├── agents/
    │   ├── __init__.py
    │   ├── display_agent.py
    │   ├── movement_agent.py
    │   ├── perception_agent.py
    │   └── sound_agent.py
    ├── config.py
    ├── hal.py
    ├── ninja_agent.py  # This becomes the Orchestrator
    ├── tools.py        # Defines functions for the Orchestrator
    └── web_server.py
```

**3.2. Implementation Plan**

**Step 1: Implement the Specialized Agents**

These agents are simple Python classes that manage a specific hardware capability. They are initialized with a hardware controller from the Hardware Abstraction Layer (HAL).

*   **`agents/movement_agent.py`**
    *   **`MovementAgent` class:**
        *   `__init__(self, servo_controller)`: Takes the servo controller from the HAL.
        *   `execute_movement(self, movement_name: str)`: Executes a pre-defined movement sequence (e.g., "wave", "nod").
        *   `move_servo(self, servo_id: int, angle: int)`: Moves a single servo to a specific angle.

*   **`agents/display_agent.py`**
    *   **`DisplayAgent` class:**
        *   `__init__(self, display_controller)`: Takes the facial expression controller from the HAL.
        *   `show_face(self, expression: str)`: Displays a facial expression (e.g., "happy", "thinking").

*   **`agents/sound_agent.py`**
    *   **`SoundAgent` class:**
        *   `__init__(self, sound_controller)`: Takes the sound controller from the HAL.
        *   `play_sound(self, sound_name: str)`: Plays a sound (e.g., "greeting", "error").

*   **`agents/perception_agent.py`**
    *   **`PerceptionAgent` class:**
        *   `__init__(self, distance_sensor)`: Takes the distance sensor from the HAL.
        *   `get_distance(self) -> int`: Returns the current distance in millimeters.

**Step 2: Define the Orchestrator's Tools (`tools.py`)**

This file defines the exact functions the Gemini model can call. It acts as a bridge between the Orchestrator and the specialized agents. This is crucial for security and modularity.

*   **`tools.py`:**
    *   This file will contain a list of all functions available to the `NinjaAgent`.
    *   Each function will be clearly defined with type hints, which will be used to generate the schema for the Gemini API.
    *   **Example:**
        ```python
        # In tools.py
        from . import agents # Assume agents are initialized globally or passed in

        def execute_robot_movement(movement_name: str) -> str:
            """Executes a pre-defined robot movement sequence."""
            agents.movement_agent.execute_movement(movement_name)
            return f"Movement '{movement_name}' executed successfully."

        def show_robot_face(expression: str) -> str:
            """Displays a facial expression on the robot's screen."""
            agents.display_agent.show_face(expression)
            return f"Face '{expression}' is now displayed."

        # ... other tool functions ...
        ```

**Step 3: Upgrade the `NinjaAgent` to an Orchestrator**

The existing `NinjaAgent` will be promoted to the role of Orchestrator.

*   **`ninja_agent.py`:**
    *   **`__init__`:** Modify to accept the `Tool` schema generated from the functions in `tools.py`.
    *   **System Prompt:** The prompt will be updated to instruct the agent to act as an orchestrator.
        > "You are Ninja, a robot. To fulfill user requests, you must use the available tools. You can call multiple tools in parallel to perform complex actions, like moving and showing a facial expression at the same time. Plan your steps and then call the necessary functions."
    *   **`process_command` Method:** This method will be rewritten to handle the full tool-calling workflow:
        1.  Send the user's prompt to the Gemini model.
        2.  Check if the model's response includes a `function_call`.
        3.  If it does, look up the corresponding function in `tools.py` and execute it with the arguments provided by the model.
        4.  Send the result of the function execution back to the model.
        5.  Receive the final, natural-language response from the model to be relayed to the user.
