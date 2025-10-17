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

### `main_robot_control.py`

**Imported Libraries:**
- `time`
- `json`
- `pigpio`
- `threading`
- `PIL`
- `piservo0`
- `pi0disp`
- `pi0buzzer`
- `vl53l0x_pigpio`
- `pi0ninja_v3`
- `pathlib`

---

#### **Functions**

##### `load_pins_from_config()`
- **Description:** Loads servo and buzzer pins from their respective JSON files.
- **Arguments:** None
- **Returns:** A tuple containing a list of servo pins and the buzzer pin.

##### `main()`
- **Description:** Main function to control the NinjaRobotV3 components.
- **Arguments:** None
- **Returns:** None

### `pi0buzzer/src/pi0buzzer/__main__.py`

**Imported Libraries:**
- `click`
- `pigpio`
- `json`
- `time`
- `pi0buzzer.driver`

---

#### **Functions**

##### `cli()`
- **Description:** Defines the command-line interface group.
- **Arguments:** None
- **Returns:** None

##### `init(pin)`
- **Description:** Initializes the buzzer on the specified GPIO pin.
- **Arguments:**
    - `pin` (int): The GPIO pin number.
- **Returns:** None

##### `beep(pin, frequency, duration)`
- **Description:** Plays a simple beep.
- **Arguments:**
    - `--pin` (int, optional): GPIO pin for the buzzer. Reads from `buzzer.json` if not provided.
    - `frequency` (float, default: 440.0): The frequency of the beep in Hz.
    - `duration` (float, default: 0.5): The duration of the beep in seconds.
- **Returns:** None

##### `playmusic(pin)`
- **Description:** Play music with the buzzer using the keyboard.
- **Arguments:**
    - `--pin` (int, optional): GPIO pin for the buzzer.
- **Returns:** None

### `pi0buzzer/src/pi0buzzer/driver.py`

**Imported Libraries:**
- `pigpio`
- `time`
- `json`
- `os`
- `sys`
- `tty`
- `termios`
- `select`

---

#### **Classes**

##### `Buzzer`
- **Description:** A class to control a buzzer.
- **Methods:**
    - `__init__(self, pi, pin, config_file='buzzer.json')`: Initializes the buzzer.
        - `pi`: pigpio.pi object.
        - `pin`: The GPIO pin number.
        - `config_file` (str, optional): The configuration file. Defaults to 'buzzer.json'.
    - `save_config(self)`: Saves the pin configuration to a file.
    - `play_hello(self)`: Plays a simple melody.
    - `play_sound(self, frequency, duration)`: Plays a sound with a given frequency and duration.
        - `frequency` (float): The frequency of the sound in Hz.
        - `duration` (float): The duration of the sound in seconds.
    - `off(self)`: Turns the buzzer off.

##### `MusicBuzzer(Buzzer)`
- **Description:** A class to play music with the buzzer. Inherits from `Buzzer`.
- **Methods:**
    - `__init__(self, pi, pin, config_file='buzzer.json')`: Initializes the music buzzer.
        - `pi`: pigpio.pi object.
        - `pin`: The GPIO pin number.
        - `config_file` (str, optional): The configuration file. Defaults to 'buzzer.json'.
    - `play_song(self, song)`: Plays a song defined as a list of (note_key, duration) tuples.
        - `song` (list): A list of tuples, where each tuple is (note_key, duration).
    - `play_music(self)`: Plays "Happy Birthday" and then enters a mode where the user can play notes with the keyboard.

### `pi0disp/samples/basic_usage.py`

**Imported Libraries:**
- `time`
- `pi0disp`
- `PIL`

---

This script demonstrates the basic usage of the `pi0disp` library. It initializes the display, draws a blue circle on a black background, displays it for 5 seconds, then draws a red rectangle on top of it and displays the result for another 5 seconds.

### `pi0disp/samples/robot_face1.py`

**Imported Libraries:**
- `time`
- `sys`
- `pathlib`
- `typing`
- `click`
- `PIL`
- `pi0disp.disp.st7789v`
- `pi0disp.utils.my_logger`
- `pi0disp.utils.utils`

---

#### **Classes**

