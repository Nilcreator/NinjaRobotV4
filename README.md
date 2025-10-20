# NinjaRobotV3

This document provides a comprehensive overview of the NinjaRobotV3 project, including installation instructions, user and developer guides, and a detailed code specification.

## 1. Introduction

Welcome to the world of robotics! The NinjaRobotV3 is a small, friendly robot that you can build yourself. It's powered by a tiny computer called a Raspberry Pi. This project is designed to be a fun and engaging way to learn the basics of how hardware (like motors and sensors) and software (the code) work together.

**What can the NinjaRobot do?**
- **Move:** It walks and moves its arms using eight different motors.
- **See:** It has a laser "eye" to measure how far away things are.
- **Show Emotions:** It has a screen for a face that can display different expressions.
- **Make Sounds:** A small buzzer lets it beep and play simple tunes.
- **Think:** It has an advanced AI "brain" (powered by Google's Gemini) that lets you control it using text or voice commands in a web browser.

By building this robot, you will get a hands-on introduction to electronics, programming, and artificial intelligence, even if you've never written a line of code before!

## 2. Hardware Requirements

Here is a list of the parts you'll need to build your robot. Each component has a special job.

| Component | Quantity | What it does |
| :--- | :--- | :--- |
| Raspberry Pi Zero 2W | 1 | The robot's "brain"—a small computer that runs all the software. |
| Ninja Robot customized expansion HAT & Power Management HAT | 1 set | Special circuit boards that make it easy to connect all the parts to the Pi. |
| SG90 180° servo | 4 | The robot's "muscles" for its legs, allowing it to stand and move. |
| DSpower M005 nano servo | 4 | Smaller "muscles" for the robot's arms. |
| VL53L0X laser distance sensor | 1 | The robot's "eyes"—it uses a laser to see how far away objects are. |
| 2.4-inch SPI TFT Display Module | 1 | The robot's "face," which can show expressions and information. |
| Buzzer | 1 | The robot's "voice," allowing it to make sounds and beeps. |

### Hardware Connections

The Ninja Robot HAT makes it easy to connect everything. Here’s a reference for how the parts are wired. You shouldn't need to change this, but it's helpful for understanding how it works.

#### **Servos (Motors)**

| Body Part | Connected to GPIO Pin |
| :--- | :--- |
| Left Leg | 17 |
| Right Leg | 27 |
| Left Foot | 22 |
| Right Foot | 5 |
| Left Shoulder | 25 |
| Right Shoulder | 23 |
| Left Arm | 21 |
| Right Arm | 24 |

#### **2.4 inch SPI Display (Face)**

| Pin | Ninja HAT Pin Label |
| :--- | :--- |
| GND | GND |
| VCC | 3V3 |
| SCL| SCLK |
| SDA | MOSI |
| RST | 19 |
| DC | 18 |
| CS | CE0 |
| BL | 20 |

#### **2.0 inch SPI Display (Face)**
| Pin | Ninja HAT Pin Label |
| :--- | :--- |
| VCC | 3V3 |
| GND | GND |
| DIN| MOSI |
| CLK | SCLK |
| CS | CE0 |
| DC | 18 |
| RST | 19 |
| BL | 20 |

#### **Buzzer (Voice)**

| Buzzer Pin | Connected to GPIO Pin |
| :--- | :--- |
| Signal | 26 |

#### **VL53L0X Sensor (Eyes)**

This sensor uses a connection called I2C, which has standard pins.

| Pin | Ninja HAT Pin Label |
| :--- | :--- |
| SDA | SDA (I2C) |
| SCL | SCL (I2C) |
| VCC | 3V (I2C) |
| GND | GND (I2C) |

## 3. Software Installation Guide

Now let's get the software—the instructions that tell the robot what to do—set up on your Raspberry Pi.

#### **Step 1: Install Raspberry Pi OS**

*   **What to do:** Use the official Raspberry Pi Imager to install the "Raspberry Pi OS (Legacy, 64-bit)" on your microSD card.
*   **Why:** The operating system is the foundation for all other software. We use the 64-bit Legacy version for the best compatibility with the robot's drivers.
*   **How:** Follow the official guide here: [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

#### **Step 2: Update Your System**

*   **What to do:** Open a terminal on your Raspberry Pi and run this command:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
*   **Why:** This command downloads the latest security updates and software improvements for your Pi's operating system, keeping it healthy and secure.

#### **Step 3: Enable Hardware Interfaces (I2C and SPI)**

*   **What to do:** Run the configuration tool with this command:
    ```bash
    sudo raspi-config
    ```
    In the menu, go to `3 Interface Options` and enable `I3 I2C` and `I4 SPI`.
*   **Why:** The robot's "eyes" (distance sensor) and "face" (display) use special communication methods called I2C and SPI. This step turns them on so the Pi can talk to them.

#### **Step 4: Install Essential Tools**

*   **What to do:** Install `git` and `pigpio` with this command:
    ```bash
    sudo apt install git pigpio -y
    ```
*   **Why:**
    *   `git` is a tool used to download code from the internet, which we'll use to get the NinjaRobot software.
    *   `pigpio` is a library that is very good at controlling the robot's motors and buzzer with precise timing.

#### **Step 5: Start the `pigpio` Service**

*   **What to do:** Run these two commands, one after the other:
    ```bash
    sudo systemctl start pigpiod
    sudo systemctl enable pigpiod
    ```
*   **Why:** This starts the `pigpio` service and sets it to launch automatically every time you turn on your Pi. This is necessary for the motors and buzzer to work.

#### **Step 6: Install `uv` (Python Package Manager)**

*   **What to do:** Run this command to install `uv`, a modern tool for managing Python software.
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    After it finishes, close and reopen your terminal.
*   **Why:** The robot's software is written in Python. `uv` is a fast and easy way to install the specific Python libraries the robot needs to function.

#### **Step 7: Download the NinjaRobotV3 Project**

*   **What to do:** Use `git` to download the robot's source code from GitHub.
    ```bash
    git clone https://github.com/Nilcreator/NinjaRobotV3.git
    ```
    This will create a new folder called `NinjaRobotV3`. Now, move into that folder:
    ```bash
    cd NinjaRobotV3
    ```
*   **Why:** This command copies all the robot's code, guides, and files from its online home onto your Raspberry Pi.

#### **Step 8: Install the Robot's Python Libraries**

*   **What to do:** This is the final software installation step. Make sure you are in the `NinjaRobotV3` directory and run this command:
    ```bash
    uv pip install -e ./pi0ninja_v3 -e ./piservo0 -e ./pi0disp -e ./vl53l0x_pigpio -e ./pi0buzzer
    ```
*   **Why:** This command uses `uv` to install all the different software drivers for the robot's parts (servos, display, etc.). The `-e` makes them "editable," which means you can easily modify the code later if you want to experiment.

## 4. User Guide: Testing and Controlling Your Robot

Your robot is built and the software is installed! Let's run some simple tests and then bring your robot to life.

### Testing Individual Parts

These commands help you check that each component is working correctly.

#### **Test 1: The Buzzer (Voice)**

*   **What to do:** Run this command to test the buzzer. It should play a short "Hello World" sound.
    ```bash
    uv run pi0buzzer init 26
    ```
*   **Why:** This command tells the buzzer driver (`pi0buzzer`) to initialize on GPIO pin 26 and make a sound.

#### **Test 2: The Display (Face)**

*   **What to do:** Run this command to start a test animation on the display. You should see a ball bouncing around the screen. Press `Ctrl+C` to stop.
    ```bash
    uv run pi0disp ball_anime
    ```
*   **Why:** This runs the display driver's (`pi0disp`) built-in test, confirming that the screen is connected and working correctly.

#### **Test 3: The Distance Sensor (Eyes)**

*   **What to do:** Run this command to take 5 distance readings.
    ```bash
    uv run vl53l0x_pigpio get --count 5
    ```
*   **Why:** This tells the sensor driver (`vl53l0x_pigpio`) to measure the distance to the nearest object and print it in millimeters.

#### **Test 4: The Servos (Muscles)**

*   **What to do:** Let's test the left leg servo. Run this command to move it to its center position.
    ```bash
    uv run piservo0 servo 17 1500
    ```
    You can try other pulse widths, like `600` (minimum) or `2400` (maximum).
*   **Why:** This command tells the servo driver (`piservo0`) to move the servo on GPIO pin 17 to a pulse width of 1500 (the center). You can test other servos by changing the pin number (e.g., `27` for the right leg).

### Bringing Your Robot to Life: The Web Interface

This is the most exciting part! You will now start the main web server that lets you control your robot from a browser and chat with its AI brain.

#### **Step 1: Get Your Gemini API Key**

*   **What to do:**
    1.  Go to Google AI Studio: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
    2.  Click "**Create API key**" and copy the long string of letters and numbers. This is your key.
*   **Why:** The Gemini API Key is like a secret password that allows your robot to connect to Google's powerful AI model.

#### **Step 2: Set Up a Public URL for Remote Access (One-Time Setup)**

*   **What to do:** To use the voice chat from any device or control your robot from outside your home network, you need a secure, public URL. This feature uses a tool called `ngrok`. You only need to set this up once.
    1.  Go to the ngrok dashboard and sign up for a free account: [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
    2.  On your dashboard, find your **Authtoken**.
    3.  In your Raspberry Pi terminal, inside the `NinjaRobotV3` folder, run this command, replacing `<YOUR_AUTHTOKEN>` with the token you copied:
        ```bash
        ./ngrok config add-authtoken <YOUR_AUTHTOKEN>
        ```
*   **Why:** This command securely links the `ngrok` tool on your Pi to your account. This allows the web server to create a secure `https://` address, which is required by modern browsers to use the microphone for voice commands.

#### **Step 3: Start the Web Server**

*   **What to do:** In the terminal, from the `NinjaRobotV3` directory, run this command:
    ```bash
    uv run web-server
    ```
*   **Why:** This command starts the main application. It initializes all the robot's hardware, creates the public `ngrok` URL, and starts the web interface.

#### **Step 4: Connect and Chat!**

*   **What to do:** When the server starts, it will print several URLs and display a QR code on its screen.
    1.  **For easy access on a mobile device**, simply scan the QR code on the robot's LCD screen with your phone's camera.
    2.  Alternatively, to use voice chat from a computer, you **must** use the secure public URL. Look for the line in the terminal that says `Secure Public URL (HTTPS): https://<random-string>.ngrok-free.app` and open that URL in a browser.
    3.  The first time you open the page, a popup will ask for your Gemini API Key. Paste the key you got in Step 1.
    4.  The interface will load. You can now talk to your robot!

*   **How to Interact:**
    *   **Text Chat:** Type a command like "say hello" or "raise your left arm" into the chat box and press Enter.
    *   **Voice Chat:** Click the microphone icon (🎤). It will turn red while recording. Speak your command, and it will stop automatically when you pause. Your command will be sent to the robot.

**Congratulations!** Your NinjaRobot is now fully built and ready for action. Have fun exploring the world of robotics!

## 5. Development Guide

This section provides a comprehensive guide for developers working on the NinjaRobotV3 project. It covers the project's architecture, the development environment setup, and a detailed description of each library and existing robot function.

### 5.1. Project Architecture

The NinjaRobotV3 project is a modular system composed of several Python sub-projects, each responsible for controlling a specific hardware component or providing a specific functionality. The main application, `pi0ninja_v3`, integrates all these components and exposes a unified web interface for controlling the robot.

The sub-projects are:
- **`pi0ninja_v3`**: The main application that integrates all other components and provides the web interface and AI agent.
- **`piservo0`**: A library for controlling servo motors.
- **`pi0disp`**: A library for controlling the ST7789V display.
- **`pi0buzzer`**: A library for controlling the buzzer.
- **`vl53l0x_pigpio`**: A library for the VL53L0X distance sensor.

### 5.2. Development Environment Setup

The project uses `uv` for package management and `pigpio` for hardware control.

1.  **Install `pigpio`**:
    ```bash
    sudo apt update
    sudo apt install pigpio -y
    sudo systemctl start pigpiod
    sudo systemctl enable pigpiod
    ```

2.  **Install `uv`**:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    After installation, restart your terminal.

3.  **Clone the repository**:
    ```bash
    git clone https://github.com/Nilcreator/NinjaRobotV3.git
    cd NinjaRobotV3
    ```

4.  **Install dependencies**:
    ```bash
    uv pip install -e ./pi0ninja_v3 -e ./piservo0 -e ./pi0disp -e ./vl53l0x_pigpio -e ./pi0buzzer
    ```

### 5.3. Core Libraries

#### 5.3.1. `piservo0`

- **Purpose**: A library for controlling servo motors.
- **Key Classes**:
    - `PiServo`: A basic class for controlling a single servo motor.
    - `CalibrableServo`: Extends `PiServo` with calibration functionality.
    - `MultiServo`: A class to control multiple servos.
    - `ThreadMultiServo`: A class to control multiple servos asynchronously using threads.
- **CLI**: `uv run piservo0 --help`

#### 5.3.2. `pi0disp`

- **Purpose**: A library for controlling the ST7789V display.
- **Key Classes**:
    - `ST7789V`: The main driver for the ST7789V display.
    - `Sprite`: A base class for creating animated objects.
- **CLI**: `uv run pi0disp --help`

#### 5.3.3. `pi0buzzer`

- **Purpose**: A library for controlling the buzzer.
- **Key Classes**:
    - `Buzzer`: A class to control a buzzer.
    - `MusicBuzzer`: Inherits from `Buzzer` and adds music-playing capabilities.
- **CLI**: `uv run pi0buzzer --help`

#### 5.3.4. `vl53l0x_pigpio`

- **Purpose**: A library for the VL53L0X distance sensor.
- **Key Classes**:
    - `VL53L0X`: The main driver for the VL53L0X sensor.
- **CLI**: `uv run vl53l0x_pigpio --help`

### 5.4. Main Application (`pi0ninja_v3`)

#### 5.4.1. Architecture

The main application is a FastAPI web server that integrates all the hardware controllers and the AI agent. It provides a web interface for controlling the robot and a RESTful API for programmatic access.

#### 5.4.2. Web Server (`web_server.py`)

- **API Endpoints**:
    - `GET /api/agent/status`: Returns the status of the AI agent.
    - `POST /api/agent/set_api_key`: Sets the Gemini API key.
    - `POST /api/agent/chat`: Sends a text message to the AI agent.
    - `POST /api/agent/chat_voice`: Sends a voice message to the AI agent.
    - `GET /api/servos/movements`: Returns a list of available servo movements.
    - `POST /api/servos/movements/{movement_name}/execute`: Executes a servo movement.
    - `GET /api/display/expressions`: Returns a list of available facial expressions.
    - `POST /api/display/expressions/{expression_name}`: Displays a facial expression.
    - `GET /api/sound/emotions`: Returns a list of available emotion sounds.
    - `POST /api/sound/emotions/{emotion_name}`: Plays an emotion sound.
    - `GET /api/sensor/distance`: Returns the current distance from the sensor.
- **WebSocket Endpoints**:
    - `WS /ws/distance`: Streams the distance sensor data.

#### 5.4.3. AI Agent (`ninja_agent.py`)

- **System Prompt**: The agent's behavior is defined by a system prompt that instructs it on how to respond to user commands and how to use the available tools.
- **Function Calling**: The agent uses function calling to perform web searches using the `googlesearch-python` library.

#### 5.4.4. Hardware Control

- **Servo Control (`hardware_controllers.py`)**: This module provides a `ServoController` class to manage multiple servos.
- **Display Control (`hardware_controllers.py`)**: The `AnimatedFaces` class provides methods to display various animated facial expressions on the ST7789V display.
- **Sound Control (`hardware_controllers.py`)**: The `RobotSoundPlayer` class provides methods to play sounds corresponding to different emotions.
- **Distance Sensing (`hardware_controllers.py`)**: The `DistanceDetector` class provides methods to get distance readings from the VL53L0X sensor.

## 6. Troubleshooting

- **`python-multipart` Dependency Error**: If the web server fails to start with a `RuntimeError` indicating that `python-multipart` is not installed, it means a required dependency for handling form data (like voice uploads) is missing. This can be resolved by running `uv pip install python-multipart`.
- **Gemini API File Upload Failures**: If an uploaded file's state becomes `FAILED`, it's likely because the API could not determine the file's type. This can be resolved by explicitly providing the `mime_type` when calling `genai.upload_file()`. For example, for the audio recorded by the web UI, use `mime_type="audio/webm"`.
- **Gemini API File State Errors**: When uploading a file (e.g., for voice commands), the API may return a `400 Bad Request` with the error "File is not in an ACTIVE state." This is a timing issue. It occurs if you attempt to use the file in a `generate_content` call before the API has finished processing it. The solution is to poll the file's status after uploading. Use `genai.get_file()` in a loop with a delay (`time.sleep`) until `file.state.name` is `ACTIVE` before proceeding.
- **API Function Call Errors**: When sending a function response back to the Gemini model (e.g., after a web search), `ImportError` or `AttributeError` related to the `Part` class may occur. This is often due to version differences in the `google-generativeai` library. The most robust solution is to avoid importing `Part` directly and instead construct the response using a plain dictionary, which is less sensitive to library updates.
- **JSON Parsing Errors**: The AI model may occasionally return responses that are not perfectly valid JSON (e.g., using single quotes), causing parsing errors. The current solution is to use a strict system prompt that explicitly instructs the model to return valid, double-quoted JSON.

## 7. Development Log

This file tracks the development progress of the NinjaRobot project.

### 2025-10-20: Phase 2 Refactoring

- **Change**: Consolidated hardware configuration and control logic.
- **Details**:
    - Merged `servo.json` and `buzzer.json` into a single `config.json`.
    - Created a new `hardware_controllers.py` module to house the `ServoController`, `AnimatedFaces`, `RobotSoundPlayer`, and `DistanceDetector` classes.
    - Updated all relevant files to use the new centralized configuration and hardware controller modules.

### 2025-10-18: Documentation Overhaul

- **Change**: A comprehensive review and update of all project documentation was completed.
- **Details**:
    - `InstallationGuide.md`, `NinjaUserGuide.md`, and `NinjaDevGuide.md` were corrected, updated, and refined to ensure they are accurate and provide complete information for users and developers.
    - A new `NinjaCodeSpec.md` document was generated, providing a detailed, code-level specification of the entire project, including file structures, imported libraries, and detailed descriptions of every function and method.

### 2025-09-27: Fixed Sound Playback Crash

- **Problem**: The application would crash with an `AttributeError` when the AI agent tried to play a sound, particularly after a voice command.
- **Root Cause**: A regression was introduced in a previous refactoring. The code was incorrectly calling the `RobotSoundPlayer.play` method as a static method and passing the wrong arguments, leading to the error.
- **Solution**: The sound playback logic in `web_server.py` was corrected. It now uses the available `buzzer` controller to correctly iterate through the sound's melody and play each note, resolving the crash.

### 2025-09-27: Refactored Display Logic for Thread-Safety

- **Problem**: The LCD screen displayed corrupted data ("noise") when changing facial expressions, indicating a critical race condition.
- **Root Cause**: The `AnimatedFaces` class was not thread-safe. Multiple threads were being created by the web server to play different animations, and they were attempting to write to the SPI display simultaneously without any locking or coordination.
- **Solution**: The `AnimatedFaces` class in `facial_expressions.py` was completely refactored. It now manages its own internal `threading.Thread` and uses a `threading.Event` to ensure that only one animation can be active at a time. A new `_start_animation` method safely stops any existing animation thread before starting a new one, eliminating the race condition. The logic in `web_server.py` was then greatly simplified to rely on this new thread-safe class, removing the need for complex and faulty `asyncio.Task` management for the display.

### 2025-09-27: Display Task and Shutdown Reliability Fix

- **Problem**: The server would freeze on shutdown, and the LCD screen would show noise when changing facial expressions.
- **Root Cause**: The background display task was not being managed correctly, leading to an infinite loop blocking shutdown and race conditions causing screen corruption.
- **Solution**:
    - **Centralized Task Management**: Implemented a robust task management system for all display animations. A single, authoritative background task is now tracked in the application state. This task is properly cancelled and replaced when expressions change, eliminating race conditions.
    - **Graceful Shutdown**: The `lifespan` manager now explicitly cancels the display task on shutdown, allowing the server to terminate cleanly and fixing the freeze on Ctrl+C.
    - **Idle on Interaction**: The QR code is now displayed until the user sends their first command, at which point the screen transitions to a persistent idle face.

### 2025-09-27: Server Shutdown and Interaction Fixes

- **Problem**: The server would freeze on shutdown (Ctrl+C), and the display did not provide feedback when a user started interacting with the robot.
- **Root Cause**: The background display task was not being cancelled on shutdown, causing an infinite loop to block the process from exiting.
- **Solution**:
    - **Shutdown Fix**: Implemented proper background task management in the `lifespan` manager. The display task is now tracked and explicitly cancelled on shutdown, allowing the server to exit cleanly.
    - **Idle Face on Interaction**: The display now shows the QR code indefinitely until a user sends the first chat command. Upon this first interaction, the QR code is replaced by a persistent `idle` face animation, providing clear visual feedback that the robot is "awake".

### 2025-09-27: QR Code Display Fix and Startup Refinement

- **Problem**: The QR code display on the LCD screen was crashing the application due to an incorrect image format, and the startup sequence was not optimal.
- **Root Cause**: The QR code image was being generated in a grayscale format, which was incompatible with the display driver that expected an RGB image. 
- **Solution**:
    - Modified `web_server.py` to explicitly convert the QR code image to 'RGB' format before displaying it, fixing the crash.
    - Refactored the startup logic within the `lifespan` manager to ensure all hardware and agent initializations are logged before the network and display sequences begin, providing a clearer startup log for the user.

### 2025-09-27: Ngrok Connection Resiliency

- **Problem**: The `ngrok` service was failing to start due to network timeouts, preventing the web server from being accessible remotely.
- **Root Cause**: Transient network issues were causing the initial `ngrok.connect()` call to fail.
- **Solution**: Implemented a retry mechanism in `web_server.py`. The application now attempts to connect to the ngrok service up to 3 times with a 5-second delay between attempts, making the startup process more resilient to temporary network glitches.

### 2025-09-27: Startup and Servo Performance Optimization

- **Change**: Overhauled the web server startup sequence and fixed a critical servo initialization bug.
- **Reason**: To provide a better user experience on startup and to resolve servo performance issues.
- **Implementation**:
    - **Startup Sequence**: The `web_server.py` `lifespan` manager now orchestrates the entire startup. It starts `ngrok`, displays a QR code of the URL on the robot's LCD for 60 seconds, and then transitions the display to an `idle` face to show the robot is ready.
    - **Servo Fix**: Modified `movement_recorder.py` to move all servos to their center position upon initialization. This "activates" the servos with `pigpio`, eliminating `pigpio err` warnings and ensuring smooth movement from a known starting state.
- **Documentation**: Updated all relevant user and developer guides to reflect the new, more robust startup procedure and the servo performance fix.

### 2025-09-27: QR Code for Easy Access

- **Change**: The web server now generates a QR code of the secure `ngrok` URL and displays it on the robot's LCD screen upon startup.
- **Reason**: To provide a fast and convenient way for users to access the web control interface on a mobile device without having to manually type the URL.
- **Implementation**:
    - Added the `qrcode` library as a dependency.
    - Modified `web_server.py` to use the `qrcode` library to generate an image of the URL.
    - Integrated the `pi0disp` driver to display the generated QR code image on the ST7789V screen.
- **Documentation**: Updated the `InstallationGuide.md`, `NinjaUserGuide.md`, and `NinjaDevGuide.md` to reflect this new feature.

### 2025-09-23: Voice Input Upload Fix

- **Problem**: The voice input feature failed with an error indicating the uploaded file processing had `FAILED`.
- **Root Cause**: The Gemini API was rejecting the uploaded audio file because its type was not explicitly specified. Although the file was a standard `.webm`, the API requires the MIME type for reliable processing.
- **Solution**: Modified `ninja_agent.py` to explicitly set `mime_type="audio/webm"` in the `genai.upload_file()` call. This ensures the API correctly identifies and processes the audio file, resolving the upload failure.

### 2025-09-23: Voice Input Robustness Fix

- **Problem**: The voice input feature failed with a `400 Bad Request` error, stating the uploaded audio file was "not in an ACTIVE state."
- **Root Cause**: A timing issue where the application was sending the uploaded audio file to the Gemini model for processing before the API had finished preparing it.
- **Solution**: Implemented a robust waiting mechanism in `ninja_agent.py`. The code now uploads the file, then polls the Gemini API, waiting until the file's status is 'ACTIVE' before sending it to the model. This includes a timeout to prevent indefinite waiting and ensures the temporary file is deleted, resolving the error and making the voice feature reliable.

### 2025-09-23: Environment Sync Fix

- **Problem**: The web server failed to start with a `RuntimeError`, indicating the `python-multipart` dependency was not installed.
- **Root Cause**: The project's virtual environment was out of sync with the `pyproject.toml` file, which already specified the dependency correctly.
- **Solution**: Re-ran the `uv pip install` command to synchronize the environment and install the missing package. This resolves the startup error.

### 2025-09-23: Voice Input Feature Re-instated

- **Change**: A "record-then-process" voice input feature has been added to the web interface.
- **Reason**: To provide an alternative, hands-free method for sending commands to the robot, as requested. This implementation differs from the previous live streaming approach.
- **Implementation**:
    - **Frontend**: A microphone button was added. It uses the `MediaRecorder` and Web Audio APIs to record user speech, automatically stopping on silence (3s) or after a maximum duration (30s).
    - **Backend**: A new endpoint (`/api/agent/chat_voice`) accepts the recorded audio file. The `NinjaAgent` uses the Gemini API's multimodal capabilities to transcribe the audio and execute the command.
- **Linting**: Added `ruff` as a development dependency to `pi0ninja_v3` to ensure code quality for new backend changes.


### 2025-09-23: Voice Input Feature Removal

- **Change**: The live voice input feature has been completely removed from the project.
- **Reason**: To simplify the user interface and core functionality, focusing on the text-based chat experience.
- **Impact**:
    - The `ninja_agent` has been updated to only process text commands.
    - The `/ws/voice` WebSocket endpoint and all related backend code have been removed.
    - The microphone button and all associated JavaScript have been removed from the frontend.
    - All documentation has been updated to reflect the removal of this feature.
    - The `pyngrok` integration is preserved to provide a reliable, secure HTTPS tunnel to the web interface, but is no longer a requirement for the primary AI functionality.

### 2025-09-23: Architectural Change: Ngrok Integration Refactored to `pyngrok`

- **Problem**: The automated `ngrok` startup was unreliable, failing with `Connection refused` errors. The manual `subprocess` management approach was brittle and difficult to debug.
- **Root Cause**: The `subprocess` approach did not provide robust control over the `ngrok` process lifecycle, leading to race conditions and silent failures.
- **Solution**: Replaced the entire manual `subprocess` and `requests` implementation with the `pyngrok` library. This is a major architectural improvement that delegates all `ngrok` process management to a dedicated, robust library. `pyngrok` now handles the tunnel creation, URL fetching, and shutdown, resolving the startup failures and making the code cleaner and more reliable. The `pi0ninja_v3` dependencies and the web server startup sequence have been updated accordingly.

### 2025-09-22: Ngrok Automatic Startup Reliability Fix

- **Problem**: The automated `ngrok` secure tunnel failed to activate intermittently upon starting the web server.
- **Root Cause**: A race condition was identified where the server script attempted to fetch the public URL from the `ngrok` API before the `ngrok` service had fully initialized. The previous static `time.sleep()` was an unreliable solution.
- **Solution**: Replaced the fixed delay with a robust retry mechanism in the `get_ngrok_url` function. The function now repeatedly attempts to connect to the `ngrok` API for a few seconds, ensuring it only proceeds once the tunnel is active and the URL is available. This makes the automatic HTTPS startup process reliable.

### 2025-09-21: Voice Agent Re-architecture

- **Problem**: The voice agent was unresponsive because the underlying Gemini library does not support true bidirectional audio streaming. The previous implementation was only a diagnostic placeholder.
- **Solution**: Re-architected the entire voice pipeline to a "record-then-process" model. The frontend now records the user's full utterance and sends the complete audio file to the backend. The `NinjaAgent` was updated with a new `process_audio_input` method that sends the audio data directly to the Gemini API for transcription and execution. This provides a fully functional and reliable voice command experience.
- **UI**: The frontend was updated to provide clear visual feedback for "recording" and "processing" states.

### 2025-09-21: Automated HTTPS and Voice Agent Diagnostics

- **Ngrok Automation**: Modified the `web_server.py` script to automatically start, manage, and terminate an `ngrok` subprocess. The server now fetches and displays the public HTTPS URL on startup, streamlining the process of enabling the microphone for voice input.
- **Voice Agent Diagnostic**: Addressed an issue where the voice agent was unresponsive. The `ninja_agent.py` was updated to consume the audio stream and log the receipt of data, confirming the data pipeline is working. This serves as a diagnostic step while a full speech-to-text implementation is pending.

### 2025-09-21: HTTPS Voice Input and Linting

- **HTTPS for Voice Input**: Successfully configured and enabled `ngrok` to provide a secure HTTPS tunnel to the local web server. This resolves the browser security error (`Microphone access requires a secure (HTTPS) connection`) and enables the microphone for live voice interaction with the AI agent.
- **Code Linting**: Fixed several linting issues in the `pi0ninja_v3` codebase, including unused imports and module-level imports not being at the top of the file, improving code quality and adherence to standards.

### 2025-09-21: AI Agent Web Search Fix (ImportError)

- **Problem**: Fixed an `ImportError: cannot import name 'Part' from 'google.generativeai.types'` that occurred at startup.
- **Root Cause**: A previous fix for an `AttributeError` incorrectly assumed the `Part` class was available for import. The `ImportError` revealed that the installed version of the `google-generativeai` library does not expose this class in its `types` module.
- **Solution**: To create a more robust and version-agnostic solution, the code was refactored to not rely on importing the `Part` class. Instead, the function response is now constructed using a standard Python dictionary, which the library accepts. This resolves the import error and makes the code less likely to break with future library updates.

### 2025-09-21: AI Agent and Documentation Update

- **JSON Parsing Robustness**: Addressed a bug where the AI agent would fail to parse responses from the language model due to invalid JSON formatting (e.g., single quotes). The system prompt was enhanced to enforce a strict, double-quoted JSON output for all action commands. Diagnostic logging was also added to capture the raw AI response for easier debugging.
- **HTTPS for Voice Input**: Resolved the issue where voice input was disabled. This was identified as a browser security feature requiring an HTTPS connection. The `NinjaUserGuide.md` was updated with a comprehensive, step-by-step guide on how to use `ngrok` to create a secure `https://` tunnel for local development. The `NinjaDevGuide.md` was also updated to reflect these changes.

### 2025-09-21: AI Agent Bug Fix

- **Problem**: Fixed a `ModuleNotFoundError: No module named 'default_api'` that occurred when starting the web server.
- **Root Cause**: The error was caused by an incorrect import of a `google_web_search` function that was not defined. The agent was trying to import a tool as a regular module.
- **Solution**: Removed the incorrect import and implemented the `web_search` function within the `NinjaAgent` class using the `googlesearch-python` library. This resolves the startup crash and correctly integrates the web search tool with the agent's capabilities.

### 2025-09-21: AI Agent Major Upgrade

- **Live Voice Streaming**: Re-architected the AI agent to support real-time, low-latency voice conversations. The implementation now uses a WebSocket (`/ws/voice`) to stream audio directly from the browser to the backend, which then communicates with the Gemini streaming model. This replaces the previous text-based input and provides a much more natural and interactive experience.
- **Web Search Capability**: Integrated function calling into the AI agent. The agent can now decide when to search the web to answer questions beyond its core capabilities (e.g., weather, facts, news). It uses the `google_web_search` tool and incorporates the findings into its conversational responses.
- **Bug Fixes & Enhancements**:
    - Fixed a critical bug where the robot would not execute movements planned by the AI agent.
    - Improved the AI's system prompt to be more robust in understanding multilingual commands and intents.
    - Updated all relevant documentation (`README.md`, `NinjaUserGuide.md`, `NinjaDevGuide.md`) to reflect the new architecture and features.

### 2025-09-20: Web Server Usability

- **Enhanced Startup Message**: Improved the web server's startup sequence to automatically detect and display both the hostname and IP address connection URLs, making it easier for users to connect to the robot's control panel.

### 2025-09-20: Servo Driver Bug Fix

- **Problem**: Fixed a `pigpio.error: 'GPIO is not in use for servo pulses'` that occurred when executing a servo movement from the web interface for the first time.
- **Root Cause**: The error was caused by the system trying to read the.current position of a servo that had not yet been activated, resulting in an invalid state.
- **Solution**: Made the underlying `piservo0` driver more robust. The `get_pulse()` method was updated to catch the error and return a default center value, allowing movements to start correctly from a "cold" state.

(Previous entries remain)
