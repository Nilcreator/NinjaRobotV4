# NinjaRobotV3 Code Specification

This document provides a detailed, code-level specification of the entire NinjaRobotV3 project, including file structures, imported libraries, and detailed descriptions of every function and method.

## 1. Project File Structure

```
/
├── pi0ninja_v3/
│   └── src/pi0ninja_v3/
│       ├── __init__.py
│       ├── detect_distance.py
│       ├── facial_expressions.py
│       ├── movement_recorder.py
│       ├── ninja_agent.py
│       ├── robot_sound.py
│       ├── show_faces.py
│       └── web_server.py
├── piservo0/
│   └── piservo0/
│       ├── __init__.py
│       ├── __main__.py
│       ├── command/
│       │   ├── cmd_apiclient.py
│       │   ├── cmd_calib.py
│       │   ├── cmd_servo.py
│       │   └── cmd_strclient.py
│       ├── core/
│       │   ├── calibrable_servo.py
│       │   ├── multi_servo.py
│       │   └── piservo.py
│       └── helper/
│           ├── str_cmd_to_json.py
│           └── thread_multi_servo.py
├── pi0disp/
│   └── src/pi0disp/
│       ├── __init__.py
│       ├── __main__.py
│       ├── commands/
│       │   ├── ball_anime.py
│       │   ├── image.py
│       │   └── off.py
│       ├── disp/
│       │   └── st7789v.py
│       └── utils/
│           ├── performance_core.py
│           └── sprite.py
├── pi0buzzer/
│   └── src/pi0buzzer/
│       ├── __init__.py
│       ├── __main__.py
│       └── driver.py
└── vl53l0x_pigpio/
    └── src/vl53l0x_pigpio/
        ├── __init__.py
        ├── __main__.py
        ├── click_utils.py
        ├── config_manager.py
        ├── constants.py
        └── driver.py
```

---

## 2. Library: `pi0ninja_v3`

This is the main application that integrates all other hardware libraries and provides the user-facing web interface and AI agent.

### File: `pi0ninja_v3/src/pi0ninja_v3/detect_distance.py`

**Imported Libraries:**
- `pigpio`, `time`, `sys`, `select`, `termios`, `tty`, `os`, `vl53l0x_pigpio`

**Classes:**

#### `DistanceDetector`
- **Description:** A class to detect distance using the VL53L0X sensor.
- **Methods:**
    - `__init__(self)`: Initializes the pigpio connection.
    - `timed_detection(self, count: int, delay: float)`: Performs a specified number of distance measurements with a delay.
    - `continuous_detection(self)`: Performs continuous distance measurement at 5Hz until 'q' is pressed.
    - `cleanup(self)`: Stops the pigpio connection.

### File: `pi0ninja_v3/src/pi0ninja_v3/facial_expressions.py`

**Imported Libraries:**
- `time`, `math`, `threading`, `PIL` (Image, ImageDraw, ImageFont), `pi0disp`

**Classes:**

#### `AnimatedFaces`
- **Description:** Generates and displays programmatically drawn, animated facial expressions. This class is thread-safe.
- **Methods:**
    - `__init__(self, lcd: ST7789V)`: Initializes the face controller with an LCD instance.
    - `stop(self)`: Stops the current animation thread.
    - `play_idle(self, duration_s=float('inf'))`: Displays a blinking idle face.
    - `play_happy(self, duration_s=3)`: Displays a happy face.
    - `play_sad(self, duration_s=3)`: Displays a sad face.
    - `play_angry(self, duration_s=3)`: Displays an angry face.
    - `play_surprising(self, duration_s=3)`: Displays a surprised face.
    - `play_sleepy(self, duration_s=3)`: Displays a sleepy face.
    - `play_speaking(self, duration_s=3)`: Displays a speaking animation.
    - `play_shy(self, duration_s=3)`: Displays a shy face.
    - `play_cry(self, duration_s=3)`: Displays a crying face.
    - `play_laughing(self, duration_s=3)`: Displays a laughing face.
    - `play_embarrassing(self, duration_s=3)`: Displays an embarrassed face.
    - `play_scary(self, duration_s=3)`: Displays a scary face.
    - `play_exciting(self, duration_s=3)`: Displays an excited face.
    - `play_confusing(self, duration_s=3)`: Displays a confused face.

### File: `pi0ninja_v3/src/pi0ninja_v3/movement_recorder.py`

**Imported Libraries:**
- `json`, `os`, `time`, `pigpio`, `sys`, `select`, `termios`, `tty`, `copy`, `piservo0`

**Classes:**

