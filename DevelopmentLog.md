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