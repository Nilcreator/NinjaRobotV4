# NinjaRobotV4

<div align="center">

**An AI-Powered, Modular Robot Platform for Research and STEAM Education**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Raspberry Pi](https://img.shields.io/badge/platform-Raspberry%20Pi%20Zero%202W-red.svg)](https://www.raspberrypi.com/)

</div>

---

## 📋 Table of Contents

- [Project Objective](#-project-objective)
- [NinjaRobotV4 Overview](#-ninjarobotv4-overview)
- [System Architecture](#-system-architecture)
- [Library Introduction](#-library-introduction)
- [Getting Started](#-getting-started)
- [Documentation](#-documentation)
- [Current Status](#-current-status)
- [License](#-license)

---

## 🎯 Project Objective

**NinjaRobotV4** is an open-source robotics platform designed for **AI-integrated Robot Research and STEAM Education**. 

Our mission is to provide:
- **A hands-on learning tool** for students and educators to explore robotics, AI, and hardware integration
- **A research platform** for experimenting with human-robot interaction, computer vision, and autonomous behaviors
- **An accessible entry point** into advanced robotics without requiring expensive commercial kits
- **A modular, extensible codebase** that demonstrates best practices in embedded systems development

This project bridges the gap between theory and practice, making cutting-edge AI technology tangible and interactive through a physical robot that can see, hear, speak, and respond intelligently to its environment.

---

## 🤖 NinjaRobotV4 Overview

### What is NinjaRobotV4?

NinjaRobotV4 is a small, friendly robot powered by a **Raspberry Pi Zero 2W** that combines **AI intelligence** with **physical interaction capabilities**. It can understand natural language commands in multiple languages, express emotions through facial animations and sounds, move using servo motors, and sense its surroundings.

### Key Features

#### 🧠 **AI-Powered Intelligence**
- **Natural Language Understanding**: Powered by **Google Gemini 2.5 Flash**, the robot understands conversational commands with semantic nuance (e.g., "I'm joyful" → shows happy face)
- **Multilingual Communication**: Supports **English, Japanese, Traditional Chinese, and Simplified Chinese** with automatic language detection
- **Real-Time Web Search**: Can answer questions about current events, weather, and facts by searching the internet
- **Context-Aware Responses**: Generates appropriate emotional expressions and movements based on conversation context

#### 🎭 **Expressive Interactions**
- **Animated Facial Expressions**: Displays emotions (happy, sad, surprised, thinking, etc.) on a 240x240 color LCD screen
- **Emotion Sounds**: Plays melodic tones matching its emotional state through a passive buzzer
- **Physical Movements**: Controls up to 8 servo motors for gestures, head movements, and choreographed routines
- **Dynamic Reactions**: Automatically shows a "speaking" face during conversations and "scared" face when obstacles are too close

#### 👁️ **Environmental Awareness**
- **Distance Sensing**: Uses a VL53L0X Time-of-Flight sensor to detect objects up to 2 meters away
- **Obstacle Avoidance**: Automatically stops and reacts when objects come within 50mm, preventing collisions
- **Real-Time Monitoring**: Continuously streams distance data to the web interface

#### 🌐 **Accessible Control**
- **Web-Based Interface**: Control the robot from any device (phone, tablet, computer) through a responsive web app
- **Remote Access**: Automatic public URL generation via **ngrok** with QR code display for instant connection
- **Voice & Text Input**: Interact using your voice (via Web Speech API) or typed messages
- **Manual Controls**: Direct buttons for servo movements, facial expressions, and sounds

#### 🔧 **Developer-Friendly Design**
- **Modular Architecture**: Clean separation between hardware drivers, application logic, and AI agent
- **Centralized Configuration**: Single `config.json` file for all hardware settings
- **Hardware Abstraction Layer**: Easy to swap or upgrade components without changing application code
- **Interactive Calibration Tools**: User-friendly CLI tools for servo calibration and movement recording
- **Well-Documented Code**: Comprehensive inline documentation and type hints

### Hardware Components

- **Raspberry Pi Zero 2W**: Main computer (ARM Cortex-A53, 512MB RAM)
- **ST7789V LCD Display**: 240x240 pixel SPI color screen for facial expressions
- **VL53L0X Distance Sensor**: I2C Time-of-Flight sensor (up to 2000mm range)
- **8x Servo Motors**: SG90 or similar (for body articulation)
- **Passive Buzzer**: 3-5V piezo buzzer for sound generation
- **External 5V Power Supply**: For servo motors (3A recommended)

---

## 🏗️ System Architecture

NinjaRobotV4 follows a **layered architecture** that separates hardware control, application logic, and user interfaces.

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                         │
│  ┌──────────────────┐  ┌─────────────────┐  ┌────────────┐ │
│  │   Web Browser    │  │  Voice Input    │  │  CLI Tools │ │
│  │ (Remote/Local)   │  │ (Speech-to-Text)│  │ (Terminal) │ │
│  └──────────────────┘  └─────────────────┘  └────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                   APPLICATION LAYER                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            ninja_core (Main Application)               │ │
│  │  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐  │ │
│  │  │  NinjaAgent  │  │ Web Server  │  │  Movement    │  │ │
│  │  │  (Gemini AI) │  │  (FastAPI)  │  │  Controller  │  │ │
│  │  └──────────────┘  └─────────────┘  └──────────────┘  │ │
│  │  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐  │ │
│  │  │   Facial     │  │    Sound    │  │  Distance    │  │ │
│  │  │ Expressions  │  │   Player    │  │   Monitor    │  │ │
│  │  └──────────────┘  └─────────────┘  └──────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │     Hardware Abstraction Layer (HAL) + Config          │ │
│  │         (Unified interface to all hardware)            │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    HARDWARE LAYER                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────┐ │
│  │  pi0servo  │  │  pi0disp   │  │ pi0vl53l0x │  │pi0    │ │
│  │  (Servos)  │  │ (Display)  │  │  (Sensor)  │  │buzzer │ │
│  └────────────┘  └────────────┘  └────────────┘  └───────┘ │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           ninja_utils (Shared Utilities)             │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │
                    ┌────────▼──────────┐
                    │   Raspberry Pi    │
                    │  (pigpio daemon)  │
                    └───────────────────┘
```

### Architecture Benefits

1. **Modularity**: Each layer can be developed, tested, and upgraded independently
2. **Reusability**: Hardware drivers can be used in other Raspberry Pi projects
3. **Maintainability**: Clear separation of concerns makes debugging easier
4. **Extensibility**: Add new sensors or actuators by creating new driver libraries
5. **Testability**: Components can be tested individually without full hardware setup

---

## 📚 Library Introduction

NinjaRobotV4 consists of **6 Python packages** organized by responsibility. Each library is installable independently and follows best practices for embedded systems development.

### 🛠️ Hardware Libraries

#### **`pi0servo`** - Servo Motor Control
*Multi-servo control with calibration and smooth interpolation*

- **Purpose**: Controls up to 8 servo motors simultaneously with precise angle positioning
- **Key Features**:
  - Individual servo calibration (min/center/max pulse widths)
  - Smooth interpolated movements between positions
  - Thread-safe asynchronous control
  - Interactive TUI calibration tool
- **CLI Commands**:
  - `pi0servo servo <pin> <angle>` - Move a single servo
  - `pi0servo calib <pin>` - Launch interactive calibration
- **Use Cases**: Robot limbs, head movements, camera gimbals

---

#### **`pi0disp`** - ST7789V Display Driver
*High-performance SPI display driver with partial update support*

- **Purpose**: Controls the 240x240 pixel LCD screen for visual output
- **Key Features**:
  - Full-frame and partial region updates
  - Gamma correction and color space conversion
  - Hardware-accelerated rendering with memory pooling
  - FPS monitoring and performance optimization
- **CLI Commands**:
  - `pi0disp image <path>` - Display an image
  - `pi0disp ball_anime` - Run physics simulation demo
- **Use Cases**: Facial expressions, status indicators, sensor visualizations

---

#### **`pi0vl53l0x`** - VL53L0X Distance Sensor
*I2C Time-of-Flight sensor driver with calibration*

- **Purpose**: Measures distances from 30mm to 2000mm with high accuracy
- **Key Features**:
  - Single-shot and continuous measurement modes
  - Calibration with offset correction
  - Performance benchmarking (up to 50Hz sampling)
  - Error handling and retry logic
- **CLI Commands**:
  - `pi0vl53l0x get --count 10` - Take distance readings
  - `pi0vl53l0x calibrate --distance 100` - Calibrate sensor
- **Use Cases**: Obstacle avoidance, proximity detection, environment mapping

---

#### **`pi0buzzer`** - Passive Buzzer Sound Generation
*Simple sound and music generation through PWM*

- **Purpose**: Plays tones and melodies for auditory feedback
- **Key Features**:
  - Single-tone playback with frequency control
  - Multi-note song sequences
  - Pre-defined melodies
  - Hardware PWM via pigpio
- **CLI Commands**:
  - `pi0buzzer init <pin>` - Configure buzzer GPIO pin
  - `pi0buzzer beep` - Play a test beep
  - `pi0buzzer playmusic` - Play a melody
- **Use Cases**: Notifications, emotional sounds, musical expressions

---

### 🧩 Utility Library

#### **`ninja_utils`** - Shared Utilities
*Common tools used across all libraries*

- **Purpose**: Provides logging and input handling utilities to avoid code duplication
- **Key Components**:
  - **`my_logger.py`**: Centralized logging with consistent formatting
  - **`keyboard.py`**: Non-blocking keyboard input for interactive CLI tools
- **Use Cases**: Debugging, interactive calibration, real-time control

---

### 🎮 Core Application

#### **`ninja_core`** - Main Robot Application
*Integrates all libraries into a cohesive robot system*

- **Purpose**: The "brain" of the robot that coordinates all components
- **Key Modules**:

  **`config.py`** - Centralized Configuration
  - Single `config.json` for all hardware settings
  - Pydantic models for validation
  - Import/export from individual library configs

  **`hal.py`** - Hardware Abstraction Layer
  - Unified interface to all hardware drivers
  - Shared `pigpio` connection management
  - Safe initialization and shutdown sequences

  **`ninja_agent.py`** - AI Agent
  - Google Gemini integration for NLP
  - Semantic understanding and intent mapping
  - Auto-emotion generation
  - Web search capability
  - Multilingual support (EN/JP/ZH-TW/ZH-CN)

  **`movement_controller.py`** - Motion System
  - Multi-servo choreography with interpolation
  - Named movement sequences
  - Emergency stop on obstacle detection

  **`facial_expressions.py`** - Visual Emotions
  - Programmatic face drawing (happy, sad, etc.)
  - Threaded animation engine
  - Automatic idle/speaking states

  **`robot_sound.py`** - Auditory Feedback
  - Emotion-matched sound sequences
  - Synchronized with facial expressions

  **`perception.py`** - Distance Monitoring
  - Background thread for continuous sensing
  - Thread-safe distance queries

  **`web_server.py`** - Web Interface
  - FastAPI REST API
  - WebSocket for real-time data
  - ngrok integration for remote access
  - QR code generation

- **CLI Commands**:
  - `ninja_core server` - Start the web interface
  - `ninja_core chat` - Interactive AI chat in terminal
  - `ninja_core movement-tool` - Record and edit movements
  - `ninja_core config import-all` - Import hardware configs
  - `ninja_core config set-key gemini <key>` - Set AI API key

---

## 🚀 Getting Started

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/Nilcreator/NinjaRobotV4.git
cd NinjaRobotV4

# Install everything with one command
uv pip install -e .

# Set up your API key
ninja_core config set-key gemini YOUR_GEMINI_API_KEY

# Calibrate hardware (follow on-screen instructions)
ninja_core config import-all

# Start the robot web server
ninja_core server
```

For detailed step-by-step instructions, see the **[Installation Guide](InstallationGuide.md)**.

### Documentation

- **[Installation Guide](InstallationGuide.md)** - Complete setup instructions for beginners
- **[Development Log](DevelopmentLog.md)** - Detailed development history and bug fixes
- **[Reconstruction Guide](ReconstructionGuide.md)** - Technical design decisions and architecture
- **[ninja_core README](ninja_core/README.md)** - Developer documentation and API reference

---

## 📊 Current Status

The **Web Server & Remote Access** module has been successfully implemented. The robot now hosts a FastAPI-based web interface that allows for complete control and interaction from any device.

**Completed Features:**
- ✅ All hardware libraries (`pi0servo`, `pi0disp`, `pi0buzzer`, `pi0vl53l0x`, `ninja_utils`)
- ✅ Hardware Abstraction Layer (HAL)
- ✅ Centralized Configuration System
- ✅ AI Agent with Gemini 2.5 Flash integration
- ✅ Multilingual support (4 languages)
- ✅ Web server with voice and text input
- ✅ Remote access via ngrok with QR code
- ✅ Real-time distance monitoring via WebSocket
- ✅ Obstacle avoidance safety system
- ✅ Facial expressions and emotion sounds
- ✅ Motion system with interpolated movements

**Previous Milestones:**
- The **AI Agent** (`ninja_agent.py`) has been successfully implemented with nuanced semantic understanding, multilingual communication, and real-time web search
- The **Motion System** (`movement_controller.py`) was ported and refactored with HAL integration
- All core modules (`perception.py`, `robot_sound.py`, `facial_expressions.py`) are integrated and tested
- All foundational hardware libraries are complete and verified

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Copyright © 2025 Chihkuang Chang**

Hardware libraries `pi0servo`, `pi0disp`, and `pi0vl53l0x` are co-authored with **Tanibayashi Yoichi**.

---

## 🤝 Contributing

Contributions are welcome! This is an educational project, and we encourage:
- Bug reports and feature requests via GitHub Issues
- Code contributions via Pull Requests
- Documentation improvements
- Educational materials and tutorials
- Hardware modifications and alternative designs

---

## 🙏 Acknowledgments

- **Google Gemini** for providing powerful and accessible AI capabilities
- **ngrok** for simplifying remote access
- **Raspberry Pi Foundation** for creating affordable, capable hardware
- The open-source community for Python libraries and hardware drivers

---

<div align="center">

**Built with ❤️ for robotics education and research**

[Installation Guide](InstallationGuide.md) • [Documentation](ninja_core/README.md) • [GitHub](https://github.com/Nilcreator/NinjaRobotV4)

</div>
