# Ninja Core

This package contains the main application logic for the NinjaRobotV4. It integrates all the individual hardware libraries (`pi0servo`, `pi0buzzer`, etc.) into a cohesive system managed by a central configuration and a Hardware Abstraction Layer (HAL).

## Key Components

- **`hal.py` (Hardware Abstraction Layer):** Initializes and provides a single access point for all hardware drivers.
- **`config.py` (Configuration Manager):** Manages all robot settings from a central `config.json` file.
- **`movement_controller.py` (Motion System):** Executes complex, multi-servo movement sequences.
- **`facial_expressions.py`, `robot_sound.py`, `perception.py`:** High-level controllers for expressions, sounds, and sensing.

## The Motion System (`movement_controller.py`)

The Motion System is responsible for all servo-based movements. It is composed of two main parts: the runtime `MovementController` class and the interactive `movement-tool` CLI.

### `MovementController` Class

This class is the runtime engine for executing pre-defined motion sequences.
- It is initialized with the HAL and `NinjaConfig` objects, removing the need for direct hardware or file system access.
- Its primary method, `execute_movement(movement_name)`, plays back a named sequence from the configuration.
- It uses smooth interpolation to ensure fluid motion rather than abrupt changes.

### `movement-tool` CLI

This is an interactive, command-line tool for developers to **calibrate, create, edit, and test** all servo-related functions. You can launch it by running `uv run ninja_core movement-tool` from the project root.

The tool presents a main menu with the following options:

- **1. Calibrate a Servo:** Launches the `pi0servo` calibration tool for a selected servo. This allows you to define the min, center, and max pulse widths. The new calibration is automatically imported into the application's main configuration when the tool is running.
- **2. Record new movement:** Starts the interactive recorder to create a new, named motion sequence step-by-step.
- **3. Modify existing movement:** Provides a menu to interactively edit, insert, or delete steps within a saved movement.
- **4. Execute a movement:** Plays back a saved movement, with options for looping.
- **5. Clear movement:** Deletes a saved movement from the configuration.
- **6. Exit:** Closes the tool and safely shuts down the hardware, saving all changes to `config.json`.

#### In-Depth Guide: Recording a New Movement

This feature allows you to define a sequence of positions for your servos, which are then saved as a single, named movement (e.g., "wave", "nod").

##### Command Input Rules

When recording, you define each step using a special command syntax:

| Rule                | Description                                                                                                                            | Example                |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **Basic Format**    | A GPIO pin number and an angle, separated by a colon. Angles range from -90 to 90.                                                     | `17:45`                |
| **Angle Keywords**  | Use keywords for common angles: `C` for Center (0°), `M` for Minimum (-90°), and `X` for Maximum (90°).                                  | `17:C`                 |
| **Chaining**        | Multiple servo movements in the same step are chained together with a `/`.                                                              | `17:45/22:-30`         |
| **Speed Prefix**    | Set the speed for a step with a prefix: `S_` (Slow), `M_` (Medium), or `F_` (Fast). Medium is the default.                               | `S_17:90/22:90`        |
| **Auto-Completion** | **(Crucial Rule)** If a servo isn't specified in a command, it automatically holds its position from the *previous* step. This is the key to creating smooth, continuous motions. | If step 1 is `17:45` and step 2 is `22:30`, servo 17 remains at 45° during step 2. |

---

## Testing the Core Components

This guide assumes you are in the root directory of the `NinjaRobotV4` project and have already installed all dependencies.

### Prerequisites

1.  **pigpio Daemon:** Before running any test, ensure the `pigpio` service is running.
    ```bash
    sudo pigpiod
    ```
2.  **Initial Configuration:** If you have not yet created the master `config.json`, run the import command at least once.
    ```bash
    uv run ninja_core config import-all
    ```

### Step 1: Calibrate and Test the Motion System

This workflow demonstrates the seamless integration of the calibration and movement tools.

1.  **Launch the Movement Tool:**
    ```bash
    uv run ninja_core movement-tool
    ```

2.  **Calibrate a Servo:**
    - Select option **1** to "Calibrate a Servo."
    - Choose the servo pin you wish to calibrate from the list.
    - The `pi0servo` calibration interface will launch. Follow the on-screen instructions (`h` for help) to set the Min, Center, and Max positions.
    - Press `q` to quit the calibration tool.
    - The `movement-tool` will automatically import the new settings and re-initialize the hardware.

3.  **Record a Movement:**
    - Select option **2** to "Record new movement."
    - Create a simple movement (e.g., `17:45`, confirm, then `17:C`, finish) and name it `test_wave`.

4.  **Execute the Movement:**
    - Select option **4** to "Execute a movement."
    - Choose the `test_wave` movement and loop it once.
    - **Expected Result:** The servo will smoothly move to its 45-degree position and back, respecting the calibration you just set.

5.  **Exit:** Select option **6** to exit. All your new calibration and movement data will be saved to `config.json`.

### Step 2: Test Other Core Components

You can test other hardware functionalities using the pre-made test scripts in the project root:

- **Test HAL (Servos and Buzzer):**
  ```bash
  uv run python test_hal.py
  ```
- **Test Display System:**
  ```bash
  uv run python test_facial_expressions.py
  ```
- **Test Sound System:**
  ```bash
  uv run python test_robot_sound.py
  ```
- **Test Perception System:**
  ```bash
  uv run python test_perception.py
  ```

This confirms that all `ninja_core` systems are successfully communicating with and controlling the hardware.
