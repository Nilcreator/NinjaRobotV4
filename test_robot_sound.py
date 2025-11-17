
import time
import traceback
from ninja_core.config import load_config
from ninja_core.hal import HardwareAbstractionLayer
from ninja_core.robot_sound import RobotSoundPlayer

def main():
    """
    Initializes the HAL and cycles through all sounds
    to test the RobotSoundPlayer module.
    """
    hal = None
    try:
        # 1. Initialize Config and HAL
        print("Initializing configuration...")
        config = load_config()

        print("Initializing Hardware Abstraction Layer...")
        hal = HardwareAbstractionLayer(config)
        hal.initialize()

        # 2. Initialize the sound controller
        print("Initializing RobotSoundPlayer...")
        sound_player = RobotSoundPlayer(hal)

        # 3. Get the list of available sounds
        sounds = list(sound_player.SOUNDS.keys())
        print(f"Found sounds: {', '.join(sounds)}")
        time.sleep(1)

        # 4. Cycle through each sound
        for sound in sounds:
            print(f"--> Testing sound: '{sound}'")
            sound_player.play(sound)
            time.sleep(1) # Wait a moment between sounds

        print("\nTest complete.")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Shutting down...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        traceback.print_exc()
    finally:
        if hal:
            print("Shutting down HAL...")
            hal.shutdown()
        print("Cleanup complete.")

if __name__ == "__main__":
    main()
