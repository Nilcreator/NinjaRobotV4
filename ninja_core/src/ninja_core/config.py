"""
Centralized configuration management for NinjaRobotV4.

This module defines the data structures for the robot's configuration using Pydantic
and provides functions to load, save, and manage the config file.
"""

import json
from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseModel, Field


# --- Data Models for Configuration ---


class ServoCalibration(BaseModel):
    """Stores calibration data for a single servo."""

    min_pulse: int = 500
    center_pulse: int = 1500
    max_pulse: int = 2500
    angle_range: int = 180


class ServosConfig(BaseModel):
    """Configuration for all servos."""

    pins: Dict[str, int] = Field(
        default_factory=dict, description="Mapping of servo names to GPIO pin numbers."
    )
    calibration: Dict[str, ServoCalibration] = Field(
        default_factory=dict,
        description="Calibration data for each servo, keyed by pin number as a string.",
    )


class BuzzerConfig(BaseModel):
    """Configuration for the buzzer."""

    pin: Optional[int] = Field(None, description="The GPIO pin for the buzzer.")


class DisplayConfig(BaseModel):
    """Configuration for the ST7789V display."""

    dc: Optional[int] = Field(18, description="The DC (Data/Command) pin.")
    rst: Optional[int] = Field(19, description="The RST (Reset) pin.")
    blk: Optional[int] = Field(20, description="The BLK (Backlight) pin.")


class SensorConfig(BaseModel):
    """Placeholder for sensor-related settings."""

    # Future settings: I2C address, offsets, etc.
    pass


class NinjaConfig(BaseModel):
    """The root configuration model for the entire robot."""

    servos: ServosConfig = Field(default_factory=ServosConfig)
    buzzer: BuzzerConfig = Field(default_factory=BuzzerConfig)
    display: DisplayConfig = Field(default_factory=DisplayConfig)
    sensors: SensorConfig = Field(default_factory=SensorConfig)
    movements: Dict[str, list] = Field(
        default_factory=dict, description="Named servo movement sequences."
    )
    api_keys: Dict[str, str] = Field(
        default_factory=dict, description="API keys for services like Google Gemini."
    )


# --- Configuration Management Functions ---

CONFIG_FILE_PATH = Path("config.json")


def save_config(config: NinjaConfig, path: Path = CONFIG_FILE_PATH):
    """Saves the configuration object to a JSON file."""
    with open(path, "w") as f:
        json.dump(config.model_dump(), f, indent=4)


def load_config(path: Path = CONFIG_FILE_PATH) -> NinjaConfig:
    """
    Loads the configuration from a JSON file.

    If the file does not exist, it creates a default configuration file.
    """
    if not path.exists():
        print(f"Configuration file not found. Creating default config at '{path}'")
        default_config = NinjaConfig()
        save_config(default_config, path)
        return default_config

    with open(path, "r") as f:
        data = json.load(f)
        return NinjaConfig.model_validate(data)


def import_and_update_config(config: NinjaConfig) -> bool:
    """
    Imports settings from individual hardware config files and updates the config object.

    Args:
        config: The NinjaConfig object to update in memory.

    Returns:
        True if changes were made, False otherwise.
    """
    servo_config_path = Path("servo.json")
    buzzer_config_path = Path("buzzer.json")
    made_changes = False

    # --- Import servo calibration ---
    if servo_config_path.exists():
        print(f"Found servo config at '{servo_config_path}'. Importing...")
        with open(servo_config_path, "r") as f:
            servo_data = json.load(f)

        if isinstance(servo_data, list):
            for servo_entry in servo_data:
                pin = servo_entry.get("pin")
                if pin is None:
                    continue

                pin_str = str(pin)
                new_calib = ServoCalibration.model_validate(servo_entry)
                if config.servos.calibration.get(pin_str) != new_calib:
                    config.servos.calibration[pin_str] = new_calib
                    made_changes = True
        print("...servo import complete.")
    else:
        print(f"Info: Servo config '{servo_config_path}' not found. Skipping.")

    # --- Import buzzer pin ---
    if buzzer_config_path.exists():
        print(f"Found buzzer config at '{buzzer_config_path}'. Importing...")
        with open(buzzer_config_path, "r") as f:
            buzzer_data = json.load(f)

        if "pin" in buzzer_data and config.buzzer.pin != buzzer_data["pin"]:
            config.buzzer.pin = buzzer_data["pin"]
            made_changes = True
        print("...buzzer import complete.")
    else:
        print(f"Info: Buzzer config '{buzzer_config_path}' not found. Skipping.")

    return made_changes
