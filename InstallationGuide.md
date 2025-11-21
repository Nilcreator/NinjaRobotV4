# NinjaRobotV4 Complete Installation Guide

This guide will walk you through every step needed to build and run your NinjaRobotV4 on a Raspberry Pi Zero 2W. No programming experience is required—just follow each step carefully.

---

## Table of Contents

1. [Hardware Requirements](#1-hardware-requirements)
2. [Hardware Wiring Guide](#2-hardware-wiring-guide)
3. [Raspberry Pi OS Installation](#3-raspberry-pi-os-installation)
4. [Software Installation](#4-software-installation)
5. [Service Setup (Gemini AI & ngrok)](#5-service-setup-gemini-ai--ngrok)
6. [Project Installation](#6-project-installation)
7. [Hardware Calibration](#7-hardware-calibration)
8. [Function Testing](#8-function-testing)
9. [Running the Robot](#9-running-the-robot)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Hardware Requirements

### Required Components

- **Raspberry Pi Zero 2W** (with headers soldered)
- **MicroSD Card** (16GB or larger, Class 10 recommended)
- **Power Supply** (5V 2.5A USB-C or Micro-USB)
- **8x Servo Motors** (SG90 or similar, 5V)
- **External 5V Power Supply** for servos (recommended: 5V 3A or higher)
- **ST7789V LCD Display** (240x240 pixels, SPI interface)
- **VL53L0X Distance Sensor** (Time-of-Flight, I2C interface)
- **Passive Buzzer** (3-5V)
- **Jumper Wires** (Male-to-Female and Male-to-Male)
- **Breadboard** (optional, for prototyping)
- **Keyboard, Mouse, and Monitor** (for initial setup)

### Optional but Recommended

- **Raspberry Pi Case**
- **Heatsinks** for the Raspberry Pi
- **USB Hub** (if you need multiple USB devices during setup)

---

## 2. Hardware Wiring Guide

### Important Safety Notes

> [!CAUTION]
> - **Always power off** the Raspberry Pi before connecting or disconnecting components.
> - **Never connect servo power** directly to the Raspberry Pi's 5V pin—use an external power supply.
> - **Double-check all connections** before powering on to avoid damage.

### GPIO Pin Layout

Here's the complete wiring diagram for all components:

```
Raspberry Pi Zero 2W GPIO Pinout (40-pin header)
┌─────────────────────────────────────┐
│  3.3V  [1] [2]  5V                  │
│  SDA   [3] [4]  5V                  │
│  SCL   [5] [6]  GND                 │
│  GPIO4 [7] [8]  GPIO14 (TXD)        │
│  GND   [9] [10] GPIO15 (RXD)        │
│  SPI0 SCLK [11] [12] GPIO18 (DC)    │  ← Display DC
│  GPIO27[13] [14] GND                │
│  GPIO22[15] [16] GPIO23             │
│  3.3V [17] [18] GPIO24              │
│  SPI0 MOSI [19] [20] GND            │
│  GPIO9[21] [22] GPIO25              │
│  SPI0 SCLK [23] [24] SPI0 CE0       │
│  GND  [25] [26] SPI0 CE1            │
│  ID_SD[27] [28] ID_SC               │
│  GPIO5[29] [30] GND                 │
│  GPIO6[31] [32] GPIO12              │
│  GPIO13[33] [34] GND                │
│  GPIO19[35] [36] GPIO16             │  ← Display RST (19)
│  GPIO26[37] [38] GPIO20             │  ← Buzzer (26), Display BLK (20)
│  GND  [39] [40] GPIO21              │
└─────────────────────────────────────┘
```

### Component Connection Table

#### Servo Motors (8 servos)

| Servo # | GPIO Pin | Signal Wire | Power (5V) | Ground |
|---------|----------|-------------|------------|--------|
| 1       | GPIO 5   | Orange/Yellow | External 5V | Common GND |
| 2       | GPIO 17  | Orange/Yellow | External 5V | Common GND |
| 3       | GPIO 21  | Orange/Yellow | External 5V | Common GND |
| 4       | GPIO 22  | Orange/Yellow | External 5V | Common GND |
| 5       | GPIO 23  | Orange/Yellow | External 5V | Common GND |
| 6       | GPIO 24  | Orange/Yellow | External 5V | Common GND |
| 7       | GPIO 25  | Orange/Yellow | External 5V | Common GND |
| 8       | GPIO 27  | Orange/Yellow | External 5V | Common GND |

> [!IMPORTANT]
> **Servo Power:** Connect all servo power wires (red) to your external 5V power supply (NOT the Raspberry Pi). Connect all servo ground wires (brown/black) to a common ground that is also connected to one of the Raspberry Pi's GND pins (e.g., Pin 6, 9, 14, 20, 25, 30, 34, or 39).

#### ST7789V LCD Display (SPI)

| Display Pin | Raspberry Pi Pin | Description |
|-------------|------------------|-------------|
| VCC         | Pin 17 (3.3V)    | Power       |
| GND         | Pin 14 (GND)     | Ground      |
| SCL (CLK)   | Pin 23 (GPIO 11 - SPI0 SCLK) | SPI Clock |
| SDA (MOSI)  | Pin 19 (GPIO 10 - SPI0 MOSI) | SPI Data  |
| DC          | Pin 12 (GPIO 18) | Data/Command |
| RST         | Pin 35 (GPIO 19) | Reset       |
| BLK         | Pin 38 (GPIO 20) | Backlight   |

#### VL53L0X Distance Sensor (I2C)

| Sensor Pin | Raspberry Pi Pin | Description |
|------------|------------------|-------------|
| VCC        | Pin 1 (3.3V)     | Power       |
| GND        | Pin 6 (GND)      | Ground      |
| SCL        | Pin 5 (GPIO 3 - I2C SCL) | I2C Clock |
| SDA        | Pin 3 (GPIO 2 - I2C SDA) | I2C Data  |

#### Passive Buzzer

| Buzzer Pin | Raspberry Pi Pin | Description |
|------------|------------------|-------------|
| Positive (+) | Pin 37 (GPIO 26) | Signal    |
| Negative (-) | Pin 39 (GND)     | Ground    |

### Wiring Checklist

Before proceeding, verify:
- [ ] All servo signal wires are connected to the correct GPIO pins
- [ ] Servo power comes from an external 5V supply (NOT the Pi)
- [ ] Common ground is shared between Pi and external servo power supply
- [ ] Display is connected via SPI (pins 19, 23, 12, 35, 38)
- [ ] Distance sensor is connected via I2C (pins 3, 5)
- [ ] Buzzer is connected to GPIO 26
- [ ] No loose wires or short circuits

---

## 3. Raspberry Pi OS Installation

### Step 3.1: Download Raspberry Pi Imager

1. On your computer, go to: https://www.raspberrypi.com/software/
2. Download **Raspberry Pi Imager** for your operating system (Windows, macOS, or Linux)
3. Install and open the Raspberry Pi Imager

### Step 3.2: Flash the OS to MicroSD Card

1. Insert your MicroSD card into your computer (use an adapter if needed)
2. In Raspberry Pi Imager:
   - Click **"Choose Device"** → Select **"Raspberry Pi Zero 2W"**
   - Click **"Choose OS"** → Select **"Raspberry Pi OS (64-bit)"** (recommended) or **"Raspberry Pi OS (32-bit)"**
   - Click **"Choose Storage"** → Select your MicroSD card

3. Click the **Settings (gear icon)** button to configure:
   - **Hostname**: `ninjarobot` (or your preferred name)
   - **Enable SSH**: Check this box and select "Use password authentication"
   - **Set username and password**: 
     - Username: `pi` (or your choice)
     - Password: (create a secure password)
   - **Configure WiFi** (if you want wireless):
     - SSID: Your WiFi network name
     - Password: Your WiFi password
     - Wireless LAN country: Select your country
   - **Set locale settings**: Choose your timezone and keyboard layout

4. Click **"SAVE"** to save settings
5. Click **"WRITE"** to flash the OS to the card
6. Wait for the process to complete (this may take 5-10 minutes)
7. When done, safely eject the MicroSD card

### Step 3.3: Boot the Raspberry Pi

1. Insert the MicroSD card into your Raspberry Pi Zero 2W
2. Connect your keyboard, mouse, and monitor (via HDMI adapter)
3. Connect the power supply
4. Wait for the Pi to boot (first boot may take 2-3 minutes)
5. Log in with the username and password you set earlier

---

## 4. Software Installation

### Step 4.1: Update System

Open a terminal and run:

```bash
sudo apt update && sudo apt upgrade -y
```

This may take 10-20 minutes depending on your internet speed.

### Step 4.2: Enable Required Interfaces

1. Open the Raspberry Pi configuration tool:
   ```bash
   sudo raspi-config
   ```

2. Navigate to **"3 Interface Options"**

3. Enable the following:
   - **I2C**: Select **"I5 I2C"** → **"Yes"**
   - **SPI**: Select **"I4 SPI"** → **"Yes"**

4. Select **"Finish"** and reboot when prompted:
   ```bash
   sudo reboot
   ```

### Step 4.3: Install System Dependencies

After reboot, open a terminal and install required packages:

```bash
sudo apt install -y git pigpio python3-pip
```

### Step 4.4: Install Python Package Manager (uv)

We use `uv` for faster and more reliable Python package management:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, close and reopen your terminal, or run:

```bash
source $HOME/.cargo/env
```

Verify installation:

```bash
uv --version
```

You should see a version number like `uv 0.x.x`.

### Step 4.5: Start pigpio Daemon

The `pigpio` daemon must run in the background for hardware control:

```bash
sudo pigpiod
```

> [!TIP]
> To make `pigpiod` start automatically on boot, run:
> ```bash
> sudo systemctl enable pigpiod
> sudo systemctl start pigpiod
> ```

---

## 5. Service Setup (Gemini AI & ngrok)

### Step 5.1: Create Google Gemini API Key

The robot uses Google's Gemini AI for natural language understanding.

1. **Go to Google AI Studio**: https://aistudio.google.com/
2. **Sign in** with your Google account
3. Click **"Get API Key"** in the left sidebar
4. Click **"Create API Key"**
5. Select **"Create API key in new project"** or choose an existing project
6. **Copy the API key** that appears (it looks like: `AIzaSy...`)
7. **Save this key** somewhere safe—you'll need it later

> [!WARNING]
> Keep your API key private! Do not share it publicly or commit it to version control.

### Step 5.2: Create ngrok Account

`ngrok` creates a public URL so you can control your robot from anywhere.

1. **Go to ngrok**: https://ngrok.com/
2. Click **"Sign up"** and create a free account
3. After signing in, go to: https://dashboard.ngrok.com/get-started/your-authtoken
4. **Copy your Authtoken** (it looks like: `2a...`)
5. **Save this token**—you'll enter it when you first start the robot's web server

---

## 6. Project Installation

### Step 6.1: Clone the Repository

Navigate to your home directory and clone the project:

```bash
cd ~
git clone https://github.com/Nilcreator/NinjaRobotV4.git
cd NinjaRobotV4
```

> [!NOTE]
> If the repository is private or you're using a different source, adjust the URL accordingly.

### Step 6.2: Install All Dependencies

This single command installs everything you need:

```bash
uv pip install -e .
```

This will:
- Install all Python dependencies
- Set up all the robot's libraries in editable mode
- Make all CLI commands available

The installation may take 5-10 minutes.

### Step 6.3: Verify Installation

Check that the main command is available:

```bash
ninja_core --help
```

You should see a list of available commands like `chat`, `server`, `config`, etc.

---

## 7. Hardware Calibration

Before running the robot, you need to calibrate the servos and configure the hardware.

### Step 7.1: Configure Buzzer

Tell the system which GPIO pin the buzzer is connected to:

```bash
cd ~/NinjaRobotV4/pi0buzzer
uv run pi0buzzer init 26
```

Test the buzzer:

```bash
uv run pi0buzzer beep
```

You should hear a short beep.

### Step 7.2: Test Distance Sensor

Return to the project root:

```bash
cd ~/NinjaRobotV4
```

Test the sensor:

```bash
uv run pi0vl53l0x get --count 5 --interval 1.0
```

You should see 5 distance readings in millimeters.

### Step 7.3: Calibrate Servos

Each servo needs to be calibrated to define its minimum, center, and maximum positions.

For each servo (example for GPIO 17):

```bash
uv run pi0servo calib 17
```

Follow the on-screen instructions:
1. Press `v` to select **Min** position
2. Use **Up/Down** arrow keys for large adjustments, **w/s** for fine-tuning
3. When the servo is at its minimum position, press **Enter** to save
4. Press `c` to select **Center** position, adjust, and press **Enter**
5. Press `x` to select **Max** position, adjust, and press **Enter**
6. Press `q` to quit

**Repeat this for all 8 servos** (GPIO pins: 5, 17, 21, 22, 23, 24, 25, 27)

### Step 7.4: Import Hardware Configuration

After calibrating all servos, import the configurations:

```bash
uv run ninja_core config import-all
```

You should see:
```
Found servo config at 'servo.json'. Importing...
Found buzzer config at 'buzzer.json'. Importing...
Configuration updated and saved to config.json!
```

### Step 7.5: Set Gemini API Key

Configure the AI agent with your API key (replace `YOUR_API_KEY` with the actual key):

```bash
uv run ninja_core config set-key gemini YOUR_API_KEY
```

---

## 8. Function Testing

Now let's test each component individually.

### Test 8.1: Display Test

Test the LCD screen with an image:

```bash
uv run pi0disp image assets/images/sample_face.jpg
```

You should see an image on the display with changing brightness.

Test animation:

```bash
uv run pi0disp ball_anime --num-balls 5
```

Press **Ctrl+C** to stop.

### Test 8.2: Servo Movement Test

Move a servo to its center position:

```bash
uv run pi0servo servo 17 center
```

The servo on GPIO 17 should move to 0 degrees.

Try other positions:

```bash
uv run pi0servo servo 17 45
uv run pi0servo servo 17 -45
uv run pi0servo servo 17 max
```

### Test 8.3: Sound Test

Play a melody:

```bash
uv run pi0buzzer playmusic
```

### Test 8.4: Distance Sensor Performance

Measure sensor speed:

```bash
uv run pi0vl53l0x performance --count 100
```

### Test 8.5: AI Agent Test (Text Chat)

Test the AI chat in terminal mode:

```bash
uv run ninja_core chat
```

Try these commands:
- `Hello` (the robot should greet you)
- `Show me a happy face` (displays happy expression and sound)
- `こんにちは` (responds in Japanese)
- `你好` (responds in Chinese)
- Type `quit` or press **Ctrl+C** to exit

> [!NOTE]
> The robot will monitor distance continuously and react if you get too close (<50mm).

---

## 9. Running the Robot

### Start the Web Server

This is the main way to interact with your robot:

```bash
uv run ninja_core server
```

On **first run**, you'll be prompted to enter your **ngrok authtoken** (from Step 5.2). Paste it and press Enter.

The robot will:
1. Initialize all hardware
2. Start the web server
3. Create a public URL via ngrok
4. Display a QR code on its screen

### Access the Web Interface

You have two options:

#### Option A: Scan the QR Code (Recommended)

Use your smartphone to scan the QR code displayed on the robot's screen. This will open the web interface in your phone's browser.

#### Option B: Local Network

On any device on the same WiFi network, open a browser and go to:
```
http://ninjarobot.local:8000
```
(Replace `ninjarobot` with your hostname if different)

### Web Interface Features

Once connected, you can:

1. **Chat with the Robot**:
   - Type messages in the text box
   - Or click the **microphone icon** and speak (select language first)
   - The robot will respond in the same language

2. **Control Servos**:
   - Select a movement from the dropdown
   - Click **Execute**

3. **Show Facial Expressions**:
   - Select an expression (happy, sad, etc.)
   - Click **Show**

4. **Play Sounds**:
   - Select an emotion sound
   - Click **Play**

5. **Monitor Distance**:
   - Real-time distance readings appear at the top

### Supported Languages

- **English** (en-US)
- **日本語** (ja-JP) - Japanese
- **繁體中文** (zh-TW) - Traditional Chinese
- **简体中文** (zh-CN) - Simplified Chinese

### Stopping the Server

Press **Ctrl+C** in the terminal to stop the server. The robot will safely shut down all hardware.

---

## 10. Troubleshooting

### Problem: "Could not connect to pigpiod daemon"

**Solution**:
```bash
sudo pigpiod
```

Then try running your command again.

### Problem: Display not working

**Checks**:
1. Verify SPI is enabled: `sudo raspi-config` → Interface Options → SPI
2. Check wiring matches the pin table in Section 2
3. Reboot: `sudo reboot`

### Problem: Distance sensor not responding

**Checks**:
1. Verify I2C is enabled: `sudo raspi-config` → Interface Options → I2C
2. Check if sensor is detected:
   ```bash
   sudo i2cdetect -y 1
   ```
   You should see `29` or `52` in the output
3. Check wiring (VCC to 3.3V, not 5V)

### Problem: Servos not moving

**Checks**:
1. Ensure external 5V power supply is connected and turned on
2. Verify common ground between Pi and servo power supply
3. Check servo signal wire connections
4. Recalibrate servo: `uv run pi0servo calib <PIN>`

### Problem: "ImportError" or "ModuleNotFoundError"

**Solution**:
Reinstall the project:
```bash
cd ~/NinjaRobotV4
uv pip install -e . --force-reinstall
```

### Problem: Web server won't start

**Checks**:
1. Ensure port 8000 is not already in use
2. Check if ngrok authtoken is set correctly
3. Restart the server with verbose output:
   ```bash
   uv run ninja_core server --log-level debug
   ```

### Problem: AI agent not responding

**Checks**:
1. Verify Gemini API key is set:
   ```bash
   cat config.json | grep gemini
   ```
2. Check internet connection
3. Re-set API key:
   ```bash
   uv run ninja_core config set-key gemini YOUR_KEY
   ```

### Getting More Help

If you encounter issues not covered here:

1. Check the project's GitHub Issues page
2. Review the `DevelopmentLog.md` for known issues and fixes
3. Ensure all wiring matches the diagrams exactly
4. Try running individual component tests (Section 8) to isolate the problem

---

## Next Steps

- **Record Custom Movements**: Use `uv run ninja_core movement-tool` to create and save servo choreography
- **Customize Behavior**: Edit `config.json` to adjust settings
- **Build an Enclosure**: Design a robot body and mount all components
- **Explore the Code**: Check `ninja_core/README.md` for developer documentation

**Congratulations!** Your NinjaRobotV4 is now ready to use. Enjoy exploring and experimenting with your AI-powered robot! 🤖
