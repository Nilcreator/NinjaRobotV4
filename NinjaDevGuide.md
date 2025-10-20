# NinjaRobotV3 Development Guide

## 1. Introduction

This document provides a comprehensive guide for developers working on the NinjaRobotV3 project. It covers the project's architecture, the development environment setup, and a detailed description of each library and existing robot function.

### 1.1. Project Architecture

The NinjaRobotV3 project is a modular system composed of several Python sub-projects, each responsible for controlling a specific hardware component or providing a specific functionality. The main application, `pi0ninja_v3`, integrates all these components and exposes a unified web interface for controlling the robot.

The sub-projects are:
- **`pi0ninja_v3`**: The main application that integrates all other components and provides the web interface and AI agent.
- **`piservo0`**: A library for controlling servo motors.
- **`pi0disp`**: A library for controlling the ST7789V display.
- **`pi0buzzer`**: A library for controlling the buzzer.
- **`vl53l0x_pigpio`**: A library for the VL53L0X distance sensor.

### 1.2. Development Environment Setup

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

## 2. Core Libraries

### 2.1. `piservo0`

- **Purpose**: A library for controlling servo motors.
- **Key Classes**:
    - `PiServo`: A basic class for controlling a single servo motor.
    - `CalibrableServo`: Extends `PiServo` with calibration functionality.
    - `MultiServo`: A class to control multiple servos.
    - `ThreadMultiServo`: A class to control multiple servos asynchronously using threads.
- **CLI**: `uv run piservo0 --help`

### 2.2. `pi0disp`

- **Purpose**: A library for controlling the ST7789V display.
- **Key Classes**:
    - `ST7789V`: The main driver for the ST7789V display.
    - `Sprite`: A base class for creating animated objects.
- **CLI**: `uv run pi0disp --help`

### 2.3. `pi0buzzer`

- **Purpose**: A library for controlling the buzzer.
- **Key Classes**:
    - `Buzzer`: A class to control a buzzer.
    - `MusicBuzzer`: Inherits from `Buzzer` and adds music-playing capabilities.
- **CLI**: `uv run pi0buzzer --help`

### 2.4. `vl53l0x_pigpio`

- **Purpose**: A library for the VL53L0X distance sensor.
- **Key Classes**:
    - `VL53L0X`: The main driver for the VL53L0X sensor.
- **CLI**: `uv run vl53l0x_pigpio --help`

## 3. Main Application (`pi0ninja_v3`)

### 3.1. Architecture

The main application is a FastAPI web server that integrates all the hardware controllers and the AI agent. It provides a web interface for controlling the robot and a RESTful API for programmatic access.

### 3.2. Web Server (`web_server.py`)

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

### 3.3. AI Agent (`ninja_agent.py`)

- **System Prompt**: The agent's behavior is defined by a system prompt that instructs it on how to respond to user commands and how to use the available tools.
- **Function Calling**: The agent uses function calling to perform web searches using the `googlesearch-python` library.

### 3.4. Hardware Control

- **Servo Control (`movement_recorder.py`)**: This module provides a `ServoController` class to manage multiple servos and a set of functions to record, play back, and edit servo movement sequences.
- **Display Control (`facial_expressions.py`)**: The `AnimatedFaces` class provides methods to display various animated facial expressions on the ST7789V display.
- **Sound Control (`robot_sound.py`)**: The `RobotSoundPlayer` class provides methods to play sounds corresponding to different emotions.
- **Distance Sensing (`detect_distance.py`)**: The `DistanceDetector` class provides methods to get distance readings from the VL53L0X sensor.

## 4. Troubleshooting

- **`python-multipart` Dependency Error**: If the web server fails to start with a `RuntimeError` indicating that `python-multipart` is not installed, it means a required dependency for handling form data (like voice uploads) is missing. This can be resolved by running `uv pip install python-multipart`.
- **Gemini API File Upload Failures**: If an uploaded file's state becomes `FAILED`, it's likely because the API could not determine the file's type. This can be resolved by explicitly providing the `mime_type` when calling `genai.upload_file()`. For example, for the audio recorded by the web UI, use `mime_type="audio/webm"`.
- **Gemini API File State Errors**: When uploading a file (e.g., for voice commands), the API may return a `400 Bad Request` with the error "File is not in an ACTIVE state." This is a timing issue. It occurs if you attempt to use the file in a `generate_content` call before the API has finished processing it. The solution is to poll the file's status after uploading. Use `genai.get_file()` in a loop with a delay (`time.sleep`) until `file.state.name` is `ACTIVE` before proceeding.
- **API Function Call Errors**: When sending a function response back to the Gemini model (e.g., after a web search), `ImportError` or `AttributeError` related to the `Part` class may occur. This is often due to version differences in the `google-generativeai` library. The most robust solution is to avoid importing `Part` directly and instead construct the response using a plain dictionary, which is less sensitive to library updates.
- **JSON Parsing Errors**: The AI model may occasionally return responses that are not perfectly valid JSON (e.g., using single quotes), causing parsing errors. The current solution is to use a strict system prompt that explicitly instructs the model to return valid, double-quoted JSON.
