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
from pi0servo.core import MultiServo, CalibrableServo
from pi0buzzer.driver import MusicBuzzer
# from pi0disp.disp.st7789v import ST7789V  # Placeholder: Add when disp is ready
# from pi0vl53l0x.driver import VL53L0X      # Placeholder: Add when sensor is ready

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
        # self.display: ST7789V | None = None
        # self.distance_sensor: VL53L0X | None = None
        log.info("Hardware Abstraction Layer created.")

    def initialize(self):
        """
        Connects to the pigpio daemon and initializes all hardware components
        based on the provided configuration.
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

        # --- Initialize Servos ---
        if self.config.servos and self.config.servos.calibration:
            servo_list = []
            for pin_str, calibration_data in self.config.servos.calibration.items():
                pin = int(pin_str)
                servo = CalibrableServo(
                    pi=self.pi,
                    pin=pin,
                    config_data=calibration_data.model_dump()  # Pass config directly
                )
                log.info(f"Initialized servo on pin {pin} with imported calibration.")
                servo_list.append(servo)

            if servo_list:
                self.servos = MultiServo(self.pi, servo_list)
                log.info("MultiServo controller initialized.")
        else:
            log.info("No servo calibration data found. Skipping servo initialization.")

        # --- Initialize Buzzer ---
        if self.config.buzzer and self.config.buzzer.pin:
            self.buzzer = MusicBuzzer(self.pi, self.config.buzzer.pin)
            log.info(f"Buzzer initialized on pin {self.config.buzzer.pin}.")
        else:
            log.info("No buzzer pin configured. Skipping buzzer initialization.")

        # --- Initialize Display (Placeholder) ---
        # if self.config.display:
        #     log.info("Initializing display...")

        # --- Initialize Distance Sensor (Placeholder) ---
        # if self.config.sensors:
        #     log.info("Initializing distance sensor...")

        log.info("Hardware initialization process complete.")

    def shutdown(self):
        """
        Safely shuts down all initialized hardware components and disconnects
        from the pigpio daemon.
        """
        log.info("Shutting down hardware components...")

        if self.servos:
            self.servos.off_all()
            log.info("All servos turned off.")

        if self.buzzer:
            self.buzzer.off()
            log.info("Buzzer turned off.")

        # if self.display:
        #     self.display.off()
        #     log.info("Display turned off.")

        if self.pi and self.pi.connected:
            self.pi.stop()
            log.info("Disconnected from pigpiod.")
