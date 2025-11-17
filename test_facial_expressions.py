import time
from ninja_core.config import NinjaConfig
from ninja_core.hal import HardwareAbstractionLayer
from ninja_core.facial_expressions import AnimatedFaces


def main():
    """
    Initializes the HAL and cycles through all facial expressions
    to test the AnimatedFaces module.
    """
    config = None
    hal = None
    face_controller = None
    try:
        # 1. Initialize Config and HAL
        print("Initializing configuration...")
        config = NinjaConfig.load()

        print("Initializing Hardware Abstraction Layer...")
        hal = HardwareAbstractionLayer(config)
        hal.initialize()

        # 2. Initialize the face animation controller
        print("Initializing AnimatedFaces...")
        face_controller = AnimatedFaces(hal)

        # 3. Get the list of available expressions
        expressions = list(face_controller.animations.keys())
        print(f"Found expressions: {', '.join(expressions)}")

        # 4. Cycle through each expression
        for expression in expressions:
            if expression == "idle":  # Skip idle for this test
                continue

            print(f"--> Testing expression: '{expression}' for 3 seconds...")
            face_controller.play(expression, duration_s=3.0)
            time.sleep(3.5)  # Wait for the animation to play + a small buffer

        # 5. Play idle animation at the end
        print("--> Testing expression: 'idle' (infinite loop)...")
        face_controller.play("idle", duration_s=float("inf"))
        print("Test complete. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Shutting down...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        if face_controller:
            print("Stopping face animation thread...")
            face_controller.stop()
        if hal:
            print("Shutting down HAL...")
            hal.shutdown()
        print("Cleanup complete.")


if __name__ == "__main__":
    main()
