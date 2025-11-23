### 2025-11-23 - Autostart Functionality (Phase 2.8)
- **Implemented Automatic Startup**:
    - Created `ninja_utils/src/ninja_utils/service_manager.py` to manage systemd services.
    - Added `install-startup`, `remove-startup`, and `status-startup` commands to `ninja_utils` CLI.
    - **Safety Features**: The installation script validates that `config.json` exists, `pigpiod` is running, and `ninja_core` is installed before enabling the service.
- **Documentation**:
    - Updated `ReconstructionGuide.md` with Phase 2.8 details.
    - Updated `InstallationGuide.md` with instructions for enabling autostart.

### 2025-11-20 - Web Server Fixes & Documentation
- **Server Startup Robustness**:
    - Modified `web_server.py` to catch `MissingAPIKeyError` during startup. The server now starts even if the Gemini API key is missing (AI features disabled).
    - Refined `ninja_core server` startup to intelligently check for existing `ngrok` configuration and prompt the user accordingly.
    - Implemented a **Welcome Greeting** (Happy Face + Sound) that triggers automatically when a user connects to the web interface (via localhost or ngrok).
    - Added **Voice Input** support to the web interface:
        - Uses Web Speech API for client-side recognition.
        - Supports English, Japanese, Traditional Chinese, and Simplified Chinese via a language selector.
        - Includes a 30-second recording timeout and visual feedback.
    - **Fixes**:
        - Resolved a critical regression where the missing text input field caused the web interface JavaScript to crash, breaking all controls and the API key status check.
        - Restored the text input field and reorganized the layout (controls below input) as requested.
- **Documentation**:
    - Updated `ninja_core/README.md` with detailed steps for creating a Google Gemini API key and an ngrok account/authtoken.
    - Clarified setup instructions for new users.

### 2025-11-20 - Web Server & Remote Access (Phase 2.6)
- **Implemented Web Server**:
    - Created `web_server.py` using FastAPI and Uvicorn.
    - Integrated `HardwareAbstractionLayer` and `NinjaAgent` into the web application state.
    - Implemented API endpoints for Chat, Servo Movements, Facial Expressions, Sounds, and Distance Sensor.
    - Added `ninja_core server` CLI command.
- **Remote Access**:
    - Integrated `pyngrok` to automatically create a public tunnel.
    - Displays a QR code of the public URL on the robot's screen.
- **Web Interface**:
    - Ported `index.html`, `style.css`, and `main.js` from V3.
    - Updated frontend to communicate with V4 API endpoints.
    - Added real-time distance monitoring via WebSocket.
- **Safety Integration**:
    - Enforced Obstacle Avoidance in web-triggered movements using `abort_check`.

### 2025-11-20 - Chat Features Enhancement
- **Welcome Greeting**:
    - Added a "happy" face and greeting message ("Hello! I am ready.") upon starting the chat.
- **Idle Status Management**:
    - The agent now defaults to the "idle" face.
    - Automatically returns to the "idle" face 3 seconds after completing any interaction.
- **Bug Fixes**:
    - Fixed `NameError: name 'time' is not defined` by importing the `time` module.
    - Fixed `pigpio.error: 'unknown handle'` by ensuring the facial animation thread is stopped (`faces.stop()`) before the HAL shutdown.

### 2025-11-20 - Obstacle Avoidance Feature
- **Implemented Safety Reflex**:
    - Modified `MovementController` to support emergency stops via an `abort_check` callback.
    - Updated `__main__.py` (chat command) to continuously monitor distance during movements.
    - **Refinement**: Decreased monitoring interval from 0.1s to 0.01s for higher sensitivity and faster reaction time.
    - **Behavior**: If an object is detected < 5cm away, the robot immediately stops, centers servos, and displays a "frightened" reaction.

### 2025-11-20 - AI Agent (`ninja_agent.py`) Implementation

