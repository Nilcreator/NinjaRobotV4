import threading
import time
from .hal import HardwareAbstractionLayer


class DistanceMonitor:
    """
    A class to manage distance measurements from the VL53L0X sensor,
    providing both single-shot and continuous background monitoring.
    """

    def __init__(self, hal: HardwareAbstractionLayer):
        """
        Initializes the DistanceMonitor using the sensor from the HAL.

        Args:
            hal: The initialized HardwareAbstractionLayer object.
        """
        self.sensor = hal.distance_sensor
        self._is_running = False
        self._monitor_thread = None
        self._stop_event = threading.Event()
        self._current_distance = -1
        self._lock = threading.Lock()

    def get_distance(self) -> int:
        """
        Performs a single, blocking distance measurement.

        Returns:
            The measured distance in millimeters, or -1 if the sensor
            is not available.
        """
        if not self.sensor:
            print("Distance sensor is not available in the HAL.")
            return -1
        return self.sensor.get_range()

    def start_continuous(self, interval: float = 0.1):
        """
        Starts monitoring the distance in a background thread.

        If monitoring is already running, this method does nothing.

        Args:
            interval: The time to wait between measurements, in seconds.
        """
        if not self.sensor:
            print("Cannot start continuous monitoring: Distance sensor not available.")
            return

        if self._is_running:
            print("Continuous monitoring is already running.")
            return

        self._is_running = True
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop, args=(interval,)
        )
        self._monitor_thread.daemon = True  # Allow main program to exit
        self._monitor_thread.start()
        print("Continuous distance monitoring started.")

    def stop_continuous(self):
        """
        Stops the background distance monitoring thread.
        """
        if not self._is_running:
            return

        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join()  # Wait for the thread to finish
        self._is_running = False
        print("Continuous distance monitoring stopped.")

    def get_continuous_distance(self) -> int:
        """
        Gets the most recent distance measurement from the background thread.

        This method is non-blocking and returns the last known value.

        Returns:
            The last measured distance in millimeters.
        """
        with self._lock:
            return self._current_distance

    def _monitor_loop(self, interval: float):
        """
        The internal loop that runs in a thread to continuously get readings.
        """
        while not self._stop_event.is_set():
            try:
                distance = self.sensor.get_range()
                with self._lock:
                    self._current_distance = distance
            except Exception as e:
                print(f"Error in distance monitoring loop: {e}")
                # In case of sensor error, stop the loop
                with self._lock:
                    self._current_distance = -1
                break
            time.sleep(interval)
