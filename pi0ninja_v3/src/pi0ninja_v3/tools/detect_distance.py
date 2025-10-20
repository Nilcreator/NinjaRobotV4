
import pigpio
import time
import sys
import select
import tty
import termios
import os

# Add the parent directory to the path to find the vl53l0x_pigpio library
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from vl53l0x_pigpio import VL53L0X



def main():
    """Main function to run the interactive distance detector."""
    detector = DistanceDetector()
    if not detector.pi:
        return

    try:
        while True:
            print("\n--- Distance Detector Menu ---")
            print("1. Timed Detection")
            print("2. Continuous Detection")
            print("----------------------------")
            choice = input("Choose an option (or 'q' to quit): ")

            if choice == '1':
                try:
                    count = int(input("Enter number of measurements (e.g., 5): "))
                    delay = float(input("Enter delay between measurements in seconds (e.g., 1.0): "))
                    detector.timed_detection(count, delay)
                except ValueError:
                    print("Invalid input. Please enter numbers for count and delay.")
            elif choice == '2':
                detector.continuous_detection()
            elif choice.lower() == 'q':
                break
            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("\nCaught interrupt, shutting down.")
    finally:
        detector.cleanup()

if __name__ == '__main__':
    main()
