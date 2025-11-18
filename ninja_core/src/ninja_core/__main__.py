import click

from .config import load_config, save_config, import_and_update_config

from .movement_cli import run_cli as run_movement_cli


@click.group()
def main():
    """Command-line interface for NinjaRobotV4 core application."""

    pass


@main.command("movement-tool")
def movement_tool():
    """Launch the interactive CLI tool for recording and editing servo movements."""

    run_movement_cli()


@main.group()
def config():
    """Manage the robot's configuration."""

    pass


@config.command("import-all")
def import_all():
    """

    Imports settings from individual hardware config files (servo.json, buzzer.json)

    into the main config.json.

    """

    main_config = load_config()

    made_changes = import_and_update_config(main_config)

    if made_changes:
        save_config(main_config)

        click.echo(
            click.style(
                "Successfully imported settings and updated config.json!", fg="green"
            )
        )

    else:
        click.echo("No new settings to import or no changes detected.")


if __name__ == "__main__":
    main()
