import json
from pathlib import Path
import click

from .config import load_config, save_config, ServoCalibration


@click.group()
def main():
    """Command-line interface for NinjaRobotV4 core application."""
    pass


@main.group()
def config():
    """Manage the robot's configuration."""
    pass


@config.command("import-all")
def import_all():
    """
    Imports settings from individual hardware config files (servo.json, buzzer.json)
    into the main config.json.

    This command assumes it is run from the project's root directory.
    """
    # These paths are relative to the project root directory
    servo_config_path = Path("servo.json")
    buzzer_config_path = Path("buzzer.json")

    # load_config() will create a default config.json in the current directory
    # if it doesn't exist.
    main_config = load_config()
    made_changes = False

    # --- Import servo calibration ---
    if servo_config_path.exists():
        click.echo(f"Found servo config at '{servo_config_path}'. Importing...")
        with open(servo_config_path, "r") as f:
            servo_data = json.load(f)

        # The servo.json is a list of servo objects, not a dictionary.
        if isinstance(servo_data, list):
            for servo_entry in servo_data:
                pin = servo_entry.get("pin")
                if pin is None:
                    continue  # Skip entries without a pin

                pin_str = str(pin)
                # The entire entry is the calibration data
                new_calib = ServoCalibration.model_validate(servo_entry)
                if main_config.servos.calibration.get(pin_str) != new_calib:
                    main_config.servos.calibration[pin_str] = new_calib
                    made_changes = True
        click.echo("...servo import complete.")
    else:
        click.echo(
            f"Info: Servo config not found at '{servo_config_path}'. Skipping."
        )

    # --- Import buzzer pin ---
    if buzzer_config_path.exists():
        click.echo(f"Found buzzer config at '{buzzer_config_path}'. Importing...")
        with open(buzzer_config_path, "r") as f:
            buzzer_data = json.load(f)

        if "pin" in buzzer_data and main_config.buzzer.pin != buzzer_data["pin"]:
            main_config.buzzer.pin = buzzer_data["pin"]
            made_changes = True
        click.echo("...buzzer import complete.")
    else:
        click.echo(
            f"Info: Buzzer config not found at '{buzzer_config_path}'. Skipping."
        )

    # --- Save changes if any were made ---
    if made_changes:
        save_config(main_config)
        click.echo(
            click.style("Successfully imported settings and updated config.json!", fg="green")
        )
    else:
        click.echo("No new settings to import or no changes detected.")


if __name__ == "__main__":
    main()
