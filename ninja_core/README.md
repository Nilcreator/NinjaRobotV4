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
### Testing `facial_expressions.py`

This test will cycle through all available facial expressions on the robot's display.

#### **1. Prerequisites**

*   **Hardware:** Ensure your ST7789V LCD display is connected to the Raspberry Pi according to the pinout in `InstallationGuide.md`.
*   **Configuration:** Your `config.json` file must have the correct pin configuration for the display in the `display` section. The default values are correct for the standard wiring, but you can verify them.

#### **2. Run the Test Script**

A dedicated test script, `test_facial_expressions.py`, is located in the project's root directory. Execute the following command from the `NinjaRobotV4` root directory:

```bash
uv run python test_facial_expressions.py
```

#### **3. Expected Outcome**

You should see the following on your Raspberry Pi:

1.  The terminal will print status messages as it initializes the hardware.
2.  The LCD display will light up.
3.  The display will cycle through all the facial expressions (`happy`, `sad`, `angry`, etc.), showing each one for about 3 seconds.
4.  After the cycle is complete, the `idle` face (blinking eyes) will be displayed indefinitely.
5.  You can press **Ctrl+C** at any time to stop the test and safely shut down the hardware.

### Testing `robot_sound.py`

This test will cycle through all available sounds and play them on the robot's buzzer.

#### **1. Prerequisites**

*   **Hardware:** Ensure your passive buzzer is connected to the Raspberry Pi according to the pinout in `InstallationGuide.md` (default is GPIO 26).
*   **Configuration:** Your `config.json` file must have the correct pin configuration for the buzzer in the `buzzer` section. If you haven't configured it, run `uv run pi0buzzer init 26` and then re-import the settings with `uv run ninja_core config import-all`.

#### **2. Run the Test Script**

Execute the following command from the `NinjaRobotV4` root directory:

```bash
uv run python test_robot_sound.py
```

#### **3. Expected Outcome**

You should see and hear the following:

1.  The terminal will print status messages as it initializes the hardware.
2.  You will hear a sequence of short melodies and sounds, with the terminal printing the name of each sound (`happy`, `sad`, `angry`, etc.) before it plays.
3.  The script will exit cleanly after playing all sounds.
