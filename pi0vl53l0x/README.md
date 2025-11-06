# `pi0vl53l0x` Library

A Python library for the VL53L0X time-of-flight distance sensor, designed for Raspberry Pi using the `pigpio` library for high performance.

---

## Testing the `pi0vl53l0x` Library

This guide provides step-by-step instructions for testing the `pi0vl53l0x` library on a Raspberry Pi.

### Prerequisites

#### Hardware
- A VL53L0X Time-of-Flight sensor.

#### Software
- **git**: Must be installed.
- **uv**: Must be installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
- **pigpio**: The library and daemon must be installed (`sudo apt-get install pigpio`).

### Step 1: Hardware Setup

Connect the VL53L0X sensor to your Raspberry Pi's I2C pins.

1.  Connect the **VCC** pin on the sensor to a **3.3V** pin on the Pi.
2.  Connect the **GND** pin on the sensor to a **Ground (GND)** pin on the Pi.
3.  Connect the **SCL** pin on the sensor to the Pi's **SCL** pin (GPIO 3).
4.  Connect the **SDA** pin on the sensor to the Pi's **SDA** pin (GPIO 2).

### Step 2: Enable I2C and Start `pigpio`

1.  **Enable I2C:**
    If you haven't already, enable the I2C interface.
    ```bash
    sudo raspi-config
    ```
    Navigate to `3 Interface Options` -> `I5 I2C`, select `<Yes>`, and reboot if prompted.

2.  **Start the `pigpio` Daemon:**
    This background process is required for the library to work. Run it once after each reboot.
    ```bash
    sudo pigpiod
    ```

### Step 3: Get the Code and Install

1.  **Navigate to your project directory:**
    ```bash
    cd NinjaRobotV4
    ```
    *(If you have not cloned the repository yet, do so now)*

2.  **Install the library:**
    Navigate into the `pi0vl53l0x` directory and install it in editable mode.
    ```bash
    cd pi0vl53l0x
    uv pip install -e .
    ```

### Step 4: Test Using the Command-Line Interface (CLI)

The CLI is perfect for quick tests and calibration.

1.  **Get Distance Readings:**
    This command will take 10 distance readings, one per second.
    ```bash
    uv run pi0vl53l0x get --count 10 --interval 1.0
    ```
    *   **Expected Output:**
        ```
        1/10: 150 mm
        2/10: 149 mm
        3/10: ...
        ```

2.  **Measure Performance:**
    This command runs 100 measurements as fast as possible to see how many readings you can get per second.
    ```bash
    uv run pi0vl53l0x performance --count 100
    ```
    *   **Expected Output:** A report showing the total time, average time per measurement, and measurements per second.

3.  **Calibrate the Sensor:**
    The sensor might have a small, consistent error (an offset). This tool helps you calculate and save that offset.

    *   Place a flat object at a **known distance** from the sensor. For this example, we'll use **100mm**.
    *   Run the calibration command:
        ```bash
        uv run pi0vl53l0x calibrate --distance 100
        ```
    *   The tool will prompt you to press Enter when you are ready. It will then take several readings, calculate the average offset, and save it to a configuration file (`~/.config/pi0vl53l0x/config.json`). The library will automatically use this offset for all future readings.