# NinjaRobotV3 User Guide

## 1. Introduction

Welcome to the NinjaRobotV3! This guide will help you get started with controlling your robot and using its various features. Whether you want to make it walk, talk, or show emotions, you'll find all the information you need right here.

## 2. Getting Started

Before you can start using your robot, you need to make sure you have followed the installation instructions in the `InstallationGuide.md` file. This includes setting up the hardware, installing the software, and configuring the necessary services.

## 3. Controlling the Robot

The primary way to control your NinjaRobotV3 is through its web interface.

### 3.1. Starting the Web Server

1.  Open a terminal on your Raspberry Pi.
2.  Navigate to the `NinjaRobotV3` directory.
3.  Run the following command:
    ```bash
    uv run web-server
    ```

### 3.2. Accessing the Web Interface

Once the web server is running, you can access the web interface in two ways:

1.  **QR Code**: A QR code will be displayed on the robot's LCD screen. Scan this code with your smartphone or tablet to open the web interface.
2.  **URL**: The web server will print a local URL in the terminal (e.g., `http://<your-pi-ip-address>:8000`). Open this URL in a web browser on a device connected to the same network as your robot.

### 3.3. Interacting with the AI Agent

The web interface features a chat window where you can interact with the robot's AI agent.

-   **Text Input**: Type a command in the chat box and press Enter or click the "Send" button.
-   **Voice Input**: Click the microphone button to start recording. Speak your command, and the robot will respond.

**Example Commands:**
- "Say hello"
- "Raise your left arm"
- "What's the weather like today?"
- "Tell me a joke"

## 4. Library-Specific User Guides

### 4.1. `piservo0` - Servo Motor Control

- **Purpose**: This library allows you to control the robot's servo motors.
- **CLI**:
    - `uv run piservo0 --help`: Shows all available commands.
    - `uv run piservo0 servo <pin> <pulse>`: Moves a single servo to a specific pulse width.
        - **Example**: `uv run piservo0 servo 17 1500` (moves the servo on pin 17 to the center position).
    - `uv run piservo0 calib <pin>`: Starts the interactive calibration tool for a specific servo.
- **Python Library Usage**:
    ```python
    import time
    import pigpio
    from piservo0 import CalibrableServo

    pi = pigpio.pi()
    servo = CalibrableServo(pi, 17)

    servo.move_angle(90)
    time.sleep(1)
    servo.move_angle(-90)
    time.sleep(1)

    servo.off()
    pi.stop()
    ```

### 4.2. `pi0disp` - Display Control

- **Purpose**: This library allows you to control the robot's display.
- **CLI**:
    - `uv run pi0disp --help`: Shows all available commands.
    - `uv run pi0disp ball_anime`: Runs a bouncing ball animation.
    - `uv run pi0disp image <image_path>`: Displays an image on the screen.
- **Python Library Usage**:
    ```python
    from pi0disp import ST7789V
    from PIL import Image, ImageDraw

    with ST7789V() as lcd:
        image = Image.new("RGB", (lcd.width, lcd.height), "black")
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 100, 100), fill="red")
        lcd.display(image)
    ```

### 4.3. `pi0buzzer` - Buzzer Control

- **Purpose**: This library allows you to control the robot's buzzer.
- **CLI**:
    - `uv run pi0buzzer --help`: Shows all available commands.
    - `uv run pi0buzzer init <pin>`: Initializes the buzzer on a specific GPIO pin.
    - `uv run pi0buzzer beep`: Plays a simple beep.
    - `uv run pi0buzzer playmusic`: Plays a pre-defined song.
- **Python Library Usage**:
    ```python
    import pigpio
    from pi0buzzer.driver import Buzzer

    pi = pigpio.pi()
    buzzer = Buzzer(pi, 26)

    buzzer.play_sound(440, 0.5) # Play 440 Hz for 0.5 seconds

    buzzer.off()
    pi.stop()
    ```

### 4.4. `vl53l0x_pigpio` - Distance Sensor

- **Purpose**: This library allows you to get distance readings from the VL53L0X sensor.
- **CLI**:
    - `uv run vl53l0x_pigpio --help`: Shows all available commands.
    - `uv run vl53l0x_pigpio get --count 5`: Takes 5 distance readings.
    - `uv run vl53l0x_pigpio calibrate`: Starts the interactive calibration tool.
- **Python Library Usage**:
    ```python
    import pigpio
    from vl53l0x_pigpio import VL53L0X

    pi = pigpio.pi()
    with VL53L0X(pi) as tof:
        distance = tof.get_range()
        print(f"Distance: {distance} mm")
    pi.stop()
    ```

## 5. `pi0ninja_v3` - The Robot's Brain

The `pi0ninja_v3` library is the central nervous system of your robot. It integrates all the other libraries and provides the main functionalities of the robot, including the web interface and the AI agent.

### 5.1. `movement_recorder.py`

- **Purpose**: This script allows you to record, play back, and edit servo movement sequences.
- **CLI**:
    - `python -m pi0ninja_v3.movement_recorder`: Starts the interactive movement recorder menu.
- **Menu Options**:
    - **1. Record new movement**: Allows you to create a new movement sequence by manually inputting servo angles.
    - **2. Modify existing movement**: Allows you to edit an existing movement sequence.
    - **3. Execute a movement**: Plays back a saved movement sequence.
    - **4. Clear movement**: Deletes a saved movement sequence.

### 5.1.1. Recording a New Movement: Command Rules

When you select "1. Record new movement" from the menu, you will be prompted to enter servo movement commands. These commands have a specific format that you need to follow.

**Command Structure:**

`[speed_]pin:angle[/pin:angle]...`

-   **`speed` (optional):** A single character to set the speed of the movement.
    -   `S`: Slow
    -   `M`: Medium (default)
    -   `F`: Fast
-   **`pin`:** The GPIO pin number of the servo you want to move.
-   **`angle`:** The angle to move the servo to. This can be:
    -   A number from -90 to 90.
    -   `C`: Center (0 degrees)
    -   `X`: Max (90 degrees)
    -   `M`: Min (-90 degrees)

You can specify movements for multiple servos in a single command by separating them with a `/`.

**Example:**

`S_17:45/27:C`

This command will:
-   Set the speed to **Slow**.
-   Move the servo on pin **17** to **45** degrees.
-   Move the servo on pin **27** to the **Center** (0 degrees).

After entering a command, you will have the option to confirm the movement, reset to the previous position, or finish the recording.

### 5.2. `show_faces.py`

- **Purpose**: This script allows you to display the robot's facial expressions.
- **CLI**:
    - `python -m pi0ninja_v3.show_faces`: Starts an interactive menu to display facial expressions.
- **Menu Options**:
    - A list of available expressions will be displayed. Enter the number corresponding to the expression you want to see.

### 5.3. `robot_sound.py`

- **Purpose**: This script allows you to play sounds corresponding to the robot's emotions.
- **CLI**:
    - `python -m pi0ninja_v3.robot_sound`: Starts an interactive menu to play sounds.
- **Menu Options**:
    - A list of available emotions will be displayed. Enter the number corresponding to the sound you want to hear.

### 5.4. `detect_distance.py`

- **Purpose**: This script allows you to get distance readings from the VL53L0X sensor.
- **CLI**:
    - `python -m pi0ninja_v3.detect_distance`: Starts an interactive menu to perform distance measurements.
- **Menu Options**:
    - **1. Timed Detection**: Performs a specified number of distance measurements with a delay.
    - **2. Continuous Detection**: Performs continuous distance measurement at 5Hz until 'q' is pressed.
