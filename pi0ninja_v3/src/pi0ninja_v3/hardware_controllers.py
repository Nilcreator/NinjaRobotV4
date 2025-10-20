import json
import os
import time
import pigpio
import sys
import select
import termios
import tty
import math
import threading
from PIL import Image, ImageDraw, ImageFont

from piservo0.core.calibrable_servo import CalibrableServo
from pi0disp.disp.st7789v import ST7789V
from pi0buzzer.driver import Buzzer
from vl53l0x_pigpio import VL53L0X

# --- Configuration and Setup ---
NINJA_ROBOT_V3_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_FILE = os.path.join(NINJA_ROBOT_V3_ROOT, "pi0ninja_v3", "config.json")
MOVEMENTS_FILE = os.path.join(NINJA_ROBOT_V3_ROOT, "servo_movement.json")

class ServoController:
    """A custom controller to manage multiple servos based on config.json."""
    def __init__(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise IOError("Failed to connect to pigpiod.")
        
        self.servos = {}
        self.servo_definitions = {}
        self._initialize_servos()

    def _initialize_servos(self):
        """Loads servo definitions, initializes CalibrableServo objects, and centers them."""
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                servo_configs = config.get("servos", [])
            
            print("Initializing and centering servos...")
            for config in servo_configs:
                pin = config['pin']
                servo = CalibrableServo(
                    self.pi,
                    pin,
                    conf_file=CONFIG_FILE
                )
                self.servos[pin] = servo
                self.servo_definitions[pin] = config
                
                # Set initial position to center to activate the servo
                servo.move_center()
                print(f"Initialized and centered servo on pin {pin}")
            
            # Give servos time to reach the center position
            time.sleep(0.5)
            print("All servos centered.")

        except FileNotFoundError:
            raise RuntimeError(f"Error: {CONFIG_FILE} not found.")
        except Exception as e:
            raise RuntimeError(f"Error initializing servos: {e}")

    def get_servo_definitions(self):
        """Returns the raw servo definitions from the JSON file."""
        return self.servo_definitions

    def move_servos(self, movements, speed='M'):
        """
        Executes a set of servo movements with smooth interpolation.
        The duration of the movement is determined by the 'speed' parameter.
        """
        duration_map = {'S': 1.0, 'M': 0.5, 'F': 0.2}
        duration = duration_map.get(speed, 0.5)

        # Get current and target angles for interpolation
        pins_to_move = [int(p) for p in movements.keys()]
        current_angles = {p: self.servos[p].get_angle() for p in pins_to_move if p in self.servos}
        target_angles = {int(p): a for p, a in movements.items()}

        steps = int(duration / 0.02)  # 50 FPS update rate
        if steps <= 0:
            steps = 1

        for i in range(1, steps + 1):
            ratio = i / steps
            for pin in pins_to_move:
                if pin in self.servos:
                    start_angle = current_angles.get(pin, 0)
                    end_angle = target_angles.get(pin, 0)
                    
                    new_angle = start_angle + (end_angle - start_angle) * ratio
                    self.servos[pin].move_angle(new_angle)
            time.sleep(0.02)

        # Ensure final position is set accurately
        for pin in pins_to_move:
            if pin in self.servos:
                self.servos[pin].move_angle(target_angles.get(pin, 0))

    def get_current_angles(self):
        """Returns a dictionary of {pin: current_angle}."""
        return {pin: servo.get_angle() for pin, servo in self.servos.items()}

    def center_all_servos(self):
        """Moves all servos to their center position."""
        print("Centering all servos...")
        for servo in self.servos.values():
            servo.move_center()
        time.sleep(0.5)

    def cleanup(self):
        """Turns off all servos and disconnects from pigpio."""
        print("Cleaning up resources.")
        for servo in self.servos.values():
            servo.off()
        self.pi.stop()

class AnimatedFaces:
    """
    Generates and displays programmatically drawn, animated facial expressions
    based on a unified design style. This class is thread-safe.
    """

    def __init__(self, lcd: ST7789V):
        self.lcd = lcd
        self.width, self.height = lcd.width, lcd.height
        self.bg_color = "black"
        self.face_color = "white"
        self.blush_color = "#FF69B4"
        self.tear_color = "#00BFFF"

        # Threading control
        self._animation_thread = None
        self._stop_event = threading.Event()

        # Style guide
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.eye_y = self.center_y - 35
        self.mouth_y = self.center_y + 50
        self.eye_offset = 60
        self.eye_radius = 45
        self.pupil_radius = 20
        self.line_width = 12

        try:
            self.font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 50)
        except IOError:
            self.font = ImageFont.load_default()

    def _get_blank_image(self):
        return Image.new("RGB", (self.width, self.height), self.bg_color)

    def _animation_loop(self, duration_s, frame_logic):
        """The actual loop that runs in a thread to draw frames."""
        start_time = time.time()
        while not self._stop_event.is_set() and (time.time() - start_time < duration_s):
            image = self._get_blank_image()
            draw = ImageDraw.Draw(image)
            frame_logic(draw, time.time() - start_time)
            self.lcd.display(image)
            time.sleep(1/60) # ~60 FPS

    def _start_animation(self, duration_s, frame_logic):
        """Stops any running animation and starts a new one."""
        self.stop() # Safely stop the previous thread

        self._stop_event.clear()
        self._animation_thread = threading.Thread(
            target=self._animation_loop, 
            args=(duration_s, frame_logic)
        )
        self._animation_thread.start()

    def stop(self):
        """Stops the current animation thread and waits for it to exit."""
        if self._animation_thread and self._animation_thread.is_alive():
            self._stop_event.set()
            self._animation_thread.join()

    # --- Base Drawing Helpers ---

    def _draw_base_eyes(self, draw, left_pupil_shift=(0, 0), right_pupil_shift=(0, 0)):
        lx, ly = self.center_x - self.eye_offset, self.eye_y
        draw.ellipse([lx - self.eye_radius, ly - self.eye_radius, lx + self.eye_radius, ly + self.eye_radius], fill=self.face_color)
        lpx, lpy = lx + left_pupil_shift[0], ly + left_pupil_shift[1]
        draw.ellipse([lpx - self.pupil_radius, lpy - self.pupil_radius, lpx + self.pupil_radius, lpy + self.pupil_radius], fill=self.bg_color)

        rx, ry = self.center_x + self.eye_offset, self.eye_y
        draw.ellipse([rx - self.eye_radius, ry - self.eye_radius, rx + self.eye_radius, ry + self.eye_radius], fill=self.face_color)
        rpx, rpy = rx + right_pupil_shift[0], ry + right_pupil_shift[1]
        draw.ellipse([rpx - self.pupil_radius, rpy - self.pupil_radius, rpx + self.pupil_radius, rpy + self.pupil_radius], fill=self.bg_color)

    def _draw_happy_base(self, draw):
        self._draw_base_eyes(draw)
        eyebrow_y = self.eye_y - self.eye_radius - (self.line_width / 2) - 5
        draw.arc([self.center_x - self.eye_offset - 40, eyebrow_y - 40, self.center_x - self.eye_offset + 40, eyebrow_y], 0, 180, fill=self.face_color, width=self.line_width)
        draw.arc([self.center_x + self.eye_offset - 40, eyebrow_y - 40, self.center_x + self.eye_offset + 40, eyebrow_y], 0, 180, fill=self.face_color, width=self.line_width)
        draw.arc([self.center_x - 70, self.mouth_y - 50, self.center_x + 70, self.mouth_y + 50], 0, 180, fill=self.face_color)

    def _draw_sad_base(self, draw):
        pupil_shift = (0, 15)
        self._draw_base_eyes(draw, pupil_shift, pupil_shift)
        draw.line([self.center_x - self.eye_offset - 30, self.eye_y - 50, self.center_x - self.eye_offset + 10, self.eye_y - 70], fill=self.face_color, width=self.line_width)
        draw.line([self.center_x + self.eye_offset + 30, self.eye_y - 50, self.center_x + self.eye_offset - 10, self.eye_y - 70], fill=self.face_color, width=self.line_width)
        draw.arc([self.center_x - 60, self.mouth_y + 20, self.center_x + 60, self.mouth_y + 80], 180, 360, fill=self.face_color)

    # --- Animation Methods ---

    def play_idle(self, duration_s=float('inf')):
        print("Playing: Idle")
        def logic(draw, t):
            blink_cycle = (t * 2) % 3
            if blink_cycle < 0.15:
                draw.line([self.center_x - self.eye_offset - 30, self.eye_y, self.center_x - self.eye_offset + 30, self.eye_y], fill=self.face_color, width=self.line_width)
                draw.line([self.center_x + self.eye_offset - 30, self.eye_y, self.center_x + self.eye_offset + 30, self.eye_y], fill=self.face_color, width=self.line_width)
            else:
                self._draw_base_eyes(draw)
            draw.arc([self.center_x - 50, self.mouth_y - 10, self.center_x + 50, self.mouth_y + 10], 0, 180, fill=self.face_color)
        self._start_animation(duration_s, logic)

    def play_happy(self, duration_s=3):
        print("Playing: Happy")
        def logic(draw, t):
            self._draw_happy_base(draw)
        self._start_animation(duration_s, logic)

    def play_laughing(self, duration_s=3):
        print("Playing: Laughing")
        def logic(draw, t):
            self._draw_happy_base(draw)
            mouth_height = abs(math.sin(t * 15)) * 60
            draw.rectangle([self.center_x - 70, self.mouth_y, self.center_x + 70, self.mouth_y + mouth_height], fill=self.bg_color)
        self._start_animation(duration_s, logic)

    def play_sad(self, duration_s=3):
        print("Playing: Sad")
        def logic(draw, t):
            self._draw_sad_base(draw)
        self._start_animation(duration_s, logic)

    def play_cry(self, duration_s=3):
        print("Playing: Cry")
        def logic(draw, t):
            self._draw_sad_base(draw)
            tear_y_base = self.eye_y + self.eye_radius
            tear_length = self.height - tear_y_base
            for i in range(3):
                tear_y = tear_y_base + (t * 200 + i * 40) % tear_length
                draw.line([self.center_x - self.eye_offset, tear_y, self.center_x - self.eye_offset, tear_y + 30], fill=self.tear_color, width=self.line_width)
        self._start_animation(duration_s, logic)

    def play_angry(self, duration_s=3):
        print("Playing: Angry")
        def logic(draw, t):
            shake = math.sin(t * 20) * 3
            self._draw_base_eyes(draw)
            draw.line([self.center_x - self.eye_offset - 40, self.eye_y - 30 + shake, self.center_x - self.eye_offset + 40, self.eye_y - 70 + shake], fill=self.face_color, width=self.line_width)
            draw.line([self.center_x + self.eye_offset + 40, self.eye_y - 30 + shake, self.center_x + self.eye_offset - 40, self.eye_y - 70 + shake], fill=self.face_color, width=self.line_width)
            draw.arc([self.center_x - 70, self.mouth_y - 20, self.center_x + 70, self.mouth_y + 80], 180, 360, fill=self.face_color)
        self._start_animation(duration_s, logic)

    def play_surprising(self, duration_s=3):
        print("Playing: Surprising")
        def logic(draw, t):
            open_factor = min(1, t * 4)
            pupil_radius_factor = 1 - (open_factor * 0.5)
            current_pupil_radius = self.pupil_radius * pupil_radius_factor
            lx, ly = self.center_x - self.eye_offset, self.eye_y
            draw.ellipse([lx - self.eye_radius, ly - self.eye_radius, lx + self.eye_radius, ly + self.eye_radius], fill=self.face_color)
            draw.ellipse([lx - current_pupil_radius, ly - current_pupil_radius, lx + current_pupil_radius, ly + current_pupil_radius], fill=self.bg_color)
            rx, ry = self.center_x + self.eye_offset, self.eye_y
            draw.ellipse([rx - self.eye_radius, ry - self.eye_radius, rx + self.eye_radius, ry + self.eye_radius], fill=self.face_color)
            draw.ellipse([rx - current_pupil_radius, ry - current_pupil_radius, rx + current_pupil_radius, ry + current_pupil_radius], fill=self.bg_color)
            mouth_radius = min(50, t * 120)
            draw.ellipse([self.center_x - mouth_radius, self.mouth_y - mouth_radius, self.center_x + mouth_radius, self.mouth_y + mouth_radius], fill=self.face_color)
        self._start_animation(duration_s, logic)

    def play_sleepy(self, duration_s=3):
        print("Playing: Sleepy")
        def logic(draw, t):
            open_factor = (math.cos(t * 1.5) + 1) / 2 * 0.9 + 0.05
            ly, ry = self.eye_y, self.eye_y
            draw.arc([self.center_x - self.eye_offset - self.eye_radius, ly - self.eye_radius, self.center_x - self.eye_offset + self.eye_radius, ly + self.eye_radius], 180, 360, fill=self.face_color)
            draw.arc([self.center_x + self.eye_offset - self.eye_radius, ry - self.eye_radius, self.center_x + self.eye_offset + self.eye_radius, ry + self.eye_radius], 180, 360, fill=self.face_color)
            draw.arc([self.center_x - self.eye_offset - self.eye_radius, ly - self.eye_radius, self.center_x - self.eye_offset + self.eye_radius, ly + self.eye_radius], 0, 180, fill=self.face_color, width=self.line_width)
            draw.arc([self.center_x + self.eye_offset - self.eye_radius, ry - self.eye_radius, self.center_x + self.eye_offset + self.eye_radius, ry + self.eye_radius], 0, 180, fill=self.face_color, width=self.line_width)
            draw.rectangle([0, self.eye_y - self.eye_radius, self.width, self.eye_y - self.eye_radius + (self.eye_radius*2)*(1-open_factor)], fill=self.bg_color)
            draw.arc([self.center_x - 20, self.mouth_y - 10, self.center_x + 20, self.mouth_y + 10], 0, 360, fill=self.face_color)
        self._start_animation(duration_s, logic)

    def play_speaking(self, duration_s=3):
        print("Playing: Speaking")
        def logic(draw, t):
            self._draw_base_eyes(draw)
            mouth_height = (math.sin(t * 15) + 1) / 2 * 40 + 10
            draw.ellipse([self.center_x - 50, self.mouth_y, self.center_x + 50, self.mouth_y + mouth_height], fill=self.face_color)
        self._start_animation(duration_s, logic)

    def play_shy(self, duration_s=3):
        print("Playing: Shy")
        def logic(draw, t):
            pupil_shift = (-20, 15)
            self._draw_base_eyes(draw, pupil_shift, pupil_shift)
            blush_y = self.eye_y + self.eye_radius / 2
            blush_radius = 25
            draw.ellipse([self.center_x - self.eye_offset - 15, blush_y, self.center_x - self.eye_offset + 35, blush_y + blush_radius], fill=self.blush_color)
            draw.ellipse([self.center_x + self.eye_offset - 35, blush_y, self.center_x + self.eye_offset + 15, blush_y + blush_radius], fill=self.blush_color)
            points = [self.center_x - 40, self.mouth_y+10, self.center_x - 20, self.mouth_y, self.center_x, self.mouth_y+10, self.center_x + 20, self.mouth_y, self.center_x + 40, self.mouth_y+10]
            draw.line(points, fill=self.face_color, width=self.line_width-2, joint="curve")
        self._start_animation(duration_s, logic)

    def play_embarrassing(self, duration_s=3):
        self.play_shy(duration_s)

    def play_scary(self, duration_s=3):
        print("Playing: Scary")
        def logic(draw, t):
            current_pupil_radius = 10
            shake = math.sin(t * 50) * 4
            lx, ly = self.center_x - self.eye_offset, self.eye_y
            draw.ellipse([lx - self.eye_radius, ly - self.eye_radius, lx + self.eye_radius, ly + self.eye_radius], fill=self.face_color)
            lpx, lpy = lx, ly + shake
            draw.ellipse([lpx - current_pupil_radius, lpy - current_pupil_radius, lpx + current_pupil_radius, lpy + current_pupil_radius], fill=self.bg_color)
            rx, ry = self.center_x + self.eye_offset, self.eye_y
            draw.ellipse([rx - self.eye_radius, ry - self.eye_radius, rx + self.eye_radius, ry + self.eye_radius], fill=self.face_color)
            rpx, rpy = rx, ry + shake
            draw.ellipse([rpx - current_pupil_radius, rpy - current_pupil_radius, rpx + current_pupil_radius, rpy + current_pupil_radius], fill=self.bg_color)
            draw.arc([self.center_x - 70, self.mouth_y - 20, self.center_x + 70, self.mouth_y + 80], 180, 360, fill=self.face_color)
        self._start_animation(duration_s, logic)

    def play_exciting(self, duration_s=3):
        print("Playing: Exciting")
        def logic(draw, t):
            star_points = 10
            for eye_center_x in [self.center_x - self.eye_offset, self.center_x + self.eye_offset]:
                angle = math.pi * 2 / star_points
                points = []
                for i in range(star_points):
                    r = self.eye_radius if i % 2 == 0 else self.eye_radius / 2
                    points.append((eye_center_x + r * math.cos(angle * i + t*10), self.eye_y + r * math.sin(angle * i + t*10)))
                draw.polygon(points, fill=self.face_color)
            draw.arc([self.center_x - 70, self.mouth_y - 50, self.center_x + 70, self.mouth_y + 50], 0, 180, fill=self.face_color)
        self._start_animation(duration_s, logic)

    def play_confusing(self, duration_s=3):
        print("Playing: Confusing")
        def logic(draw, t):
            self._draw_base_eyes(draw, (-15, 0), (15, 0))
            draw.arc([self.center_x - self.eye_offset - 40, self.eye_y - 90, self.center_x - self.eye_offset + 40, self.eye_y - 10], 0, 180, fill=self.face_color, width=self.line_width)
            points = [self.center_x - 50, self.mouth_y+10, self.center_x - 25, self.mouth_y-10, self.center_x, self.mouth_y+10, self.center_x + 25, self.mouth_y-10, self.center_x + 50, self.mouth_y+10]
            draw.line(points, fill=self.face_color, width=self.line_width-2, joint="curve")
            if t > 0.5:
                draw.text((self.center_x + self.eye_offset + 10, self.eye_y - 100), "?", font=self.font, fill=self.face_color)