- **Completed Phase 2.5**: Implemented the core AI Agent logic.
    - **Created `ninja_agent.py`**:
        - Integrated **Google Gemini** for natural language processing.
        - Implemented **Nuance & Semantic Understanding**: The agent now interprets synonyms (e.g., "joyful" -> "happy") and maps them to robot actions.
        - Implemented **Multilingual Support**: The agent detects and responds in the user's language (English, Japanese, Chinese).
        - Implemented **Real-Time Web Search**: Integrated `googlesearch-python` to answer questions about current events.
        - Implemented **Automatic Emotional Expression**: The robot automatically displays a "speaking" face/sound if the AI response has no physical actions.
    - **Updated `config.py` & `__main__.py`**:
        - Added `api_keys` management to `NinjaConfig`.
        - Added `ninja_core config set-key` CLI command for easy API key setup.
    - **Verified Functionality**:
        - Created `verify_agent.py` to test logic, JSON parsing, and auto-emotion rules without hardware.
        - Verified that the agent correctly handles missing API keys and generates valid action plans.

### 2025-11-18 - `movement-tool` Finalization and Bug Fixes

- **Completed `movement-tool` Features**:
    - Implemented the "Modify existing movement" and "Clear movement" functions, making the tool fully featured.
    - Integrated the `pi0servo` calibration tool directly into the `movement-tool`'s main menu for a unified user experience.

- **Critical Bug Fixes & UX Improvements**:
    - **Fixed `AttributeError: 'NoneType'`:** Resolved a critical bug where the application would crash after using the calibration tool. The root cause was a stale hardware object being held by the `MovementController`. The fix ensures that the controller is re-instantiated with a fresh, live hardware object after the calibration subprocess completes.
    - **Seamless Configuration Sync:** The calibration workflow was redesigned to be seamless. After a user calibrates a servo, the new `servo.json` data is now automatically imported into the application's in-memory configuration, eliminating the need for the user to manually run `config import-all` and providing immediate feedback.
    - **Data Type Mismatches:** Fixed several bugs related to `int` vs `str` keys for servo pins and `list` vs `dict` return types for angle data.

- **Documentation**:
    - Updated `ninja_core/README.md` with a comprehensive guide to the now-complete `movement-tool`, including the new calibration workflow.

### 2025-11-18 - Motion System Ported and Refactored


- **Completed Sub-Phase 2.4.4**: Ported the motion control and recording logic from the V3 archive into the `ninja_core` application.
    - **Created `movement_controller.py`**: Implemented the `MovementController` class, which handles the execution of complex, interpolated servo movements. It is fully integrated with the HAL and `NinjaConfig`, removing all direct hardware access and file I/O.
    - **Created `movement_cli.py`**: The interactive CLI for recording, editing, and testing movement sequences was ported into its own module to separate developer tools from runtime logic.
    - **Added `movement-tool` CLI Command**: Exposed the interactive movement CLI through the main `ninja_core` entry point (`uv run ninja_core movement-tool`).
    - **Documentation**: Added a comprehensive guide to the `ninja_core/README.md` explaining the Motion System's architecture, command rules, and testing procedures.

### 2025-11-17 - Distance Detection Feature Added


- **Completed New Feature**: Implemented a centralized distance detection feature as requested.
    - **HAL Integration**: The `VL53L0X` distance sensor driver was fully integrated into the Hardware Abstraction Layer (`hal.py`).
    - **Created `perception.py`**: Added the new module to `ninja_core/src/ninja_core/` to house perception-related logic.
    - **Implemented `DistanceMonitor`**: Created the `DistanceMonitor` class, which provides both single-shot (`get_distance`) and continuous, thread-based background monitoring (`start_continuous`, `stop_continuous`).
    - **Verified Functionality**: Created `test_perception.py` and successfully tested both measurement modes, confirming the feature is robust and working correctly.

### 2025-11-17 - Robot Sound Module Created

