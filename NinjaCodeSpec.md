# NinjaCodeSpec.md

## File Structure

```
/
├── assets/
│   ├── angry.jpg
│   └── face_expression.jpg
├── buzzer.json
├── GEMINI.md
├── InstallationGuide.md
├── main_robot_control.py
├── ngrok
├── ngrok.zip
├── NinjaDevGuide.md
├── NinjaUserGuide.md
├── pi0buzzer/
│   ├── buzzer.json
│   ├── implementation.md
│   ├── pyproject.toml
│   ├── README.md
│   ├── src/
│   │   └── pi0buzzer/
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       └── driver.py
│   └── uv.lock
├── pi0disp/
│   ├── .gitignore
│   ├── .python-version
│   ├── docs/
│   │   ├── ImageProcessor_usage.md
│   │   ├── pi0disp-test3.mp4
│   │   ├── PXL_20250820_192440131.jpg
│   │   ├── PXL_20250820_195152207.jpg
│   │   ├── samples
│   │   └── ST7789V.pdf
│   ├── GEMINI.md
│   ├── LICENSE
│   ├── Memo.md
│   ├── pyproject.toml
│   ├── README.md
│   ├── samples/
│   │   ├── basic_usage.py
│   │   ├── faces/
│   │   │   ├── 155542.png
│   │   │   ├── 155650.png
│   │   │   ├── 155722.png
│   │   │   ├── 155802.png
│   │   │   ├── 155904.png
│   │   │   ├── 155943.png
│   │   │   └── 160023.png
│   │   ├── my_photo.jpg
│   │   ├── robot_face1.py
│   │   ├── robot_face2.py
│   │   └── sprite_usage.py
│   ├── src/
│   │   └── pi0disp/
│   │       ├── 20250821a-Claude.ai/
│   │       │   ├── modular_architecture_doc.md
│   │       │   └── optimization_summary.md
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       ├── commands/
│   │       │   ├── __init__.py
│   │       │   ├── ball_anime.py
│   │       │   ├── image.py
│   │       │   ├── off.py
│   │       │   ├── rgb.py
│   │       │   ├── sleep.py
│   │       │   └── wake.py
│   │       ├── disp/
│   │       │   ├── __init__.py
│   │       │   └── st7789v.py
│   │       ├── py.typed
│   │       └── utils/
│   │           ├── __init__.py
│   │           ├── my_logger.py
│   │           ├── performance_core.py
│   │           ├── sprite.py
│   │           └── utils.py
│   ├── ToDo.md
│   └── uv.lock
├── pi0ninja_v3/
│   ├── .gitignore
│   ├── .python-version
│   ├── pyproject.toml
│   ├── README.md
│   └── src/
│       └── pi0ninja_v3/
│           ├── __init__.py
│           ├── detect_distance.py
│           ├── facial_expressions.py
│           ├── movement_recorder.py
│           ├── ninja_agent.py
│           ├── py.typed
│           ├── robot_sound.py
│           ├── show_faces.py
│           ├── static/
│           │   ├── main.js
│           │   └── style.css
│           ├── templates/
│           │   └── index.html
│           └── web_server.py
├── piservo0/
│   ├── .gitignore
│   ├── .python-version
│   ├── docs/
│   │   ├── 20250802a-test-bipad01.mp4
│   │   ├── api_reference.rst
│   │   ├── conf.py
│   │   ├── index.rst
│   │   ├── JSONCMD_SAMPLES.md
│   │   ├── MEMO-keybindings.md
│   │   ├── Memo1.md
│   │   ├── SG90_a.pdf
│   │   ├── SoftwareArchitecture1.png
│   │   ├── SoftwareArchitecture2.png
│   │   └── STR_CMD.md
│   ├── GEMINI.md
│   ├── GEMINI2.md
│   ├── LICENSE
│   ├── Memo.md
│   ├── piservo0/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── command/
│   │   │   ├── __init__.py
│   │   │   ├── cmd_apiclient.py
│   │   │   ├── cmd_calib.py
│   │   │   ├── cmd_servo.py
│   │   │   └── cmd_strclient.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── calibrable_servo.py
│   │   │   ├── multi_servo.py
│   │   │   └── piservo.py
│   │   ├── helper/
│   │   │   ├── __init__.py
│   │   │   ├── str_cmd_to_json.md
│   │   │   ├── str_cmd_to_json.py
│   │   │   ├── thread_multi_servo.py
│   │   │   └── thread_worker.py
│   │   ├── py.typed
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── my_logger.py
│   │   │   └── servo_config_manager.py
│   │   └── web/
│   │       ├── __init__.py
│   │       ├── api_client.py
│   │       ├── json_api.py
│   │       └── sample_json.js
│   ├── pyproject.toml
│   ├── README.md
│   ├── REFERENCE.md
│   ├── samples/
│   │   ├── sample_01_piservo.py
│   │   ├── sample_02_calibrable_servo.py
│   │   ├── sample_03_multi_servo.py
│   │   └── tiny_robot/
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       ├── exec.py
│   │       ├── manual.py
│   │       ├── py.typed
│   │       ├── README.md
│   │       ├── right.txt
│   │       ├── script1-walk.txt
│   │       ├── script2-hi.txt
│   │       ├── script3-happy.txt
│   │       ├── script4-walk2.txt
│   │       ├── thr_manual.py
│   │       ├── tiny_robot_app.py
│   │       ├── tiny_robot1.jpg
│   │       ├── walk1.txt
│   │       ├── walk2.txt
│   │       └── web.py
│   ├── tasks/
│   │   ├── 01_specification_analysis.md
│   │   └── 02_document_correction.md
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── README.md
│   │   ├── test_01_piservo.py
│   │   ├── test_02_servo_config_manager.py
│   │   ├── test_03_calibrable_servo.py
│   │   ├── TEST_04_MULTI_SERVO.md
│   │   ├── test_04_multi_servo.py
│   │   └── test_05_thread_multi_servo.py
│   └── uv.lock
├── README.md
├── servo_movement.json
├── servo.json
└── vl53l0x_pigpio/
    ├── .gitignore
    ├── .python-version
    ├── archives/
    │   ├── 20250903-2325-Tasks-done.md
    │   ├── 20250904-0318-Tasks-done.md
    │   ├── 20250904-0346-Tasks-done.md
    │   ├── 20250904-1715-Tasks-done.md
    │   ├── 20250904-1728-Tasks-done.md
    │   ├── 20250904-1738-Tasks-done.md
    │   ├── 20250904-1801-Tasks-done.md
    │   ├── 20250904-1843-Tasks-done.md
    │   ├── 20250904-HHMM-Tasks-done.md
    │   ├── 20250905-1352-Tasks-done.md
    │   ├── 20250905-1449-Tasks-done.md
    │   ├── 20250905-1505-Tasks-done.md
│   ├── 20250905-1528-Tasks-done.md
    │   ├── 20250905-1550-Tasks-done.md
    │   ├── 20250905-1601-Tasks-done.md
    │   ├── 20250905-1601-ToDo.md
    │   ├── 20250905-1644-Tasks-done.md
    │   ├── 20250905-1707-ToDo.md
    │   ├── 20250908-0523-Tasks-done.md
    │   ├── 20250908-0613-Tasks-done.md
    │   └── 20250908-0638-ToDo-done.md
    ├── calibrate_output.txt
    ├── docs/
    │   └── PyPI.md
    ├── GEMINI.md
    ├── LICENSE
    ├── pyproject.toml
    ├── README.md
    ├── rename_task.py
    ├── samples/
    │   ├── calibrate_example.py
    │   ├── example.py
    │   └── numpy_example.py
    ├── src/
    │   └── vl53l0x_pigpio/
    │       ├── __init__.py
    │       ├── __main__.py
    │       ├── click_utils.py
    │       ├── config_manager.py
    │       ├── constants.py
    │       ├── driver.py
    │       ├── my_logger.py
    │       └── py.typed
    ├── tests/
    │   ├── test_01_driver.py
    │   ├── test_02_offset.py
    │   └── test_03_config_manager.py
    └── uv.lock
```

