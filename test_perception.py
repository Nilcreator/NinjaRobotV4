
import time
import traceback
from ninja_core.config import load_config
from ninja_core.hal import HardwareAbstractionLayer
from ninja_core.perception import DistanceMonitor

def main():
    """
    Initializes the HAL and tests the DistanceMonitor's single-shot and
    continuous measurement modes.
    """
    hal = None
    monitor = None
    try:
        # 1. Initialize
        print("Initializing configuration...")
        config = load_config()

        print("Initializing Hardware Abstraction Layer...")
        hal = HardwareAbstractionLayer(config)
        hal.initialize()

        print("Initializing DistanceMonitor...")
        monitor = DistanceMonitor(hal)

        # 2. Test Single-Shot Measurement
        print("\n--- Testing Single-Shot Measurement ---")
        distance = monitor.get_distance()
        if distance != -1:
            print(f"Measured distance: {distance} mm")
        else:
            print("Failed to get single-shot measurement.")
        time.sleep(1)

        # 3. Test Continuous Measurement
        print("\n--- Testing Continuous Measurement for 5 seconds ---")
        monitor.start_continuous(interval=0.5)

        for i in range(10):
            dist = monitor.get_continuous_distance()
            print(f"Latest continuous distance: {dist} mm")
            time.sleep(0.5)

        print("\nTest complete.")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Shutting down...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        traceback.print_exc()
    finally:
        if monitor:
            print("Stopping continuous monitoring...")
            monitor.stop_continuous()
        if hal:
            print("Shutting down HAL...")
            hal.shutdown()
        print("Cleanup complete.")

if __name__ == "__main__":
    main()
