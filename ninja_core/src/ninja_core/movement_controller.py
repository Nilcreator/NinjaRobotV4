import time
from ninja_core.hal import HardwareAbstractionLayer
from ninja_core.config import NinjaConfig


class MovementController:
    """A controller to manage and execute complex, multi-servo movement sequences."""

    def __init__(self, hal: HardwareAbstractionLayer, config: NinjaConfig):
        """
        Initializes the MovementController.

        Args:
            hal: The HardwareAbstractionLayer instance.
            config: The NinjaConfig instance for loading settings.
        """
        self.servos = hal.servos
        self.servo_definitions = config.servos.calibration
        self.movements = config.movements

    def move_servos(self, movements: dict[int, float], speed: str = "M"):
        """
        Executes a set of servo movements with smooth interpolation.

        Args:
            movements: A dictionary of {pin: angle}.
            speed: A character representing speed ('S'low, 'M'edium, 'F'ast).
        """
        duration_map = {"S": 1.0, "M": 0.5, "F": 0.2}
        duration = duration_map.get(speed, 0.5)

        # Get current and target angles for interpolation
        current_angles = self.get_current_angles()
        target_angles = movements

        steps = int(duration / 0.02)  # 50 FPS update rate
        if steps <= 0:
            steps = 1

        # The driver expects a list of angles in a specific order
        ordered_pins = self.servos.pins

        for i in range(1, steps + 1):
            ratio = i / steps
            # Build the list of angles for this step in the correct order
            step_angles_list = []
            for pin in ordered_pins:
                start_angle = current_angles.get(pin, 0)
                # If a pin isn't in the current movement, it should hold its start position
                end_angle = target_angles.get(pin, start_angle)

                new_angle = start_angle + (end_angle - start_angle) * ratio
                step_angles_list.append(new_angle)

            self.servos.move_all_angles(step_angles_list)
            time.sleep(0.02)

        # Ensure final position is set accurately by creating the final ordered list
        final_angles_list = []
        for pin in ordered_pins:
            start_angle = current_angles.get(pin, 0)
            final_angle = target_angles.get(pin, start_angle)
            final_angles_list.append(final_angle)

        self.servos.move_all_angles(final_angles_list)

    def get_current_angles(self) -> dict[int, float]:
        """
        Returns a dictionary of {pin: current_angle} by mapping the list
        from the driver to its corresponding pins.
        """
        angle_list = self.servos.get_all_angles()
        pin_list = self.servos.pins
        return {pin_list[i]: angle_list[i] for i in range(len(pin_list))}

    def center_all_servos(self):
        """Moves all servos to their center position."""
        print("Centering all servos...")
        center_angles = {int(pin): 0 for pin in self.servo_definitions.keys()}
        self.move_servos(center_angles, speed="M")
        time.sleep(0.5)

    def execute_movement(self, movement_name: str):
        """
        Executes a pre-defined movement sequence by name.

        Args:
            movement_name: The name of the movement to execute.
        """
        if movement_name not in self.movements:
            print(f"Error: Movement '{movement_name}' not found.")
            return

        print(f"Executing movement: '{movement_name}'...")
        sequence = self.movements[movement_name]
        for step in sequence:
            # The keys in 'moves' from JSON will be strings, convert them to int
            moves = {int(k): v for k, v in step["moves"].items()}
            self.move_servos(moves, step["speed"])
        print(f"Movement '{movement_name}' finished.")