##### `RobotFace`
- **Description:** Manages drawing and animating the geometric robot face.
- **Methods:**
    - `__init__(self, lcd: ST7789V, font: ImageFont.FreeTypeFont | ImageFont.ImageFont)`: Initializes the RobotFace.
        - `lcd`: An instance of the `ST7789V` class.
        - `font`: A PIL ImageFont object.
    - `_get_eye_bbox(self, center_x: int, center_y: int, radius: int) -> Tuple[int, int, int, int]`: Calculates the bounding box for an eye.
    - `_draw_overlay_text(self, text: str, y_offset_ratio: float = 0.0) -> Tuple[int, int, int, int]`: Draws overlay text.
    - `_clear_overlay_text(self) -> Optional[Tuple[int, int, int, int]]`: Clears any existing overlay text.
    - `draw_eyes(self, state: str = "open", color: Tuple[int, int, int] = (255, 255, 255)) -> Tuple[int, int, int, int]`: Draws the eyes with a given state and color.
    - `draw_mouth(self, state: str = "neutral", color: Tuple[int, int, int] = (255, 255, 255)) -> Tuple[int, int, int, int]`: Draws the mouth with a given state and color.
    - `animate_blink(self, num_blinks: int = 1, blink_duration: float = 0.1)`: Animates blinking.
    - `animate_expression(self, expression: str, duration: float = 1.0, save_screenshot_flag: bool = False)`: Animates a facial expression.
    - `save_screenshot(self, filename: str = "screenshot.png")`: Saves the current display buffer to a PNG file.

---

#### **Functions**

##### `main(screenshot, face, debug)`
- **Description:** Main function to run the geometric robot face animation.
- **Arguments:**
    - `--screenshot` (bool, optional): Save screenshot for each expression.
    - `--face` (str, optional): Display a specific face and exit.
    - `--debug` (bool, optional): Enable debug logging.
- **Returns:** None

### `pi0disp/samples/robot_face2.py`

**Imported Libraries:**
- `time`
- `sys`
- `pathlib`
- `typing`
- `math`
- `PIL`
- `pi0disp.disp.st7789v`
- `pi0disp.utils.sprite`
- `pi0disp.utils.performance_core`

---

#### **Classes**

##### `RobotFace(Sprite)`
- **Description:** A robot face class that inherits from `Sprite`.
- **Methods:**
    - `__init__(self, x: int, y: int, width: int, height: int)`: Initializes the RobotFace sprite.
        - `x` (int): The x-coordinate of the top-left corner.
        - `y` (int): The y-coordinate of the top-left corner.
        - `width` (int): The width of the sprite.
        - `height` (int): The height of the sprite.
    - `update(self, delta_t: float)`: Updates the expression based on time.
    - `draw(self, draw: ImageDraw.ImageDraw)`: Draws the current expression of the face.
    - `_draw_open_eye(self, draw: ImageDraw.ImageDraw, center_x: int)`: Draws an open eye.
    - `_draw_closed_eye(self, draw: ImageDraw.ImageDraw, center_x: int)`: Draws a closed eye.
    - `_draw_happy_eye(self, draw: ImageDraw.ImageDraw, center_x: int)`: Draws a happy eye.

---

#### **Functions**

##### `main()`
- **Description:** Main function to run the robot face animation using the `Sprite` class.
- **Arguments:** None
- **Returns:** None

### `pi0disp/samples/sprite_usage.py`

**Imported Libraries:**
- `time`
- `sys`
- `pathlib`
- `random`
- `colorsys`
- `typing`
- `PIL`
- `pi0disp.disp.st7789v`
- `pi0disp.utils.sprite`
- `pi0disp.utils.performance_core`
- `pi0disp.utils.utils`

---

#### **Classes**

##### `Ball(Sprite)`
- **Description:** A bouncing ball sprite that inherits from the `Sprite` class.
- **Methods:**
    - `__init__(self, x, y, radius, speed_x, speed_y, color, screen_width, screen_height)`: Initializes the Ball sprite.
        - `x` (float): The initial x-coordinate.
        - `y` (float): The initial y-coordinate.
        - `radius` (int): The radius of the ball.
        - `speed_x` (float): The initial speed in the x-direction.
        - `speed_y` (float): The initial speed in the y-direction.
        - `color` (tuple): The color of the ball.
        - `screen_width` (int): The width of the screen.
        - `screen_height` (int): The height of the screen.
    - `update(self, delta_t: float)`: Updates the ball's position and handles bouncing off the screen edges.
    - `draw(self, draw: ImageDraw.ImageDraw)`: Draws the ball on the provided `ImageDraw` object.