#### `ServoController`
- **Description:** A custom controller to manage multiple servos based on `servo.json`.
- **Methods:**
    - `__init__(self)`: Initializes servos from the config file.
    - `move_servos(self, movements, speed='M')`: Executes a set of servo movements with smooth interpolation.
    - `get_current_angles(self)`: Returns a dictionary of current servo angles.
    - `center_all_servos(self)`: Moves all servos to their center position.
    - `cleanup(self)`: Turns off all servos.

**Functions:**
- `load_movements()`: Loads movement sequences from `servo_movement.json`.
- `save_movements(movements)`: Saves movement sequences to `servo_movement.json`.
- `parse_movement_command(command_str, definitions)`: Parses a user's command string into a speed and a dictionary of movements.
- `record_new_movement(controller)`: Handles the UI for recording a new movement sequence.
- `execute_movement(controller)`: Handles the UI for executing a saved movement.
- `modify_existing_movement(controller)`: Handles the non-destructive modification of a movement sequence.
- `clear_movement(controller)`: Handles the UI for deleting a movement sequence.

### File: `pi0ninja_v3/src/pi0ninja_v3/ninja_agent.py`

**Imported Libraries:**
- `os`, `json`, `time`, `google.generativeai`, `googlesearch`

**Classes:**

#### `NinjaAgent`
- **Description:** The AI agent for the NinjaRobot that handles text and audio-based conversations.
- **Methods:**
    - `__init__(self, api_key: str)`: Initializes the Gemini model and defines the system prompt.
    - `web_search(self, query: str)`: Performs a web search using the `googlesearch` library.
    - `process_command(self, user_input: str)`: Processes a text-based user command and returns an action plan.
    - `process_audio_command(self, audio_file_path: str)`: Processes a voice command from an audio file.

### File: `pi0ninja_v3/src/pi0ninja_v3/robot_sound.py`

**Imported Libraries:**
- `pigpio`, `time`, `json`, `os`, `sys`, `pi0buzzer`

**Classes:**

#### `RobotSoundPlayer`
- **Description:** A class to play sounds corresponding to robot emotions using a buzzer.
- **Methods:**
    - `__init__(self)`: Initializes the buzzer from the `buzzer.json` config.
    - `play(self, emotion: str)`: Plays the sound for the given emotion.
    - `cleanup(self)`: Cleans up pigpio resources.

### File: `pi0ninja_v3/src/pi0ninja_v3/web_server.py`

**Imported Libraries:**
- `socket`, `uvicorn`, `json`, `os`, `pigpio`, `inspect`, `time`, `shutil`, `tempfile`, `asyncio`, `pyngrok`, `fastapi`, `pydantic`, `dotenv`, `qrcode`

**Functions:**
- `lifespan(app: FastAPI)`: Async context manager to handle hardware initialization on startup and cleanup on shutdown.
- `handle_first_interaction(request: Request)`: Switches the display from the QR code to the idle face on the first user interaction.
- `execute_robot_actions(request: Request, action_plan: dict)`: Executes the physical actions (face, sound, movement) planned by the AI agent.

**API Endpoints:**
- `GET /api/agent/status`: Returns the status of the AI agent.
- `POST /api/agent/set_api_key`: Sets the Gemini API key.
- `POST /api/agent/chat`: Sends a text message to the AI agent.
- `POST /api/agent/chat_voice`: Sends a voice message (audio file) to the AI agent.
- `GET /api/servos/movements`: Returns a list of available servo movements.
- `POST /api/servos/movements/{movement_name}/execute`: Executes a servo movement.
- `GET /api/display/expressions`: Returns a list of available facial expressions.
- `POST /api/display/expressions/{expression_name}`: Displays a facial expression.
- `GET /api/sound/emotions`: Returns a list of available emotion sounds.
- `POST /api/sound/emotions/{emotion_name}`: Plays an emotion sound.
- `GET /api/sensor/distance`: Returns the current distance from the sensor.
- `WS /ws/distance`: Streams the distance sensor data via WebSocket.

---

## 3. Library: `piservo0`

A library for controlling servo motors with calibration capabilities.

### File: `piservo0/piservo0/core/piservo.py`

**Classes:**

#### `PiServo`
- **Description:** The most basic class for controlling a single servo motor using `pigpio`.
- **Methods:**
    - `__init__(self, pi, pin, debug=False)`: Initializes the servo on a specific GPIO pin.
    - `get_pulse(self)`: Returns the current pulse width of the servo.
    - `move_pulse(self, pulse)`: Moves the servo to a specific pulse width.
    - `move_min(self)` / `move_max(self)` / `move_center(self)`: Moves the servo to predefined positions.
    - `off(self)`: Stops sending pulses to the servo.

