### 2025-11-06 - pi0disp Library and Asset Management

- **`pi0disp` Library Created**:
    - Created the full directory structure for the `pi0disp` library, including `pyproject.toml`, `__init__.py` files, and subdirectories for `disp`, `utils`, `commands`, and `fonts`.
    - Implemented the core driver `disp/st7789v.py` and utility modules `utils/performance_core.py` and `utils/image_processor.py` by adapting them from the V3 archive.
    - Created the CLI commands `commands/ball_anime.py` and `commands/image.py`.

- **Asset Management Refactored**:
    - Created a global `assets` directory at the project root with `images`, `sounds`, and `videos` subdirectories for centralized resource management.
    - Bundled Noto fonts for English, Japanese, and Traditional Chinese directly into the `pi0disp/src/pi0disp/fonts/` directory to make the library self-contained.
    - Updated `commands/ball_anime.py` to use `importlib.resources` for robustly loading the bundled fonts.

- **Bug Fixes & Documentation**:
    - **Fixed Pillow V10 Compatibility**: Replaced the deprecated `draw.textsize()` method with `draw.textbbox()` in `ball_anime.py` to resolve an `AttributeError`.
    - **Resolved Font Download Issues**: Corrected multiple `404 Not Found` errors by using reliable CDN URLs for font downloads before deciding to bundle them instead.
    - **Updated Documentation**: Updated `InstallationGuide.md`, `pi0disp/README.md`, and `ReconstructionGuide.md` to reflect the new bundled assets and simplified testing procedures.

### 2025-11-05 - pi0vl53l0x Library Created

- Created the `pi0vl53l0x` library for the VL53L0X distance sensor.
- Created `pyproject.toml`, `README.md`, and `LICENSE`.
- Copied `constants.py`, `driver.py`, `config_manager.py`, and `__main__.py` from `V3Archive`.
- Refactored the code to use the new `pi0vl53l0x` package structure and the centralized `ninja_utils` logger.
- All modules have been linted and passed checks.

### 2025-11-05 - pi0buzzer Library Created

- Created the `pi0buzzer` library.
- Copied `driver.py` and `__main__.py` from `V3Archive`.
- Created `__init__.py`, `pyproject.toml`, `README.md`, and `LICENSE`.
- All modules have been linted and passed checks.

### 2025-10-30 - Ninja Utils Library Created

- Created the `ninja_utils` library with the following modules:
    - `pyproject.toml`: Project metadata and dependencies.
    - `my_logger.py`: Centralized logging utility.
    - `keyboard.py`: Non-blocking keyboard input utility.
    - `__init__.py`: Package initializer.
- All modules have been linted and passed checks.

### 2025-10-30 - `ninja_utils` Testing and Error Resolution

- **Issue 1: `ImportError: cannot import name 'math' from partially initialized module 'ninja_utils'`**
    - **Cause**: Incorrect installation method (`uv pip install ninja_utils`) led to an unrelated PyPI package being installed instead of the local source.
    - **Resolution**: Provided clear instructions for uninstalling the incorrect package and installing the local `ninja_utils` in editable mode (`uv pip install -e .`) from within the `ninja_utils` directory.

- **Issue 2: `OSError: License file does not exist: LICENSE`**
    - **Cause**: The `pyproject.toml` specified `license = { file = "LICENSE" }`, but the `LICENSE` file was missing.
    - **Resolution**: Created a `LICENSE` file with the MIT license text in the `ninja_utils` directory.

- **Issue 3: `OSError: Readme file does not exist: README.md`**
    - **Cause**: The `pyproject.toml` specified `readme = "README.md"`, but the `README.md` file was missing.
    - **Resolution**: Created a basic `README.md` file in the `ninja_utils` directory.

- **Issue 4: `uv` warning about `VIRTUAL_ENV`**
    - **Cause**: `uv` detected an environment variable `VIRTUAL_ENV` that conflicted with the project's local `.venv`, leading to a warning.
    - **Resolution**: Clarified that this is a warning, not an error, and provided the `--active` flag for `uv run` to explicitly target the active environment and suppress the warning.

- **Testing Progress**:
    - Created `ninja_utils/samples/sample.py` to demonstrate `get_logger` and `NonBlockingKeyboard` functionality.
    - Provided updated, detailed instructions for installing and running the sample script on a different device, emphasizing the correct editable installation method.