- **Completed Sub-Phase 2.4.2**: Created the core application logic for auditory feedback.
    - **Created `robot_sound.py`**: Added the new module to `ninja_core/src/ninja_core/`.
    - **Ported and Refactored `RobotSoundPlayer`**: Ported the class from the V3 archive and refactored it to integrate seamlessly with the Hardware Abstraction Layer. All direct hardware initialization and file I/O have been removed.
    - **Verified Functionality**: Created `test_robot_sound.py` and successfully tested the module, confirming that all sounds play correctly through the HAL.

### 2025-11-17 — Facial Expressions Module and HAL Integration

- **Completed Sub-Phase 2.4.1**
    - Ported and refactored `AnimatedFaces` into `ninja_core/src/ninja_core/facial_expressions.py`.
    - Consolidated the API into a single `play()` method and integrated the module with the HAL.
    - Module validated by tests.

- **HAL integration and debugging**
    - Performed extensive debugging to fully integrate hardware drivers with the HAL.

- **Bug fixes**
    - Fixed `AttributeError: 'HardwareAbstractionLayer' object has no attribute 'display'` by enabling display driver initialization in `hal.py`.
    - Fixed `AttributeError: 'DisplayConfig' object has no attribute 'pins'` by adding explicit pin fields (`dc`, `rst`, `blk`) to `DisplayConfig` in `config.py` and updating `hal.py` to access them.
    - Fixed `TypeError` on driver initialization by standardizing `ST7789V` (display) and `MusicBuzzer` drivers to accept an optional shared `pigpio` connection from the HAL (avoids unexpected kwargs like `pi` and `spi_port`).
    - Fixed incorrect method calls: removed an unnecessary `.begin()` call and replaced `.off()` with the correct `.close()` on the display driver.
    - Fixed `OSError: [Errno 9] Bad file descriptor` by resolving a race condition in `test_facial_expressions.py` — the animation thread is now stopped explicitly before HAL shutdown.
    - Fixed `NinjaConfig.load()` error by updating the test script to call `load_config()` instead of a non-existent class method.

### 2025-11-16 — HAL Integration and Debugging

- **Completed HAL integration testing**
    - Verified `ninja_core` can control hardware using the master `config.json`. Iterative fixes included:

    - Fixed `ImportError` by importing `MultiServo` and `CalibrableServo` directly from their source modules (e.g., `pi0servo.core.multi_servo`) to match the unmodified `pi0servo` library layout.
    - Fixed `AttributeError` in `config import-all` by handling list-based `servo.json` format during imports.
    - Fixed `TypeError` on HAL initialization by refactoring servo initialization: HAL now passes a list of pin numbers to `MultiServo`, matching the original `pi0servo` API.
    - Fixed shutdown `AttributeError` by changing `self.servos.off_all()` to the correct `self.servos.off()` in `hal.py`.

### 2025-11-15 — Phase 2: Hardware Abstraction Layer

- **`HardwareAbstractionLayer` created**
    - Added `ninja_core/src/ninja_core/hal.py` and implemented the `HardwareAbstractionLayer` (HAL) class.
    - `initialize()` reads from a `NinjaConfig` object to instantiate/configure hardware drivers (`MultiServo`, `MusicBuzzer`) and manages a shared `pigpio` connection.
    - `shutdown()` ensures all hardware components are safely turned off.
    - Module linted and passed checks.

### 2025-11-09 — pi0servo Library Refinements

- **Safety and UX improvements**
    - `CalibrableServo` now initializes with safe defaults (Min/Center/Max pulses default to 1500 when missing).
    - `pi0servo servo` command refactored to use `CalibrableServo`, accept angles and keywords (`min`, `center`, `max`), and respect calibrated limits from `servo.json`.
    - `pi0servo calib` UI improved:
        - New keybindings: `v`, `c`, `x` for direct target selection; `Tab` still cycles targets.
        - Movement keys swapped: `Up`/`Down` for large steps, `w`/`s` for fine tuning.
        - Help text updated.

