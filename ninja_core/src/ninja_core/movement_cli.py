import copy
import select
import sys
import termios
import time
import tty

from ninja_core.config import NinjaConfig, load_config, save_config
from ninja_core.hal import HardwareAbstractionLayer
from ninja_core.movement_controller import MovementController


def parse_movement_command(
    command_str: str, definitions: dict
) -> tuple[str | None, dict | None]:
    """
    Parses the user's command string (e.g., 'S_17:30/27:M').
    Returns a tuple: (speed, {pin: angle_value}).
    """
    speed = "M"  # Default to Medium speed
    if command_str.startswith(("S_", "M_", "F_")):
        speed = command_str[0]
        command_str = command_str[2:]

    movements = {}
    parts = command_str.split("/")
    for part in parts:
        try:
            pin_str, angle_char = part.split(":")
            pin = int(pin_str)
            # The keys in the definitions dict are strings, so we must check against a string.
            if pin_str not in definitions:
                raise ValueError(f"Servo pin {pin} is not defined.")

            angle = 0
            if angle_char.upper() == "X":
                angle = 90
            elif angle_char.upper() == "M":
                angle = -90
            elif angle_char.upper() == "C":
                angle = 0
            else:
                angle = int(angle_char)
                if not -90 <= angle <= 90:
                    raise ValueError("Angle must be between -90 and 90.")

            movements[pin] = angle
        except ValueError as e:
            print(f"Error parsing '{part}': {e}")
            return None, None

    return speed, movements


def record_new_movement(controller: MovementController, config: NinjaConfig):
    """Handles the UI and logic for recording a new movement sequence."""
    print("\n--- Record New Movement ---")
    print("Enter commands like '17:30/27:M' or 'S_22:-45'.")

    servo_defs = controller.servo_definitions
    print("Available Servos (Pin):")
    for pin in servo_defs.keys():
        print(f"  - Pin {pin}")

    print("\nSetting all servos to center position to begin...")
    controller.center_all_servos()

    sequence = []
    previous_angles = controller.get_current_angles()

    while True:
        command_str = input("Enter servo movement command: ").strip()
        if not command_str:
            continue

        speed, moves = parse_movement_command(command_str, servo_defs)
        if not moves:
            continue

        all_servo_pins = servo_defs.keys()
        completed_moves = moves.copy()

        for pin_str in all_servo_pins:
            pin = int(pin_str)
            if pin not in completed_moves:
                previous_angle = previous_angles.get(pin, 0)
                completed_moves[pin] = previous_angle

        print(f"Executing full movement: {completed_moves} with speed {speed}")
        controller.move_servos(completed_moves, speed)

        while True:
            choice = input(
                "1. Confirm & Next | 2. Reset | 3. Finish Recording: "
            ).strip()
            if choice == "1":
                sequence.append({"speed": speed, "moves": completed_moves})
                previous_angles = controller.get_current_angles()
                print("Movement step confirmed.")
                break
            elif choice == "2":
                print("Resetting to previous position...")
                controller.move_servos(previous_angles, "F")
                break
            elif choice == "3":
                sequence.append({"speed": speed, "moves": completed_moves})
                print("Last movement step confirmed.")

                if not sequence:
                    print("No movements recorded. Aborting.")
                    return

                movement_name = input("Enter a name for this movement: ").strip()
                if not movement_name:
                    print("Name cannot be empty. Aborting save.")
                    controller.center_all_servos()
                    return

                # Correctly access and update the Pydantic model
                config.movements[movement_name] = sequence
                print(f"Movement '{movement_name}' saved!")
                controller.center_all_servos()
                return
            else:
                print("Invalid option.")


class NonBlockingKeyboard:
    """A class to handle non-blocking keyboard input."""

    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def kbhit(self):
        """Check if a key has been pressed."""
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    def getch(self):
        """Get the pressed character."""
        return sys.stdin.read(1)


