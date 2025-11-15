# Ninja Core

This package contains the main application logic for the NinjaRobotV4. It integrates all the individual hardware libraries (`pi0servo`, `pi0buzzer`, etc.) into a cohesive system managed by a central configuration and a Hardware Abstraction Layer (HAL).

## Testing the Core Components

These instructions will guide you through testing the initial components of the `ninja_core` library: the configuration manager and the Hardware Abstraction Layer (HAL).

This guide assumes you are in the root directory of the `NinjaRobotV4` project and have already installed all dependencies as per the main project guide.

### Prerequisites

1.  **pigpio Daemon:** Before running any test, ensure the `pigpio` service is running on your Raspberry Pi.
    ```bash
    sudo pigpiod
    ```
2.  **Hardware Configurations:** Make sure you have run the initial setup for the hardware you want to test, as this creates their required configuration files (e.g., `pi0servo/servo.json`). For example, to calibrate a servo on GPIO 17:
    ```bash
    uv run pi0servo calib 17
    ```

### Step 1: Create the Master Configuration

The `ninja_core` application uses a single `config.json` file to manage all hardware. Use the following command to automatically generate this file and import the settings from your individual hardware configurations.

```bash
uv run ninja_core config import-all
```

After running this, you will find a `config.json` file in the project's root directory.

### Step 2: Run the HAL Test Script

A dedicated test script, `test_hal.py`, is located in the project's root directory. This script will initialize the HAL, test the configured hardware (servos and buzzer), and then safely shut everything down.

Execute the script with `uv`:
```bash
uv run python test_hal.py
```

### Expected Outcome

If the test is successful, you will observe the following:

*   **In your terminal:** A series of log messages will appear, confirming that the configuration was loaded, the HAL was initialized, hardware tests were run, and the system was shut down cleanly.
*   **On your robot:**
    *   Any configured servos will move to their center (0-degree) position.
    *   The buzzer will play a short, audible beep.

This confirms that the `ninja_core` library is successfully communicating with and controlling the hardware through the Hardware Abstraction Layer.