class RobotSoundPlayer:
    """
    A class to play sounds corresponding to robot emotions using a buzzer.
    """
    # Note mapping from pi0buzzer (C4-B6)
    NOTES = {
        'c4': 262, 'd4': 294, 'e4': 330, 'f4': 349, 'g4': 392, 'a4': 440, 'b4': 494,
        'c5': 523, 'd5': 587, 'e5': 659, 'f5': 698, 'g5': 784, 'a5': 880, 'b5': 988,
        'c6': 1046, 'd6': 1175, 'e6': 1318, 'f6': 1397, 'g6': 1568, 'a6': 1760, 'b6': 1976,
    }

    SOUNDS = {
        "happy": [('c5', 0.1), ('e5', 0.1), ('g5', 0.1), ('c6', 0.15)],
        "sad": [('b4', 0.4), ('a4', 0.4), ('g4', 0.6)],
        "exciting": [('c6', 0.08), ('e6', 0.08), ('g6', 0.08), ('c6', 0.08), ('e6', 0.08), ('g6', 0.08)],
        "angry": [('d4', 0.1), ('c4', 0.1), ('d4', 0.1), ('c4', 0.2)],
        "confusing": [('e5', 0.2), ('g4', 0.2), ('c5', 0.3)],
        "cry": [('e5', 0.3), ('d5', 0.2), ('c5', 0.5), ('pause', 0.2), ('c5', 0.4)],
        "embarrassing": [('a4', 0.15), ('g4', 0.15), ('a4', 0.3)],
        "idle": [('c5', 0.1), ('pause', 0.5), ('c5', 0.1)],
        "laughing": [('g5', 0.1), ('pause', 0.05)] * 5,
        "scary": [('c4', 0.5), ('d4', 0.2), ('c4', 0.5)],
        "shy": [('c5', 0.1), ('e5', 0.3), ('c5', 0.1), ('e5', 0.4)],
        "sleepy": [('g4', 0.5), ('f4', 0.5), ('e4', 0.7)],
        "speaking": [('c5', 0.1), ('d5', 0.1), ('e5', 0.1)] * 3,
        "surprising": [('g6', 0.3)],
    }

    def __init__(self):
        """
        Initializes the RobotSoundPlayer.
        """
        try:
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise IOError("Could not connect to pigpio daemon.")
        except Exception as e:
            print(f"Error initializing pigpio: {e}")
            self.pi = None
            return

        try:
            # Assumes config.json is in the pi0ninja_v3 directory
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.json'))
            with open(config_path, 'r') as f:
                config = json.load(f)
                pin = config['buzzer']['pin']
            self.buzzer = Buzzer(self.pi, pin)
        except FileNotFoundError:
            print("Error: config.json not found.")
            self.buzzer = None
        except Exception as e:
            print(f"Error initializing buzzer: {e}")
            self.buzzer = None

    def play(self, emotion: str):
        """
        Plays the sound for the given emotion.
        """
        if not self.buzzer:
            print("Buzzer is not initialized.")
            return

        if emotion not in self.SOUNDS:
            print(f"Unknown emotion: {emotion}")
            return

        melody = self.SOUNDS[emotion]
        print(f"Playing sound for: {emotion}")

        for note_name, duration in melody:
            if note_name == 'pause':
                time.sleep(duration)
                continue

            frequency = self.NOTES.get(note_name)
            if frequency:
                self.buzzer.play_sound(frequency, duration)
                time.sleep(0.01)  # Brief pause between notes
            else:
                print(f"Warning: Note '{note_name}' not found.")
        
    def cleanup(self):
        """
        Cleans up resources.
        """
        if self.buzzer:
            self.buzzer.off()
        if self.pi and self.pi.connected:
            self.pi.stop()
        print("\nRobot Sound Player shutting down.")