## Code-level Specifications

This section provides a detailed description of every function and method found in each file, including their required commands/arguments.

### `pi0ninja_v3` Library Specifications

#### `pi0ninja_v3/src/pi0ninja_v3/detect_distance.py`

**Imported Libraries:**
- `pigpio`
- `time`
- `sys`
- `select`
- `tty`
- `termios`
- `os`
- `vl53l0x_pigpio`

---

##### **Classes**

##### `DistanceDetector`
- **Description:** A class to detect distance using the VL53L0X sensor.
- **Methods:**
    - `__init__(self)`: Initializes the DistanceDetector.
    - `timed_detection(self, count: int, delay: float)`: Performs a specified number of distance measurements with a delay.
        - `count` (int): The number of measurements to take.
        - `delay` (float): The delay between measurements in seconds.
    - `continuous_detection(self)`: Performs continuous distance measurement at 5Hz until 'q' is pressed.
    - `cleanup(self)`: Cleans up the pigpio resources.

---

#### **Functions**

##### `main()`
- **Description:** Main function to run the interactive distance detector.
- **Arguments:** None
- **Returns:** None

### `pi0ninja_v3/src/pi0ninja_v3/facial_expressions.py`

**Imported Libraries:**
- `time`
- `math`
- `threading`
- `PIL`
- `pi0disp.disp.st7789v`

