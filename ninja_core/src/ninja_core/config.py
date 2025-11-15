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
        default_factory=dict,
        description="Mapping of servo names to GPIO pin numbers."
    )
    calibration: Dict[str, ServoCalibration] = Field(
        default_factory=dict,
        description="Calibration data for each servo, keyed by pin number as a string."
    )


class BuzzerConfig(BaseModel):
    """Configuration for the buzzer."""
    pin: Optional[int] = Field(None, description="The GPIO pin for the buzzer.")


class DisplayConfig(BaseModel):
    """Placeholder for display-related settings."""
    # Future settings: resolution, orientation, etc.
    pass


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
    api_keys: Dict[str, str] = Field(
        default_factory=dict,
        description="API keys for services like Google Gemini."
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