class DistanceDetector:
    """
    A class to detect distance using the VL53L0X sensor.
    """
    def __init__(self):
        try:
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise IOError("Could not connect to pigpio daemon.")
        except Exception as e:
            print(f"Error initializing pigpio: {e}", file=sys.stderr)
            self.pi = None

    def timed_detection(self, count: int, delay: float):
        """
        Performs a specified number of distance measurements with a delay.
        """
        if not self.pi:
            return

        print(f"Starting timed detection: {count} measurements, {delay}s delay...")
        try:
            with VL53L0X(self.pi) as tof:
                for i in range(count):
                    distance = tof.get_range()
                    if distance > 0:
                        print(f"Measurement {i + 1}/{count}: {distance} mm")
                    else:
                        print(f"Measurement {i + 1}/{count}: Out of range")
                    time.sleep(delay)
        except Exception as e:
            print(f"An error occurred during timed detection: {e}", file=sys.stderr)

    def continuous_detection(self):
        """
        Performs continuous distance measurement at 5Hz until 'q' is pressed.
        """
        if not self.pi:
            return

        print("Starting continuous detection at 5Hz. Press 'q' to quit.")
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(sys.stdin.fileno())
            with VL53L0X(self.pi) as tof:
                while True:
                    # Check for user input
                    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                        if sys.stdin.read(1) == 'q':
                            break

                    distance = tof.get_range()
                    if distance > 0:
                        # Use carriage return to print on the same line
                        print(f"Distance: {distance:4d} mm", end="\r")
                    else:
                        print("Distance: Out of range", end="\r")
                    
                    time.sleep(0.2) # 5Hz

        except Exception as e:
            print(f"An error occurred during continuous detection: {e}", file=sys.stderr)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            print("\nStopping continuous detection.")

    def cleanup(self):
        if self.pi and self.pi.connected:
            self.pi.stop()
