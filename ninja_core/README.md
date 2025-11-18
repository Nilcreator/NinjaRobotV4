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

This is an interactive, command-line tool for developers to **create, edit, and test** motion sequences. You can launch it by running `uv run ninja_core movement-tool` from the project root.

#### Servo Movement Command Rules

When recording or editing movements, you use a special command syntax:

| Rule                | Description                                                                                                                            | Example                |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **Basic Format**    | A GPIO pin number and an angle, separated by a colon.                                                                                  | `17:45`                |
| **Angle Keywords**  | Use keywords for common angles: `C` for Center (0°), `M` for Minimum (-90°), and `X` for Maximum (90°).                                  | `17:C`                 |
| **Chaining**        | Multiple servo movements in the same step are chained with a `/`.                                                                      | `17:45/22:-30`         |
| **Speed Prefix**    | Set the speed for a step with a prefix: `S_` (Slow), `M_` (Medium), or `F_` (Fast). Medium is the default.                               | `S_17:90/22:90`        |
| **Auto-Completion** | **(Crucial Rule)** If a servo isn't specified in a command, it automatically holds its position from the *previous* step, ensuring smooth, continuous motion. | If step 1 is `17:45` and step 2 is `22:30`, servo 17 remains at 45° during step 2. |

---

## Testing the Core Components

This guide assumes you are in the root directory of the `NinjaRobotV4` project and have already installed all dependencies.

### Prerequisites

1.  **pigpio Daemon:** Before running any test, ensure the `pigpio` service is running.
    ```bash
    sudo pigpiod
    ```
2.  **Hardware Configurations:** Make sure you have run the initial setup for the hardware you want to test, as this creates their required configuration files (e.g., `pi0servo/servo.json`). For example, to calibrate a servo on GPIO 17:
    ```bash
    uv run pi0servo calib 17
    ```

### Step 1: Create or Update the Master Configuration

The `ninja_core` application uses a single `config.json` file. Use the following command to automatically generate this file and import the settings from your individual hardware configurations.

```bash
uv run ninja_core config import-all
```

### Step 2: Test the Motion System

1.  **Launch the Movement Tool:**
    ```bash
    uv run ninja_core movement-tool
    ```
2.  **Record a Movement:**
    - Select option **1** to "Record new movement."
    - At the prompt, enter a command to move a servo (e.g., `17:45`).
    - The servo will move. Select option **1** to "Confirm & Next."
    - Enter another command to move it back to center (e.g., `17:C`).
    - Select option **3** to "Finish Recording."
    - Name the movement `test_wave` and press Enter.
3.  **Execute the Movement:**
    - From the main menu, select option **3** to "Execute a movement."
    - Choose the `test_wave` movement.
    - Enter `1` to loop it once.
    - **Expected Result:** The servo will smoothly move to 45 degrees and back to center.
4.  **Exit:** Select option **5** to exit the tool.

### Step 3: Test Other Core Components

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
