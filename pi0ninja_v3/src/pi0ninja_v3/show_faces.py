import inspect
import time
from PIL import Image
from pi0disp.disp.st7789v import ST7789V
from pi0ninja_v3.facial_expressions import AnimatedFaces

def get_face_methods(animated_faces_instance):
    """Inspects the AnimatedFaces instance and returns a dictionary of face-playing methods."""
    face_methods = {}
    for name, method in inspect.getmembers(animated_faces_instance, predicate=inspect.ismethod):
        if name.startswith('play_'):
            clean_name = name.replace('play_', '')
            face_methods[clean_name] = method
    return face_methods

def main():
    """Main function to display facial expressions using a simple blocking menu."""
    lcd = None
    faces = None
    try:
        lcd = ST7789V()
        faces = AnimatedFaces(lcd)
        face_options = get_face_methods(faces)
        option_list = list(face_options.keys())

        # Start with the idle animation running in the background
        faces.play_idle()
        
        while True:
            print("\n--- Select a Facial Expression ---")
            for i, name in enumerate(option_list):
                print(f"{i + 1}. {name}")
            print("Enter 'q' to quit.")
            
            choice = input("Your choice: ").strip().lower()

            if choice == 'q':
                print("\nExiting...")
                break

            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(option_list):
                    selected_face_name = option_list[choice_index]
                    
                    # The AnimatedFaces class handles stopping the old animation
                    # and starting the new one.
                    print(f"\nDisplaying: {selected_face_name} for 5 seconds...")
                    face_options[selected_face_name](duration_s=5)
                    
                    # Wait for the animation to finish.
                    # The animation runs in a background thread, so we just sleep
                    # in the main thread.
                    time.sleep(5)

                    print("Returning to idle...")
                    faces.play_idle()
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q'.")

    except KeyboardInterrupt:
        print("\nExiting due to Ctrl+C...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if faces:
            faces.stop() # Cleanly stop the animation thread
        if lcd:
            # Create a blank image to clear the screen on exit
            blank_image = Image.new("RGB", (lcd.width, lcd.height), "black")
            lcd.display(blank_image)
            lcd.close()

if __name__ == "__main__":
    main()
