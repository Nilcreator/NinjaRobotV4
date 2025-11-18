import click

from .config import import_and_update_config

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

    Imports settings from hardware files (e.g., servo.json) into the main

    config.json, or applies defaults if files are missing.

    """

    import_and_update_config()


if __name__ == "__main__":
    main()