---

##### **Classes**

##### `AnimatedFaces`
- **Description:** Generates and displays programmatically drawn, animated facial expressions. This class is thread-safe.
- **Methods:**
    - `__init__(self, lcd: ST7789V)`: Initializes the AnimatedFaces class.
        - `lcd`: An instance of the `ST7789V` class.
    - `stop(self)`: Stops the current animation thread and waits for it to exit.
    - `play_idle(self, duration_s=float('inf'))`: Plays the idle animation.
    - `play_happy(self, duration_s=3)`: Plays the happy animation.
    - `play_laughing(self, duration_s=3)`: Plays the laughing animation.
    - `play_sad(self, duration_s=3)`: Plays the sad animation.
    - `play_cry(self, duration_s=3)`: Plays the crying animation.
    - `play_angry(self, duration_s=3)`: Plays the angry animation.
    - `play_surprising(self, duration_s=3)`: Plays the surprising animation.
    - `play_sleepy(self, duration_s=3)`: Plays the sleepy animation.
    - `play_speaking(self, duration_s=3)`: Plays the speaking animation.
    - `play_shy(self, duration_s=3)`: Plays the shy animation.
    - `play_embarrassing(self, duration_s=3)`: Plays the embarrassing animation.
    - `play_scary(self, duration_s=3)`: Plays the scary animation.
    - `play_exciting(self, duration_s=3)`: Plays the exciting animation.
    - `play_confusing(self, duration_s=3)`: Plays the confusing animation.

### `pi0ninja_v3/src/pi0ninja_v3/movement_recorder.py`

**Imported Libraries:**
- `json`
- `os`
- `time`
- `pigpio`
- `sys`
- `select`
- `termios`
- `tty`
- `copy`
- `piservo0.core.calibrable_servo`

---

##### **Classes**

##### `ServoController`
- **Description:** A custom controller to manage multiple servos based on `servo.json`.
- **Methods:**
    - `__init__(self)`: Initializes the ServoController.
    - `get_servo_definitions(self)`: Returns the raw servo definitions from the JSON file.
    - `move_servos(self, movements, speed='M')`: Executes a set of servo movements with smooth interpolation.
        - `movements` (dict): A dictionary of `{pin: angle}`.
        - `speed` (str, optional): The speed of the movement ('S', 'M', or 'F'). Defaults to 'M'.
    - `get_current_angles(self)`: Returns a dictionary of `{pin: current_angle}`.
    - `center_all_servos(self)`: Moves all servos to their center position.
    - `cleanup(self)`: Turns off all servos and disconnects from pigpio.

##### `NonBlockingKeyboard`
- **Description:** A class to handle non-blocking keyboard input.
- **Methods:**
    - `__enter__(self)`: Enters a non-blocking keyboard input context.
    - `__exit__(self, type, value, traceback)`: Exits the non-blocking keyboard input context.
    - `kbhit(self)`: Checks if a key has been pressed.
    - `getch(self)`: Gets the pressed character.

---

#### **Functions**

##### `load_movements()`
- **Description:** Loads movement sequences from the JSON file.
- **Arguments:** None
- **Returns:** A dictionary of movement sequences.

##### `save_movements(movements)`
- **Description:** Saves movement sequences to the JSON file.
- **Arguments:**
    - `movements` (dict): A dictionary of movement sequences.
- **Returns:** None

##### `parse_movement_command(command_str, definitions)`
- **Description:** Parses the user's command string.
- **Arguments:**
    - `command_str` (str): The command string to parse.
    - `definitions` (dict): The servo definitions.
- **Returns:** A tuple containing the speed and a dictionary of movements.

##### `record_new_movement(controller)`
- **Description:** Handles the UI and logic for recording a new movement sequence.
- **Arguments:**
    - `controller`: An instance of the `ServoController` class.
- **Returns:** None

##### `execute_movement(controller)`
- **Description:** Handles the UI and logic for executing a saved movement with looping and interruption.
- **Arguments:**
    - `controller`: An instance of the `ServoController` class.
- **Returns:** None

