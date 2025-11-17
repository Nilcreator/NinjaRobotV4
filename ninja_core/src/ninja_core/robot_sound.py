import time
from .hal import HardwareAbstractionLayer


class RobotSoundPlayer:
    """
    A class to play sounds corresponding to robot emotions using a buzzer,
    integrated with the Hardware Abstraction Layer.
    """

    # Note mapping from pi0buzzer (C4-B6)
    NOTES = {
        "c4": 262,
        "d4": 294,
        "e4": 330,
        "f4": 349,
        "g4": 392,
        "a4": 440,
        "b4": 494,
        "c5": 523,
        "d5": 587,
        "e5": 659,
        "f5": 698,
        "g5": 784,
        "a5": 880,
        "b5": 988,
        "c6": 1046,
        "d6": 1175,
        "e6": 1318,
        "f6": 1397,
        "g6": 1568,
        "a6": 1760,
        "b6": 1976,
    }

    SOUNDS = {
        "happy": [("c5", 0.1), ("e5", 0.1), ("g5", 0.1), ("c6", 0.15)],
        "sad": [("b4", 0.4), ("a4", 0.4), ("g4", 0.6)],
        "exciting": [
            ("c6", 0.08),
            ("e6", 0.08),
            ("g6", 0.08),
            ("c6", 0.08),
            ("e6", 0.08),
            ("g6", 0.08),
        ],
        "angry": [("d4", 0.1), ("c4", 0.1), ("d4", 0.1), ("c4", 0.2)],
        "confusing": [("e5", 0.2), ("g4", 0.2), ("c5", 0.3)],
        "cry": [("e5", 0.3), ("d5", 0.2), ("c5", 0.5), ("pause", 0.2), ("c5", 0.4)],
        "embarrassing": [("a4", 0.15), ("g4", 0.15), ("a4", 0.3)],
        "idle": [("c5", 0.1), ("pause", 0.5), ("c5", 0.1)],
        "laughing": [("g5", 0.1), ("pause", 0.05)] * 5,
        "scary": [("c4", 0.5), ("d4", 0.2), ("c4", 0.5)],
        "shy": [("c5", 0.1), ("e5", 0.3), ("c5", 0.1), ("e5", 0.4)],
        "sleepy": [("g4", 0.5), ("f4", 0.5), ("e4", 0.7)],
        "speaking": [("c5", 0.1), ("d5", 0.1), ("e5", 0.1)] * 3,
        "surprising": [("g6", 0.3)],
    }

    def __init__(self, hal: HardwareAbstractionLayer):
        """
        Initializes the RobotSoundPlayer using the buzzer from the HAL.

        Args:
            hal: The initialized HardwareAbstractionLayer object.
        """
        self.buzzer = hal.buzzer

    def play(self, emotion: str):
        """
        Plays the sound for the given emotion.
        """
        if not self.buzzer:
            print("Buzzer is not available in the HAL.")
            return

        if emotion not in self.SOUNDS:
            print(f"Unknown emotion: {emotion}")
            return

        melody = self.SOUNDS[emotion]
        print(f"Playing sound for: {emotion}")

        for note_name, duration in melody:
            if note_name == "pause":
                time.sleep(duration)
                continue

            frequency = self.NOTES.get(note_name)
            if frequency:
                # The buzzer driver handles the timing, so we just call it.
                self.buzzer.play_sound(frequency, duration)
                # A brief pause between notes to make them distinct
                time.sleep(0.01)
            else:
                print(f"Warning: Note '{note_name}' not found.")
