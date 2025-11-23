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
- **Safe Shutdown**: Power off the robot safely directly from the web interface

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
│  ┌──────────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │   Web Browser    │  │  Voice Input    │  │  CLI Tools │  │
│  │ (Remote/Local)   │  │ (Speech-to-Text)│  │ (Terminal) │  │
│  └──────────────────┘  └─────────────────┘  └────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                   APPLICATION LAYER                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            ninja_core (Main Application)               │ │
│  │  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐   │ │
│  │  │  NinjaAgent  │  │ Web Server  │  │  Movement    │   │ │
│  │  │  (Gemini AI) │  │  (FastAPI)  │  │  Controller  │   │ │
│  │  └──────────────┘  └─────────────┘  └──────────────┘   │ │
│  │  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐   │ │
│  │  │   Facial     │  │    Sound    │  │  Distance    │   │ │
│  │  │ Expressions  │  │   Player    │  │   Monitor    │   │ │
│  │  └──────────────┘  └─────────────┘  └──────────────┘   │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │     Hardware Abstraction Layer (HAL) + Config          │ │
│  │         (Unified interface to all hardware)            │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    HARDWARE LAYER                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────┐  │
│  │  pi0servo  │  │  pi0disp   │  │ pi0vl53l0x │  │pi0    │  │
│  │  (Servos)  │  │ (Display)  │  │  (Sensor)  │  │buzzer │  │
│  └────────────┘  └────────────┘  └────────────┘  └───────┘  │
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

---
---

# NinjaRobotV4（日本語版）

<div align="center">

