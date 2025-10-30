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