### 2025-11-09 — pi0servo Library Created

- Created library skeleton (`pyproject.toml`, `LICENSE`, `README.md`) and package structure (`core`, `helper`, `utils`, `command`).
- Implemented core classes: `PiServo`, `CalibrableServo`, `MultiServo` (adapted from V3 archive).
- Added async control classes (`ThreadWorker`, `ThreadMultiServo`) and `ServoConfigManager`.
- Implemented CLI: `cmd_calib.py`, `cmd_servo.py`, and main `__main__.py`.
- Modules linted and passed checks.
- Updated `ReconstructionGuide.md` with configuration management plan for `ninja_core`.

### 2025-11-06 — pi0disp Library and Asset Management

- **`pi0disp` library created**
    - Added package structure and implemented `disp/st7789v.py`, `utils/performance_core.py`, and `utils/image_processor.py` (adapted from V3).
    - Added CLI commands `commands/ball_anime.py` and `commands/image.py`.

- **Asset management**
    - Created global `assets/` at project root with `images`, `sounds`, and `videos`.
    - Bundled Noto fonts (EN, JP, TC) into `pi0disp/src/pi0disp/fonts/` for a self-contained library.
    - Updated `commands/ball_anime.py` to use `importlib.resources` for loading bundled fonts.

- **Bug fixes & docs**
    - Replaced deprecated Pillow `draw.textsize()` with `draw.textbbox()` to fix compatibility with Pillow v10.
    - Resolved font download `404` issues and switched to bundling fonts.
    - Updated `InstallationGuide.md`, `pi0disp/README.md`, and `ReconstructionGuide.md`.

### 2025-11-05 — pi0vl53l0x Library Created

- Created `pi0vl53l0x` library (`pyproject.toml`, `README.md`, `LICENSE`).
- Ported and refactored `constants.py`, `driver.py`, `config_manager.py`, and `__main__.py` from V3Archive.
- Integrated centralized `ninja_utils` logger.
- Modules linted and passed checks.

### 2025-11-05 — pi0buzzer Library Created

- Created `pi0buzzer` library: `driver.py`, `__main__.py`, `__init__.py`, `pyproject.toml`, `README.md`, `LICENSE`.
- Modules linted and passed checks.

### 2025-10-30 — Ninja Utils Library Created

- Created `ninja_utils` with:
    - `pyproject.toml`
    - `my_logger.py` (centralized logging)
    - `keyboard.py` (non-blocking keyboard input)
    - `__init__.py`
- Modules linted and passed checks.

### 2025-10-30 — `ninja_utils` Testing and Error Resolution

- Issue: `ImportError: cannot import name 'math' from partially initialized module 'ninja_utils'`
    - Cause: Incorrect installation (`uv pip install ninja_utils`) installed unrelated PyPI package instead of local source.
    - Resolution: Uninstall incorrect package and install local package in editable mode: `uv pip install -e .` from inside `ninja_utils` directory.

- Issue: `OSError: License file does not exist: LICENSE`
    - Cause: `pyproject.toml` referenced `LICENSE` that was missing.
    - Resolution: Added `LICENSE` (MIT) to `ninja_utils`.

- Issue: `OSError: Readme file does not exist: README.md`
    - Cause: `pyproject.toml` referenced `README.md` that was missing.
    - Resolution: Added `README.md` to `ninja_utils`.

- Issue: `uv` warning about `VIRTUAL_ENV`
    - Cause: `uv` detected a conflicting `VIRTUAL_ENV`.
    - Resolution: Clarified it's a warning and documented `--active` flag for `uv run` to target the active environment.

- Testing progress
    - Added `ninja_utils/samples/sample.py` demonstrating `get_logger` and `NonBlockingKeyboard`.
    - Provided installation and run instructions emphasizing editable installation.
