"""
Hardware Abstraction Layer (HAL) for NinjaRobotV4.

This module provides a single, unified interface to all hardware components,
abstracting away the details of pin numbers and driver initialization. It is
responsible for initializing all hardware from a central configuration object
and providing a clean way to access and shut down the hardware.
"""

import pigpio
import logging
from .config import NinjaConfig

# Import driver classes from our hardware libraries
from pi0servo.core.multi_servo import MultiServo
from pi0buzzer.driver import MusicBuzzer
from pi0disp.disp.st7789v import ST7789V
from pi0vl53l0x.driver import VL53L0X

log = logging.getLogger(__name__)


class HardwareAbstractionLayer:
    """A class to initialize, manage, and access all robot hardware."""

    def __init__(self, config: NinjaConfig):
        """
        Initializes the HAL with the robot's configuration.

        Note: This only stores the config. Hardware is not initialized until
        the `initialize()` method is called.

        Args:
            config: The NinjaConfig object with all hardware settings.
        """
        self.config = config
        self.pi: pigpio.pi | None = None
        self.servos: MultiServo | None = None
        self.buzzer: MusicBuzzer | None = None
        self.display: ST7789V | None = None
        self.distance_sensor: VL53L0X | None = None
        log.info("Hardware Abstraction Layer created.")

    def initialize(self, components: list[str] = None):
        """
        Connects to the pigpio daemon and initializes all hardware components
        based on the provided configuration.

        Args:
            components: A list of component names to initialize. 
                        Options: "servos", "buzzer", "display", "sensors".
                        If None, all components are initialized.
        """
        log.info("Initializing hardware components...")
        try:
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise ConnectionError("Could not connect to the pigpiod daemon.")
            log.info("Successfully connected to pigpiod.")
        except Exception as e:
            log.error(f"Failed to connect to pigpio daemon: {e}")
            log.error("Please ensure the pigpio daemon is running (`sudo pigpiod`).")
            raise

        # --- Filter components if specified ---
        if components is None:
            # Default to all available components
            components = ["servos", "buzzer", "display", "sensors"]

        # --- Initialize Servos ---
        if "servos" in components and self.config.servos and self.config.servos.calibration:
            try:
                # Get a list of integer pins from the calibration data keys
                pin_list = [
                    int(pin_str) for pin_str in self.config.servos.calibration.keys()
                ]

                if pin_list:
                    log.info(f"Found pins {pin_list} in config. Initializing MultiServo.")
                    self.servos = MultiServo(
                        pi=self.pi,
                        pins=pin_list,
                        conf_file="servo.json",
                    )
                    log.info("MultiServo controller initialized using 'servo.json'.")
                else:
                    log.info(
                        "No servo calibration data found. Skipping servo initialization."
                    )
            except Exception as e:
                log.error(f"Failed to initialize Servos: {e}")
                log.warning("Continuing without Servos.")
                self.servos = None
        elif "servos" in components:
            log.info("No servo calibration data found or skipped.")

        # --- Initialize Buzzer ---
        if "buzzer" in components and self.config.buzzer and self.config.buzzer.pin:
            try:
                self.buzzer = MusicBuzzer(pin=self.config.buzzer.pin, pi=self.pi)
                log.info(f"Buzzer initialized on pin {self.config.buzzer.pin}.")
            except Exception as e:
                log.error(f"Failed to initialize Buzzer: {e}")
                log.warning("Continuing without Buzzer.")
                self.buzzer = None
        elif "buzzer" in components:
            log.info("No buzzer pin configured or skipped.")

        # --- Initialize Display ---
        if "display" in components and self.config.display and self.config.display.dc is not None:
            try:
                log.info("Initializing display...")
                self.display = ST7789V(
                    pi=self.pi,
                    channel=0,  # SPI channel 0
                    dc_pin=self.config.display.dc,
                    rst_pin=self.config.display.rst,
                    backlight_pin=self.config.display.blk,
                )
                log.info("Display initialized.")
            except Exception as e:
                log.error(f"Failed to initialize Display: {e}")
                log.warning("Continuing without Display.")
                self.display = None
        elif "display" in components:
            log.info("No display pins configured or skipped.")

        # --- Initialize Distance Sensor ---
        if "sensors" in components and self.config.sensors:
            try:
                log.info("Initializing distance sensor...")
                self.distance_sensor = VL53L0X(pi=self.pi)
                log.info("Distance sensor initialized.")
            except Exception as e:
                log.error(f"Failed to initialize distance sensor: {e}")
                log.warning("Continuing without distance sensor. Obstacle avoidance will be disabled.")
                self.distance_sensor = None
        elif "sensors" in components:
            log.info("No sensor config found. Skipping distance sensor.")

        log.info("Hardware initialization process complete.")

    def shutdown(self):
        """
        Safely shuts down all initialized hardware components and disconnects
        from the pigpio daemon.
        """
        log.info("Shutting down hardware components...")

        if self.servos:
            self.servos.off()
            log.info("All servos turned off.")

        if self.buzzer:
            self.buzzer.off()
            log.info("Buzzer turned off.")

        if self.display:
            self.display.close()
            log.info("Display closed.")

        if self.distance_sensor:
            self.distance_sensor.close()
            log.info("Distance sensor closed.")

        if self.pi and self.pi.connected:
            self.pi.stop()
            log.info("Disconnected from pigpiod.")
