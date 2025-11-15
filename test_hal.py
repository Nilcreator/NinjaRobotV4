# test_hal.py
import time
import logging
from ninja_core.config import load_config
from ninja_core.hal import HardwareAbstractionLayer

# Set up basic logging to see output from the HAL and the test script.
# This helps in debugging and verifying each step.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def run_hal_test():
    """
    Tests the complete workflow from loading configuration to initializing
    and using the Hardware Abstraction Layer (HAL).
    """
    logging.info("--- Starting HAL Test ---")
    hal = None  # Ensure 'hal' is defined in the outer scope for the finally block

    try:
        # Step 1: Load the master configuration from config.json
        # This file should have been created by the 'ninja_core config import-all' command.
        config = load_config()
        logging.info("Master configuration loaded successfully.")

        # Step 2: Create an instance of the HAL and initialize it.
        # This will connect to pigpio and set up all hardware drivers.
        hal = HardwareAbstractionLayer(config)
        hal.initialize()
        logging.info("Hardware Abstraction Layer initialized successfully.")

        # Step 3: Test hardware components through the HAL to verify functionality.
        if hal.servos:
            logging.info("Testing servo movement via HAL...")
            # Command all configured servos to move to their center position.
            hal.servos.move_all_angles({"all": 0})
            logging.info("Commanded all servos to center (0 degrees).")
            time.sleep(2)  # Wait 2 seconds for the servos to complete their movement.
        else:
            logging.warning("No servos found in HAL, skipping servo test.")

        if hal.buzzer:
            logging.info("Testing buzzer via HAL...")
            # Play a short A4 note (440 Hz) for 0.5 seconds.
            hal.buzzer.play_sound(440, 0.5)
            time.sleep(1) # Wait for the sound to finish.
        else:
            logging.warning("No buzzer found in HAL, skipping buzzer test.")

        logging.info("Hardware tests completed successfully!")

    except Exception as e:
        logging.error(f"An error occurred during the HAL test: {e}", exc_info=True)
    finally:
        # Step 4: Safely shut down all hardware components.
        # This is crucial to release hardware resources properly.
        if hal:
            hal.shutdown()
        logging.info("--- HAL Test Finished ---")

if __name__ == "__main__":
    run_hal_test()
