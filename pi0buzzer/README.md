# `pi0buzzer` Library

A library to control a passive buzzer on a Raspberry Pi.

---

## Testing the `pi0buzzer` Library

This guide provides step-by-step instructions for testing the `pi0buzzer` library on a Raspberry Pi.

### Prerequisites

#### Hardware
- A passive buzzer.

#### Software
- **git**: Must be installed.
- **uv**: Must be installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
- **pigpio**: The library and daemon must be installed (`sudo apt-get install pigpio`).

### Step 1: Hardware Setup

Connect the passive buzzer to your Raspberry Pi's GPIO pins. This guide assumes you are using **GPIO 26**.

1.  Connect the **positive (longer) leg** of the buzzer to **GPIO 26**.
2.  Connect the **negative (shorter) leg** of the buzzer to a **Ground (GND)** pin.

### Step 2: Start the `pigpio` Daemon

The `pigpio` library requires a background process (daemon) to be running. This must be done once after each reboot.

```bash
sudo pigpiod
```

### Step 3: Get the Code and Install

1.  **Clone the project repository:**
    ```bash
    git clone <your-repository-url>
    cd NinjaRobotV4
    ```

2.  **Install the library:**
    Navigate to the `pi0buzzer` directory and install the library in editable mode.
    ```bash
    cd pi0buzzer
    uv pip install -e .
    ```

### Step 4: Test Using the Command-Line Interface (CLI)

The CLI is the easiest way to test the basic functions.

1.  **Initialize the Buzzer Configuration:**
    This command creates a `buzzer.json` file that stores the GPIO pin you are using.
    ```bash
    uv run pi0buzzer init 26
    ```
    *   **Expected Output:** A confirmation message: `"Buzzer initialized on pin 26 and saved to buzzer.json."`

2.  **Test the Beep:**
    This command plays a simple, short beep.
    ```bash
    uv run pi0buzzer beep
    ```
    *   **Expected Output:** You should hear a beep from the buzzer.

3.  **Test Playing Music:**
    This command plays a short, pre-defined welcome melody.
    ```bash
    uv run pi0buzzer playmusic
    ```
    *   **Expected Output:** You should hear a short tune.