### File: `piservo0/piservo0/core/calibrable_servo.py`

**Classes:**

#### `CalibrableServo`
- **Inherits from:** `PiServo`
- **Description:** Extends `PiServo` with calibration functionality, allowing for the adjustment of min, center, and max pulse widths.
- **Methods:**
    - `__init__(self, pi, pin, conf_file, debug=False)`: Initializes the servo and loads calibration from a config file.
    - `move_angle(self, deg)`: Moves the servo to a specific angle (-90 to 90).
    - `get_angle(self)`: Returns the current angle of the servo.
    - `load_conf(self)` / `save_conf(self)`: Loads/saves calibration data.

### File: `piservo0/piservo0/core/multi_servo.py`

**Classes:**

#### `MultiServo`
- **Description:** A class to control multiple `CalibrableServo` objects simultaneously.
- **Methods:**
    - `__init__(self, pi, pins, ...)`: Initializes a group of servos.
    - `move_all_angles(self, target_angles)`: Moves all servos to their respective target angles instantly.
    - `move_all_angles_sync(self, target_angles, move_sec, step_n)`: Moves all servos to their target angles synchronously and smoothly over a specified duration.

### File: `piservo0/piservo0/helper/thread_multi_servo.py`

**Classes:**

#### `ThreadMultiServo`
- **Description:** A thread-safe wrapper around `MultiServo` that executes commands asynchronously in a separate worker thread.
- **Methods:**
    - `__init__(self, pi, pins, ...)`: Initializes the `MultiServo` instance and starts the worker thread.
    - `send_cmd(self, cmd: dict)`: Sends a command dictionary to the worker thread's queue.
    - `move_all_angles_sync(self, target_angles, ...)`: Sends a command to move all servos synchronously.
    - `end(self)`: Stops the worker thread and cleans up resources.

---

## 4. Library: `pi0disp`

A high-performance display driver for ST7789V-based screens.

### File: `pi0disp/src/pi0disp/disp/st7789v.py`

**Classes:**

#### `ST7789V`
- **Description:** An optimized driver for ST7789V-based SPI displays.
- **Methods:**
    - `__init__(self, channel, rst_pin, ...)`: Initializes the display hardware.
    - `set_rotation(self, rotation)`: Sets the display rotation.
    - `display(self, image: Image.Image)`: Displays a full PIL Image on the screen.
    - `display_region(self, image, x0, y0, x1, y1)`: Displays a portion of an image within a specified region for partial updates.
    - `sleep(self)` / `wake(self)`: Puts the display to sleep or wakes it up.
    - `close(self)`: Cleans up resources.

### File: `pi0disp/src/pi0disp/utils/performance_core.py`

**Classes:**
- `MemoryPool`: Manages a pool of reusable memory buffers to reduce garbage collection overhead.
- `RegionOptimizer`: Merges overlapping or nearby rectangular regions to reduce the number of drawing operations.
- `ColorConverter`: Provides fast color space conversion utilities (e.g., RGB to RGB565) using cached lookup tables.

---

## 5. Library: `pi0buzzer`

A simple driver for controlling a buzzer.

### File: `pi0buzzer/src/pi0buzzer/driver.py`

**Classes:**

#### `Buzzer`
- **Description:** A class to control a passive buzzer.
- **Methods:**
    - `__init__(self, pi, pin, ...)`: Initializes the buzzer on a specific GPIO pin.
    - `play_sound(self, frequency, duration)`: Plays a sound with a given frequency and duration.
    - `off(self)`: Stops the sound.

#### `MusicBuzzer`
- **Inherits from:** `Buzzer`
- **Description:** Extends `Buzzer` with the ability to play pre-defined songs or be controlled via keyboard input.
- **Methods:**
    - `play_song(self, song)`: Plays a song defined as a list of notes and durations.
    - `play_music(self)`: Starts an interactive mode to play music with the computer keyboard.

---

## 6. Library: `vl53l0x_pigpio`

A Python driver for the VL53L0X Time-of-Flight distance sensor.

### File: `vl53l0x_pigpio/src/vl53l0x_pigpio/driver.py`

**Classes:**

#### `VL53L0X`
- **Description:** A driver for the VL53L0X distance sensor using `pigpio` for I2C communication.
- **Methods:**
    - `__init__(self, pi, i2c_bus, ...)`: Initializes the sensor on the specified I2C bus.
    - `get_range(self)`: Performs a single distance measurement and returns the result in millimeters.
    - `set_offset(self, offset_mm)`: Sets a calibration offset for the distance measurements.
    - `calibrate(self, target_distance_mm, num_samples)`: Calculates the required offset based on a known target distance.
    - `close(self)`: Closes the I2C connection.