##### `edit_sequence_menu(controller, sequence_to_edit)`
- **Description:** UI for editing a sequence.
- **Arguments:**
    - `controller`: An instance of the `ServoController` class.
    - `sequence_to_edit` (list): The sequence to edit.
- **Returns:** The modified sequence or `None` if aborted.

##### `modify_existing_movement(controller)`
- **Description:** Handles the non-destructive modification of a movement sequence.
- **Arguments:**
    - `controller`: An instance of the `ServoController` class.
- **Returns:** None

##### `clear_movement(controller)`
- **Description:** Handles the UI and logic for clearing a movement sequence.
- **Arguments:**
    - `controller`: An instance of the `ServoController` class.
- **Returns:** None

##### `main_menu()`
- **Description:** Displays the main menu and handles user selection.
- **Arguments:** None
- **Returns:** None

### `pi0ninja_v3/src/pi0ninja_v3/ninja_agent.py`

**Imported Libraries:**
- `os`
- `json`
- `time`
- `google.generativeai`
- `pi0ninja_v3.facial_expressions`
- `pi0ninja_v3.robot_sound`
- `googlesearch`

---

##### **Classes**

##### `NinjaAgent`
- **Description:** An AI agent for the NinjaRobot that handles text-based conversations.
- **Methods:**
    - `__init__(self, api_key: str)`: Initializes the NinjaAgent.
        - `api_key` (str): The Gemini API key.
    - `web_search(self, query: str) -> list[str]`: Performs a web search and returns the results.
        - `query` (str): The search query.
    - `process_command(self, user_input: str) -> dict`: Processes a text-based user command.
        - `user_input` (str): The user's text input.
    - `process_audio_command(self, audio_file_path: str) -> dict`: Processes a voice command from an audio file.
        - `audio_file_path` (str): The path to the audio file.

### `pi0ninja_v3/src/pi0ninja_v3/robot_sound.py`

**Imported Libraries:**
- `pigpio`
- `time`
- `json`
- `os`
- `sys`
- `pi0buzzer.driver`

---

##### **Classes**

##### `RobotSoundPlayer`
- **Description:** A class to play sounds corresponding to robot emotions using a buzzer.
- **Methods:**
    - `__init__(self)`: Initializes the RobotSoundPlayer.
    - `play(self, emotion: str)`: Plays the sound for the given emotion.
        - `emotion` (str): The name of the emotion.
    - `cleanup(self)`: Cleans up the pigpio resources.

---

#### **Functions**

##### `main()`
- **Description:** Main function to run the interactive sound player.
- **Arguments:** None
- **Returns:** None

### `pi0ninja_v3/src/pi0ninja_v3/show_faces.py`

**Imported Libraries:**
- `sys`
- `select`
- `termios`
- `tty`
- `inspect`
- `time`
- `random`
- `pi0disp.disp.st7789v`
- `pi0ninja_v3.facial_expressions`

---

##### **Classes**

##### `NonBlockingKeyboard`
- **Description:** A class to handle non-blocking keyboard input.
- **Methods:**
    - `__enter__(self)`: Enters a non-blocking keyboard input context.
    - `__exit__(self, type, value, traceback)`: Exits the non-blocking keyboard input context.
    - `kbhit(self)`: Checks if a key has been pressed.
    - `getch(self)`: Gets the pressed character.

---

#### **Functions**

##### `get_face_methods(animated_faces_instance)`
- **Description:** Inspects the `AnimatedFaces` instance and returns a dictionary of face-playing methods.
- **Arguments:**
    - `animated_faces_instance`: An instance of the `AnimatedFaces` class.
- **Returns:** A dictionary of face-playing methods.

##### `draw_idle_frame(faces, is_blinking)`
- **Description:** Draws a single frame of the idle animation.
- **Arguments:**
    - `faces`: An instance of the `AnimatedFaces` class.
    - `is_blinking` (bool): Whether the eyes should be blinking.
- **Returns:** None

##### `main()`
- **Description:** Main function with a non-blocking idle loop and a blocking menu to display facial expressions.
- **Arguments:** None
- **Returns:** None

### `vl53l0x_pigpio` Library Specifications

#### `vl53l0x_pigpio/my_logger.py`

**Imported Libraries:**
- `logging`
- `inspect`

---

#### **Functions**

##### `get_logger(name: str, debug: bool = False) -> logging.Logger`
- **Description:** Configures and returns a logger instance.
- **Arguments:**
    - `name` (str): The name for the logger, typically `__name__`.
    - `debug` (bool): If True, the logger's level is set to DEBUG, otherwise it defaults to INFO.
- **Returns:** The configured logger instance.