**研究とSTEAM教育のための、AI搭載のモジュール型ロボットプラットフォーム**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Raspberry Pi](https://img.shields.io/badge/platform-Raspberry%20Pi%20Zero%202W-red.svg)](https://www.raspberrypi.com/)

</div>

---

## 📋 目次

- [プロジェクトの目的](#-プロジェクトの目的)
- [NinjaRobotV4の概要](#-ninjarobotv4の概要)
- [システム構成](#-システム構成)
- [ライブラリの紹介](#-ライブラリの紹介)
- [はじめに](#-はじめに)
- [ドキュメント](#-ドキュメント)
- [現在の状況](#-現在の状況)
- [ライセンス](#-ライセンス)

---

## 🎯 プロジェクトの目的

**NinjaRobotV4**は、**AI統合ロボット研究とSTEAM教育**のために設計された、オープンソース（誰でも自由に使える）のロボットプラットフォームです。

私たちの使命は以下を提供することです:
- **実践的な学習ツール** - 学生や教育者がロボット工学、AI、ハードウェア統合を探求するための教材
- **研究プラットフォーム** - 人間とロボットの相互作用、コンピュータビジョン（カメラで物を見る技術）、自律行動を実験するための基盤
- **アクセスしやすい入口** - 高価な商用キットを必要とせずに、先進的なロボット工学に触れられる機会
- **モジュール型で拡張可能なコードベース** - 組み込みシステム（小型コンピュータを使った機器）開発のベストプラクティス（良い方法）を示す設計

このプロジェクトは、理論と実践のギャップを埋め、最先端のAI技術を、見て、聞いて、話して、環境に知的に反応できる物理的なロボットを通じて、触れられるものにします。

---

## 🤖 NinjaRobotV4の概要

### NinjaRobotV4とは？

NinjaRobotV4は、**Raspberry Pi Zero 2W**（小型で安価なコンピュータ）で動く、小さくて親しみやすいロボットです。**AI知能**と**物理的な動作能力**を組み合わせています。複数の言語で自然な会話コマンドを理解し、顔のアニメーションや音で感情を表現し、サーボモーター（角度を制御できるモーター）を使って動き、周囲を感知することができます。

### 主な機能

#### 🧠 **AI搭載の知能**
- **自然言語理解** - **Google Gemini 2.5 Flash**（Googleの最新AI）を搭載し、会話的なコマンドを意味のニュアンスまで理解します（例:「嬉しい」→ハッピーな顔を表示）
- **多言語コミュニケーション** - **日本語、英語、繁体字中国語、簡体字中国語**に対応し、自動的に言語を検出します
- **リアルタイムWeb検索** - インターネットを検索して、現在のニュース、天気、事実についての質問に答えることができます
- **文脈を理解した応答** - 会話の文脈に基づいて、適切な感情表現や動きを生成します

#### 🎭 **表現豊かなインタラクション**
- **アニメーション化された表情** - 240x240ピクセルのカラー液晶画面に感情（嬉しい、悲しい、驚き、考え中など）を表示します
- **感情音** - パッシブブザー（電子音を出す部品）を通じて、感情状態に合ったメロディックな音を再生します
- **物理的な動き** - 最大8個のサーボモーターを制御して、ジェスチャー、頭の動き、振り付けられたルーチン（決まった動作）を実行します
- **ダイナミックな反応** - 会話中は自動的に「話している」顔を表示し、障害物が近すぎると「怖がっている」顔を表示します

#### 👁️ **環境認識**
- **距離センシング** - VL53L0X ToF（Time-of-Flight：光の飛行時間で距離を測る）センサーを使用して、最大2メートル離れた物体を検出します
- **障害物回避** - 物体が50mm以内に来ると自動的に停止して反応し、衝突を防ぎます
- **リアルタイム監視** - Webインターフェース（ブラウザで見る画面）に距離データを継続的に送信します

#### 🌐 **アクセスしやすい制御**
- **Webベースのインターフェース** - レスポンシブWebアプリ（スマホでもPCでも見やすい画面）を通じて、任意のデバイス（スマホ、タブレット、コンピュータ）からロボットを制御できます
- **リモートアクセス** - **ngrok**（インターネット経由でアクセスできるようにするサービス）を介した自動公開URL生成とQRコード表示で、即座に接続できます
- **音声とテキスト入力** - 音声（Web Speech API：ブラウザの音声認識機能を使用）または入力したメッセージで対話できます
- **手動コントロール** - サーボの動き、表情、音を直接操作するボタンがあります

#### 🔧 **開発者に優しい設計**
- **モジュール型アーキテクチャ** - ハードウェアドライバー（機器を動かすプログラム）、アプリケーションロジック（処理の流れ）、AIエージェント（AI部分）が明確に分離されています
- **集中型設定** - すべてのハードウェア設定を1つの`config.json`ファイルで管理します
- **ハードウェア抽象化レイヤー** - アプリケーションコードを変更せずに、コンポーネント（部品）を簡単に交換またはアップグレードできます
- **インタラクティブな校正ツール** - サーボの校正（正確な動きの調整）や動作の記録のための、使いやすいCLIツール（コマンドラインで使うツール）があります
- **よく文書化されたコード** - 包括的なインラインドキュメント（コード内の説明）と型ヒント（データの種類の注釈）があります

### ハードウェアコンポーネント（部品）

- **Raspberry Pi Zero 2W** - メインコンピュータ（ARM Cortex-A53プロセッサ、512MBメモリ）
- **ST7789V液晶ディスプレイ** - 240x240ピクセルのSPI（通信方式の一種）カラー画面で表情を表示
- **VL53L0X距離センサー** - I2C（通信方式の一種）ToFセンサー（最大2000mm範囲）
- **8個のサーボモーター** - SG90または類似品（体の関節を動かすため）
- **パッシブブザー** - 3-5V圧電ブザー（音を生成するため）
- **外部5V電源** - サーボモーター用（3A推奨）

---

## 🏗️ システム構成

NinjaRobotV4は、ハードウェア制御、アプリケーションロジック、ユーザーインターフェースを分離する**レイヤードアーキテクチャ**（層状の構造）に従っています。

```
┌─────────────────────────────────────────────────────────────┐
│                  ユーザーインターフェース                       │
│  ┌──────────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │   Webブラウザ     │  │   音声入力        │  │  CLIツール  │  │
│  │ (リモート/ローカル) │  │ (音声認識)       │  │ (ターミナル) │  │
│  └──────────────────┘  └─────────────────┘  └────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                   アプリケーション層                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            ninja_core (メインアプリケーション)             │ │
│  │  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐   │ │
│  │  │  NinjaAgent  │  │ Webサーバー  │  │  動作         │   │ │
│  │  │  (Gemini AI) │  │  (FastAPI)  │  │  コントローラ  │   │ │
│  │  └──────────────┘  └─────────────┘  └──────────────┘   │ │
│  │  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐   │ │
│  │  │   表情        │  │    音       │  │  距離         │   │ │
│  │  │   システム    │  │  プレイヤー   │  │  モニター      │   │ │
│  │  └──────────────┘  └─────────────┘  └──────────────┘   │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │     ハードウェア抽象化レイヤー (HAL) + 設定                 │ │
│  │         (すべてのハードウェアへの統一インターフェース)        │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    ハードウェア層                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────┐  │
│  │  pi0servo  │  │  pi0disp   │  │ pi0vl53l0x │  │pi0    │  │
│  │  (サーボ)   │  │(ディスプレイ)│  │  (センサー) │  │buzzer │  │
│  └────────────┘  └────────────┘  └────────────┘  └───────┘  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           ninja_utils (共有ユーティリティ)              │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │
                    ┌────────▼──────────┐
                    │   Raspberry Pi    │
                    │  (pigpioデーモン)  │
                    └───────────────────┘
```

### アーキテクチャの利点

1. **モジュール性** - 各層を独立して開発、テスト、アップグレードできます
2. **再利用性** - ハードウェアドライバーを他のRaspberry Piプロジェクトで使用できます
3. **保守性** - 関心事の明確な分離により、デバッグ（バグ修正）が容易になります
4. **拡張性** - 新しいドライバーライブラリを作成することで、新しいセンサーやアクチュエーター（動作装置）を追加できます
5. **テスト可能性** - 完全なハードウェアセットアップなしで、コンポーネントを個別にテストできます

---

## 📚 ライブラリの紹介

NinjaRobotV4は、責任ごとに整理された**6つのPythonパッケージ**（プログラムのまとまり）で構成されています。各ライブラリは独立してインストール可能で、組み込みシステム開発のベストプラクティスに従っています。

### 🛠️ ハードウェアライブラリ

#### **`pi0servo`** - サーボモーター制御
*校正とスムーズな補間を備えたマルチサーボ制御*

- **目的**: 最大8個のサーボモーターを同時に、正確な角度位置で制御します
- **主な機能**:
  - 個別のサーボ校正（最小/中央/最大パルス幅）
  - 位置間のスムーズな補間動作
  - スレッドセーフ（複数の処理が同時に動いても安全）な非同期制御
  - インタラクティブなTUI（テキストベースのユーザーインターフェース）校正ツール
- **CLIコマンド**:
  - `pi0servo servo <ピン> <角度>` - 単一のサーボを動かす
  - `pi0servo calib <ピン>` - インタラクティブな校正を起動
- **使用例**: ロボットの手足、頭の動き、カメラジンバル（カメラを安定させる装置）

---

#### **`pi0disp`** - ST7789Vディスプレイドライバー
*部分更新サポート付きの高性能SPIディスプレイドライバー*

- **目的**: 視覚出力のための240x240ピクセル液晶画面を制御します
- **主な機能**:
  - フルフレームおよび部分領域の更新
  - ガンマ補正（明るさ調整）と色空間変換
  - メモリプーリング（メモリの効率的な使い方）によるハードウェアアクセラレーションレンダリング
  - FPS（1秒間の画面更新回数）監視とパフォーマンス最適化
- **CLIコマンド**:
  - `pi0disp image <パス>` - 画像を表示
  - `pi0disp ball_anime` - 物理シミュレーションデモを実行
- **使用例**: 表情、ステータスインジケーター（状態表示）、センサーの可視化

---

#### **`pi0vl53l0x`** - VL53L0X距離センサー
*校正機能付きI2C ToFセンサードライバー*

- **目的**: 30mmから2000mmまでの距離を高精度で測定します
- **主な機能**:
  - シングルショット（1回だけ測定）および連続測定モード
  - オフセット補正（誤差修正）による校正
  - パフォーマンスベンチマーク（性能測定、最大50Hzサンプリング）
  - エラーハンドリング（エラー処理）とリトライロジック（再試行の仕組み）
- **CLIコマンド**:
  - `pi0vl53l0x get --count 10` - 距離測定を行う
  - `pi0vl53l0x calibrate --distance 100` - センサーを校正
- **使用例**: 障害物回避、近接検出、環境マッピング（地図作成）

---

#### **`pi0buzzer`** - パッシブブザー音生成
*PWM（パルス幅変調）による簡単な音と音楽の生成*

- **目的**: 聴覚フィードバック（音による反応）のためのトーンとメロディを再生します
- **主な機能**:
  - 周波数制御によるシングルトーン再生
  - マルチノート（複数の音）の曲シーケンス
  - 事前定義されたメロディ
  - pigpioによるハードウェアPWM
- **CLIコマンド**:
  - `pi0buzzer init <ピン>` - ブザーのGPIOピンを設定
  - `pi0buzzer beep` - テストビープを再生
  - `pi0buzzer playmusic` - メロディを再生
- **使用例**: 通知、感情音、音楽的表現

---

### 🧩 ユーティリティライブラリ

#### **`ninja_utils`** - 共有ユーティリティ
*すべてのライブラリで使用される共通ツール*

- **目的**: コードの重複を避けるために、ロギング（記録）と入力処理ユーティリティを提供します
- **主要コンポーネント**:
  - **`my_logger.py`**: 一貫したフォーマットの集中型ロギング
  - **`keyboard.py`**: インタラクティブCLIツール用のノンブロッキング（処理を止めない）キーボード入力
- **使用例**: デバッグ、インタラクティブ校正、リアルタイム制御

---

### 🎮 コアアプリケーション

#### **`ninja_core`** - メインロボットアプリケーション
*すべてのライブラリを統合した一貫性のあるロボットシステム*

- **目的**: すべてのコンポーネントを調整するロボットの「脳」
- **主要モジュール**:

  **`config.py`** - 集中型設定
  - すべてのハードウェア設定のための単一の`config.json`
  - 検証のためのPydanticモデル（データ構造の定義）
  - 個別のライブラリ設定からのインポート/エクスポート

  **`hal.py`** - ハードウェア抽象化レイヤー
  - すべてのハードウェアドライバーへの統一インターフェース
  - 共有`pigpio`接続管理
  - 安全な初期化とシャットダウンシーケンス

  **`ninja_agent.py`** - AIエージェント
  - NLP（自然言語処理）のためのGoogle Gemini統合
  - 意味理解と意図マッピング
  - 自動感情生成
  - Web検索機能
  - 多言語サポート（日本語/英語/繁体字中国語/簡体字中国語）

  **`movement_controller.py`** - モーションシステム
  - 補間を使ったマルチサーボの振り付け
  - 名前付き動作シーケンス
  - 障害物検出時の緊急停止

  **`facial_expressions.py`** - 視覚的感情
  - プログラムによる顔の描画（嬉しい、悲しいなど）
  - スレッド化されたアニメーションエンジン
  - 自動アイドル/話し中状態

  **`robot_sound.py`** - 聴覚フィードバック
  - 感情に合わせた音シーケンス
  - 表情と同期

  **`perception.py`** - 距離監視
  - 連続センシングのためのバックグラウンドスレッド（裏で動く処理）
  - スレッドセーフな距離クエリ（問い合わせ）

  **`web_server.py`** - Webインターフェース
  - FastAPI REST API（Webアプリを作るための仕組み）
  - リアルタイムデータのためのWebSocket（双方向通信）
  - リモートアクセスのためのngrok統合
  - QRコード生成

- **CLIコマンド**:
  - `ninja_core server` - Webインターフェースを起動
  - `ninja_core chat` - ターミナルでインタラクティブAIチャット
  - `ninja_core movement-tool` - 動作を記録および編集
  - `ninja_core config import-all` - ハードウェア設定をインポート
  - `ninja_core config set-key gemini <キー>` - AI APIキーを設定

---

## 🚀 はじめに

### クイックインストール

```bash
# リポジトリをクローン（コピー）
git clone https://github.com/Nilcreator/NinjaRobotV4.git
cd NinjaRobotV4

# 1つのコマンドですべてをインストール
uv pip install -e .

# APIキーを設定
ninja_core config set-key gemini あなたのGEMINI_APIキー

# ハードウェアを校正（画面の指示に従ってください）
ninja_core config import-all

# ロボットのWebサーバーを起動
ninja_core server
```

詳細な手順については、**[インストールガイド](InstallationGuide.md)**をご覧ください。

### ドキュメント

- **[インストールガイド](InstallationGuide.md)** - 初心者向けの完全なセットアップ手順
- **[開発ログ](DevelopmentLog.md)** - 詳細な開発履歴とバグ修正
- **[再構築ガイド](ReconstructionGuide.md)** - 技術的な設計決定とアーキテクチャ
- **[ninja_core README](ninja_core/README.md)** - 開発者向けドキュメントとAPIリファレンス

---

## 📊 現在の状況

**Webサーバーとリモートアクセス**モジュールが正常に実装されました。ロボットは現在、任意のデバイスから完全な制御と対話を可能にするFastAPIベースのWebインターフェースをホストしています。

**完了した機能:**
- ✅ すべてのハードウェアライブラリ（`pi0servo`、`pi0disp`、`pi0buzzer`、`pi0vl53l0x`、`ninja_utils`）
- ✅ ハードウェア抽象化レイヤー（HAL）
- ✅ 集中型設定システム
- ✅ Gemini 2.5 Flash統合のAIエージェント
- ✅ 多言語サポート（4言語）
- ✅ 音声とテキスト入力を備えたWebサーバー
- ✅ QRコード付きngrok経由のリモートアクセス
- ✅ WebSocket経由のリアルタイム距離監視
- ✅ 障害物回避安全システム
- ✅ 表情と感情音
- ✅ 補間動作を備えたモーションシステム

**以前のマイルストーン:**
- **AIエージェント**（`ninja_agent.py`）が、ニュアンスのある意味理解、多言語コミュニケーション、リアルタイムWeb検索で正常に実装されました
- **モーションシステム**（`movement_controller.py`）がHAL統合で移植および再構築されました
- すべてのコアモジュール（`perception.py`、`robot_sound.py`、`facial_expressions.py`）が統合およびテストされました
- すべての基礎ハードウェアライブラリが完成し、検証されました

---

## 📄 ライセンス

このプロジェクトは**MITライセンス**の下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。

**Copyright © 2025 Chihkuang Chang**

ハードウェアライブラリ`pi0servo`、`pi0disp`、`pi0vl53l0x`は**Tanibayashi Yoichi**との共著です。

---

## 🤝 貢献

貢献を歓迎します！これは教育プロジェクトであり、以下を奨励します:
- GitHub Issuesを介したバグレポートと機能リクエスト
- プルリクエストを介したコード貢献
- ドキュメントの改善
- 教育資料とチュートリアル
- ハードウェアの改造と代替設計

---

## 🙏 謝辞

- **Google Gemini** - 強力でアクセスしやすいAI機能を提供してくれたことに感謝
- **ngrok** - リモートアクセスを簡素化してくれたことに感謝
- **Raspberry Pi Foundation** - 手頃で有能なハードウェアを作成してくれたことに感謝
- オープンソースコミュニティ - Pythonライブラリとハードウェアドライバーのために

---

<div align="center">

**ロボット教育と研究のために❤️を込めて構築**

[インストールガイド](InstallationGuide.md) • [ドキュメント](ninja_core/README.md) • [GitHub](https://github.com/Nilcreator/NinjaRobotV4)

</div>