def execute_movement_cli(controller: MovementController):
    """Handles the UI for executing a saved movement with looping."""
    print("\n--- Execute a Movement ---")
    all_movements = controller.movements
    if not all_movements:
        print("No movements have been recorded yet.")
        return

    print("Select a movement to execute:")
    names = list(all_movements.keys())
    for i, name in enumerate(names):
        print(f"{i + 1}. {name}")

    try:
        choice = int(input("Enter number: ")) - 1
        if not 0 <= choice < len(names):
            raise ValueError()
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    loop_input = (
        input("Enter number of times to loop, or 'loop' for infinite: ").strip().lower()
    )

    loop_count = 0
    infinite_loop = False
    if loop_input == "loop":
        infinite_loop = True
    else:
        try:
            loop_count = int(loop_input)
        except ValueError:
            print("Invalid input for loop count.")
            return

    selected_name = names[choice]
    print(f"Executing movement: '{selected_name}'...")
    print("Press Enter or Esc to interrupt.")
    controller.center_all_servos()

    interrupted = False
    with NonBlockingKeyboard() as nkb:
        loops_done = 0
        while infinite_loop or loops_done < loop_count:
            if nkb.kbhit():
                key = nkb.getch()
                if key == "\r" or key == "\x1b":  # Enter or Esc
                    interrupted = True
                    break
            controller.execute_movement(selected_name)
            if interrupted:
                break
            loops_done += 1

    if interrupted:
        print("\nMovement interrupted by user.")
    else:
        print(f"\nMovement '{selected_name}' finished.")

    time.sleep(1)
    controller.center_all_servos()


def edit_sequence_menu(
    controller: MovementController, sequence_to_edit: list
) -> list | None:
    """UI for editing a sequence. Operates on a copy."""
    temp_sequence = copy.deepcopy(sequence_to_edit)
    # servo_defs = controller.servo_definitions

    try:
        while True:
            print("\n--- Editing Sequence ---")
            for i, step in enumerate(temp_sequence):
                print(f"Step {i + 1}: Speed={step['speed']}, Moves={step['moves']}")

            print(
                "\nOptions: 1. Edit | 2. Insert | 3. Delete | 4. Preview | 5. Save | 6. Abort"
            )
            edit_choice = input("Select an option: ").strip()

            if edit_choice == "1":  # Edit
                # ... (Implementation for editing a step)
                pass
            elif edit_choice == "2":  # Insert
                # ... (Implementation for inserting a step)
                pass
            elif edit_choice == "3":  # Delete
                # ... (Implementation for deleting a step)
                pass
            elif edit_choice == "4":  # Preview
                print("Previewing sequence...")
                controller.center_all_servos()
                for i, step in enumerate(temp_sequence):
                    print(f"  - Step {i + 1}: {step['moves']}")
                    moves = {int(k): v for k, v in step["moves"].items()}
                    controller.move_servos(moves, step["speed"])
                print("Preview finished.")
                time.sleep(1)
                controller.center_all_servos()
            elif edit_choice == "5":  # Save
                return temp_sequence
            elif edit_choice == "6":  # Abort
                return None
            else:
                print("Invalid option.")
    except KeyboardInterrupt:
        return None


def modify_existing_movement(controller: MovementController, config: NinjaConfig):
    """Handles the non-destructive modification of a movement sequence."""
    print("\n--- Modify Existing Movement ---")
    if not config.movements:
        print("No movements recorded.")
        return

    # ... (UI for selecting movement) ...
    # selected_name = ...
    # original_sequence = config.movements[selected_name]
    # modified_sequence = edit_sequence_menu(controller, original_sequence)
    # if modified_sequence:
    #     config.movements[selected_name] = modified_sequence
    #     config.save()
    #     print("Saved changes.")
    print("Modification logic not fully implemented in this port.")


def clear_movement(controller: MovementController, config: NinjaConfig):
    """Handles clearing a movement sequence."""
    print("\n--- Clear Movement ---")
    if not config.movements:
        print("No movements recorded.")
        return

    # ... (UI for selecting and confirming deletion) ...
    # del config.movements[selected_name]
    # config.save()
    # print("Movement deleted.")
    print("Clear logic not fully implemented in this port.")


def run_cli():
    """Main entry point for the interactive movement CLI tool."""
    config = load_config()
    hal = HardwareAbstractionLayer(config)

    try:
        hal.initialize()
        controller = MovementController(hal, config)

        while True:
            print("\n--- Servo Movement CLI Tool ---")
            print("1. Record new movement")
            print("2. Modify existing movement")
            print("3. Execute a movement")
            print("4. Clear movement")
            print("5. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                record_new_movement(controller, config)
            elif choice == "2":
                modify_existing_movement(controller, config)
            elif choice == "3":
                execute_movement_cli(controller)
            elif choice == "4":
                clear_movement(controller, config)
            elif choice == "5":
                break
            else:
                print("Invalid choice.")
    finally:
        hal.shutdown()
        # After CLI runs, save any potential changes made
        save_config(config)
        print("Configuration saved.")


if __name__ == "__main__":
    run_cli()
