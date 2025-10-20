import time
import json
import pigpio
import threading
from PIL import Image, ImageDraw, ImageFont

# Import drivers
from piservo0 import MultiServo
from pi0disp import ST7789V
from pi0buzzer.driver import Buzzer
from vl53l0x_pigpio import VL53L0X
from pi0ninja_v3.facial_expressions import AnimatedFaces
from pi0ninja_v3.robot_sound import RobotSoundPlayer

# --- Configuration File Paths ---
CONFIG_FILE = 'config.json'

def load_config():
    """Loads servo and buzzer pins from the JSON file."""
    print(f"Loading configuration from {CONFIG_FILE}...")
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        servo_pins = [servo['pin'] for servo in config['servo']]
        print(f"Found servo pins: {servo_pins}")
        buzzer_pin = config['buzzer']['pin']
        print(f"Found buzzer pin: {buzzer_pin}")
        return servo_pins, buzzer_pin
    except (FileNotFoundError, KeyError) as e:
        print(f"Error reading config: {e}. Aborting.")
        return None, None

def main():
    """
    Main function to control the NinjaRobotV3 components.
    """
    print("Initializing NinjaRobotV3...")

    # --- Load Configuration ---
    servo_pins, buzzer_pin = load_config()
    if not servo_pins or not buzzer_pin:
        return

    pi = None
    lcd = None
    servos = None
    tof = None
    buzzer = None

    try:
        # --- Initialize pigpio ---
        pi = pigpio.pi()
        if not pi.connected:
            raise RuntimeError("Could not connect to the pigpio daemon. Is it running?")

        # --- Initialize Modules ---
        print("Initializing display...")
        lcd = ST7789V()

        print("Initializing servos...")
        servos = MultiServo(pi, servo_pins, conf_file=CONFIG_FILE, first_move=False)

        print("Initializing buzzer...")
        buzzer = Buzzer(pi, buzzer_pin, config_file=CONFIG_FILE)

        print("Initializing sound player...")
        sound_player = RobotSoundPlayer()

        print("Initializing distance sensor...")
        tof = VL53L0X(pi)

        # --- Robot Actions ---

        # 1. Test Animated Facial Expressions with Sound
        print("Testing animated facial expressions with sound...")
        faces = AnimatedFaces(lcd)

        # List of all emotions to play
        emotions = [
            'idle', 'happy', 'laughing', 'sad', 'cry', 'angry', 'surprising',
            'sleepy', 'speaking', 'shy', 'embarrassing', 'scary', 'exciting', 'confusing'
        ]

        for emotion in emotions:
            animation_method = getattr(faces, f"play_{emotion}")
            
            # Play sound in a separate thread to run concurrently with animation
            sound_thread = threading.Thread(target=sound_player.play, args=(emotion,))
            sound_thread.start()
            
            # Play the animation (this is a blocking call for its duration)
            animation_method(duration_s=3)
            
            time.sleep(0.5) # Pause between expressions

        print("Facial expression test complete.")
        # Revert to a neutral face for the next steps
        faces.play_idle(duration_s=1)

        # 2. Play a startup sound
        print("Playing greeting music...")
        buzzer.play_hello() # Play 440 Hz for 0.5 seconds
        time.sleep(0.5)

        # 3. Initialize servos with a sweep
        print("Setting initial servo positions...")
        num_servos = len(servo_pins)
        servos.move_all_angles([0] * num_servos)
        time.sleep(1)

        print("Sweeping all servos...")
        servos.move_all_angles_sync([-90] * num_servos, move_sec=1.0)
        time.sleep(0.5)
        servos.move_all_angles_sync([90] * num_servos, move_sec=1.0)
        time.sleep(0.5)
        print("Centering servos...")
        servos.move_all_angles_sync([0] * num_servos, move_sec=0.5)
        time.sleep(1)

        # 4. Measure and display distance
        print("Measuring distance...")
        image = Image.new("RGB", (lcd.width, lcd.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        distance = tof.get_range()
        
        draw.rectangle((0, 200, lcd.width, lcd.height), fill="navy")
        if distance > 0:
            dist_text = f"Dist: {distance} mm"
            print(dist_text)
            draw.text((30, 220), dist_text, fill="cyan", font=font)
        else:
            print("Distance: Out of range")
            draw.text((30, 220), "Out of range", fill="orange", font=font)
        
        lcd.display(image)
        time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # --- Cleanup ---
        print("\nCleaning up resources...")
        if sound_player:
            sound_player.cleanup()
        if servos:
            servos.off()
        if lcd:
            lcd.close()
        if tof:
            tof.close()
        if buzzer:
            buzzer.off()
        if pi and pi.connected:
            pi.stop()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
