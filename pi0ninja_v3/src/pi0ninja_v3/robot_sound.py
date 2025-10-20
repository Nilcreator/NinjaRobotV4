
import os
import sys

# Add the parent directory to the path to find the pi0buzzer library
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))




def main():
    """
    Main function to run the interactive sound player.
    """
    player = RobotSoundPlayer()
    if not player.pi or not player.buzzer:
        return # Initialization failed

    emotions = sorted(list(player.SOUNDS.keys()))

    try:
        while True:
            print("\n--- Robot Emotion Sound Menu ---")
            for i, emotion in enumerate(emotions, 1):
                print(f"{i}. {emotion.capitalize()}")
            print("---------------------------------")
            choice = input("Enter a number to play a sound, or 'q' to quit: ")

            if choice.lower() == 'q':
                break
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(emotions):
                    player.play(emotions[index])
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q'.")

    except KeyboardInterrupt:
        print("\nCaught interrupt, shutting down.")
    finally:
        player.cleanup()

if __name__ == "__main__":
    main()
