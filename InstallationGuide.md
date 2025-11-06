# NinjaRobotV4 Installation and Testing Guide

This guide provides step-by-step instructions for setting up the necessary hardware and software, installing the core libraries, and testing their functionality on a Raspberry Pi Zero 2W.

## Phase 1: Prerequisites & Initial Setup

### 1.1 Hardware Requirements

- Raspberry Pi Zero 2W (or other compatible model)
- Passive Buzzer
- VL53L0X Time-of-Flight distance sensor
- ST7789V LCD Display
- Jumper wires
- An SD card with Raspberry Pi OS installed

### 1.2 Software Requirements

Before you begin, ensure the following software is installed on your Raspberry Pi:
- **Git:**
  ```bash
  sudo apt-get update && sudo apt-get install -y git
  ```
- **uv (Python Package Installer):**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **pigpio (GPIO Library):**
  ```bash
  sudo apt-get install -y pigpio
  ```

### 1.3 Hardware Connections

1.  **Buzzer Connection:**
    *   Connect the **positive (longer) leg** of the buzzer to **GPIO 26**.
    *   Connect the **negative (shorter) leg** to a **Ground (GND)** pin.

2.  **VL53L0X Sensor Connection (I2C):**
    *   Connect the **VCC** pin on the sensor to a **3.3V** pin.
    *   Connect the **GND** pin on the sensor to a **Ground (GND)** pin.
    *   Connect the **SCL** pin to the Pi's **SCL** pin (GPIO 3).
    *   Connect the **SDA** pin to the Pi's **SDA** pin (GPIO 2).

3.  **ST7789V Display Connection (SPI):**
    *   **VCC** -> 3.3V
    *   **GND** -> Ground (GND)
    *   **SCL** (or **CLK**) -> SPI0 SCLK (GPIO 11)
    *   **SDA** (or **MOSI**) -> SPI0 MOSI (GPIO 10)
    *   **RST** -> GPIO 19
    *   **DC** -> GPIO 18
    *   **BLK** (Backlight) -> GPIO 20

### 1.4 System Configuration

1.  **Enable I2C Interface:**
    *   Run `sudo raspi-config` in the terminal.
    *   Navigate to `3 Interface Options` -> `I5 I2C`.
    *   Select `<Yes>` to enable the interface and reboot if prompted.

2.  **Enable SPI Interface:**
    *   Run `sudo raspi-config` in the terminal.
    *   Navigate to `3 Interface Options` -> `I4 SPI`.
    *   Select `<Yes>` to enable the interface and reboot if prompted.

3.  **Start the pigpio Daemon:**
    This background service is required for the buzzer and sensor libraries to work. Run it once after each boot.
    ```bash
    sudo pigpiod
    ```

### 1.5 Get the Project Code

Clone the project repository from GitHub to your Raspberry Pi.

```bash
git clone <your-repository-url>
cd NinjaRobotV4
```

## Phase 2: Library Installation

Now, install all the core libraries (`ninja_utils`, `pi0buzzer`, `pi0vl53l0x`, and `pi0disp`) in editable mode. This method links the installation to your source code, so any changes you make are immediately reflected.

From the `NinjaRobotV4` root directory, run:

```bash
uv pip install -e ./ninja_utils -e ./pi0buzzer -e ./pi0vl53l0x -e ./pi0disp
```

## Phase 3: Component Testing

Test each library to confirm that the hardware and software are working correctly.

### 3.1 Testing `ninja_utils` (Keyboard Input)

This test verifies non-blocking keyboard input.

1.  Navigate to the `ninja_utils` directory:
    ```bash
    cd ninja_utils
    ```
2.  Run the sample script:
    ```bash
    uv run --active python samples/sample.py
    ```

**Expected Output:** You will see logger messages and a continuous stream of dots (`.`). Press any key to see it detected. Press `q` to quit the script.

3.  Return to the root directory:
    ```bash
    cd ..
    ```

### 3.2 Testing `pi0buzzer` (Buzzer Control)

This test verifies the buzzer functionality.

1.  Navigate to the `pi0buzzer` directory:
    ```bash
    cd pi0buzzer
    ```
2.  **Initialize Configuration:** Create the `buzzer.json` config file, telling the library you are using GPIO 26.
    ```bash
    uv run pi0buzzer init 26
    ```
3.  **Test Beep:** You should hear a short, simple beep.
    ```bash
    uv run pi0buzzer beep
    ```
4.  **Test Music:** You should hear a short melody.
    ```bash
    uv run pi0buzzer playmusic
    ```
5.  Return to the root directory:
    ```bash
    cd ..
    ```

### 3.3 Testing `pi0vl53l0x` (Distance Sensor)

This test verifies the distance sensor functionality.

1.  Navigate to the `pi0vl53l0x` directory:
    ```bash
    cd pi0vl53l0x
    ```
2.  **Get Live Readings:** Take 5 distance readings, one per second.
    ```bash
    uv run pi0vl53l0x get --count 5 --interval 1.0
    ```
    *Expected Output:* A list of distances in millimeters.

3.  **Measure Performance:** Check the maximum speed of the sensor. This runs 100 readings as fast as possible.
    ```bash
    uv run pi0vl53l0x performance --count 100
    ```
    *Expected Output:* A report showing total time, average time per reading, and the number of readings per second.

4.  **Calibrate Sensor:** Calculate and save the sensor's offset for better accuracy.
    *   Place a flat object at a known distance (e.g., exactly **100mm**) from the sensor.
    *   Run the command:
        ```bash
        uv run pi0vl53l0x calibrate --distance 100
        ```
    *   Follow the prompt and press Enter when ready. The calculated offset will be saved automatically for future use.

5.  Return to the root directory:
    ```bash
    cd ..
    ```

### 3.4 Testing `pi0disp` (Display Control)

This test verifies the display functionality.

1.  **Asset Preparation:**
    *   **Download Font:** The `ball_anime` demo requires the "Noto Sans JP" font.
        ```bash
        wget -O pi0disp/NotoSansJP-Regular.ttf https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP-Regular.ttf
        ```
    *   **Prepare Image:** You will need a sample JPEG image. For this example, we'll assume it's at `/home/pi/my_photo.jpg`.

2.  **Run Image Test:**
    *   This command displays your image and cycles through gamma corrections.
        ```bash
        uv run pi0disp image /home/pi/my_photo.jpg
        ```
    *   **Expected Output:** Your image appears on the display and the brightness/contrast changes every 3 seconds.

3.  **Run Animation Test:**
    *   This command runs a physics-based ball animation.
        ```bash
        uv run pi0disp ball_anime --num-balls 5
        ```
    *   **Expected Output:** Five colored balls bounce around the screen with an FPS counter in the corner. Press **Ctrl+C** to exit.

4.  Return to the root directory:
    ```bash
    cd ..
    ```

---

All tests are complete. Your core hardware libraries are now set up and verified.