---

#### **Functions**

##### `main()`
- **Description:** Main function to run the bouncing ball animation.
- **Arguments:** None
- **Returns:** None

### `pi0disp/src/pi0disp/__main__.py`

**Imported Libraries:**
- `click`
- `pi0disp`
- `pi0disp.commands.off`
- `pi0disp.commands.sleep`
- `pi0disp.commands.ball_anime`
- `pi0disp.commands.wake`
- `pi0disp.commands.rgb`
- `pi0disp.commands.image`
- `pi0disp.utils.my_logger`

---

#### **Functions**

##### `cli()`
- **Description:** Defines the command-line interface group for the ST7789V Display Driver. It provides basic commands to test and interact with the display.
- **Arguments:** None
- **Returns:** None

### `pi0disp/src/pi0disp/commands/ball_anime.py`

**Imported Libraries:**
- `time`
- `colorsys`
- `typing`
- `math`
- `click`
- `numpy`
- `PIL`
- `pi0disp.disp.st7789v`
- `pi0disp.utils.my_logger`
- `pi0disp.utils.performance_core`
- `pi0disp.utils.utils`

---

#### **Classes**

##### `Ball`
- **Description:** An optimized ball class for the animation demo.
- **Methods:**
    - `__init__(self, x, y, radius, speed, angle, fill_color)`: Initializes the Ball object.
    - `update_position(self, delta_t, screen_width, screen_height)`: Updates the ball's position.
    - `get_bbox(self)`: Returns the bounding box of the ball.
    - `draw(self, draw: ImageDraw.ImageDraw)`: Draws the ball.

##### `FpsCounter`
- **Description:** An optimized FPS counter.
- **Methods:**
    - `__init__(self)`: Initializes the FpsCounter.
    - `update(self) -> bool`: Updates the FPS counter.

---

#### **Functions**

##### `fast_sqrt(value)`
- **Description:** A fast square root calculation with caching.
- **Arguments:**
    - `value` (float): The value to calculate the square root of.
- **Returns:** The square root of the value.

##### `fast_cos_sin(angle)`
- **Description:** A fast cosine and sine calculation with caching.
- **Arguments:**
    - `angle` (float): The angle in radians.
- **Returns:** A tuple containing the cosine and sine of the angle.

##### `_initialize_balls_optimized(num_balls: int, width: int, height: int, ball_speed: float) -> List[Ball]`
- **Description:** Initializes the balls for the animation.
- **Arguments:**
    - `num_balls` (int): The number of balls.
    - `width` (int): The width of the screen.
    - `height` (int): The height of the screen.
    - `ball_speed` (float): The speed of the balls.
- **Returns:** A list of `Ball` objects.

##### `_handle_ball_collisions_optimized(balls: List[Ball], frame_count: int)`
- **Description:** Handles collisions between balls.
- **Arguments:**
    - `balls` (List[Ball]): A list of `Ball` objects.
    - `frame_count` (int): The current frame count.
- **Returns:** None

##### `_main_loop_optimized(lcd: ST7789V, background: Image.Image, balls: List[Ball], fps_counter: FpsCounter, font, target_fps: float)`
- **Description:** The main loop for the animation.
- **Arguments:**
    - `lcd`: An instance of the `ST7789V` class.
    - `background` (Image.Image): The background image.
    - `balls` (List[Ball]): A list of `Ball` objects.
    - `fps_counter` (FpsCounter): An instance of the `FpsCounter` class.
    - `font`: A PIL ImageFont object.
    - `target_fps` (float): The target frames per second.
- **Returns:** None

##### `ball_anime(spi_mhz: float, fps: float, num_balls: int, ball_speed: float)`
- **Description:** Runs the physics-based animation demo.
- **Arguments:**
    - `--spi-mhz` (float, optional): SPI speed in MHz.
    - `--fps` (float, optional): Target frames per second.
    - `--num-balls` (int, optional): Number of balls to display.
    - `--ball-speed` (float, optional): Absolute speed of balls (pixels/second).
- **Returns:** None