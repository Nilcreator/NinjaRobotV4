import click

from .config import import_and_update_config, set_api_key

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


@config.command("set-key")
@click.argument("service")
@click.argument("key")
def set_key(service, key):
    """
    Set an API key for a service (e.g., gemini).

    Usage: ninja_core config set-key gemini YOUR_API_KEY
    """
    set_api_key(service, key)


@main.command("chat")
def chat():
    """
    Start an interactive text chat with the Ninja Agent.
    This initializes the robot hardware and allows you to type commands.
    """
    import asyncio
    import time
    from .config import load_config
    from .hal import HardwareAbstractionLayer
    from .ninja_agent import NinjaAgent
    from .facial_expressions import AnimatedFaces
    from .robot_sound import RobotSoundPlayer
    from .perception import DistanceMonitor
    from .movement_controller import MovementController, EmergencyStop

    async def run_chat():
        print("Initializing NinjaRobot Hardware...")
        config = load_config()
        hal = HardwareAbstractionLayer(config)
        hal.initialize()
        
        # Initialize Distance Monitor
        distance_monitor = DistanceMonitor(hal)
        distance_monitor.start_continuous(interval=0.05)
        
        # Initialize Controllers (declare outside try for finally access)
        faces = None

        try:
            print("Initializing AI Agent...")
            agent = NinjaAgent(config)
            
            # Initialize Controllers
            faces = AnimatedFaces(hal)
            sound = RobotSoundPlayer(hal)
            movement = MovementController(hal, config)

            print("\n--- Ninja Agent Ready ---")
            print("Type 'exit' or 'quit' to stop.")
            
            # --- Welcome Greeting ---
            faces.play("happy", duration_s=3.0)
            print("Ninja: Hello! I am ready.")
            time.sleep(3.0)
            faces.play("idle", duration_s=float('inf'))
            # ------------------------

            # --- Safety Check Function ---
            def safety_check() -> bool:
                dist = distance_monitor.get_continuous_distance()
                vel = distance_monitor.get_velocity()
                
                # Display distance (flush=True to ensure immediate output)
                display_dist = dist if dist != -1 else "---"
                print(f"Dist: {display_dist}mm | Vel: {vel:.1f}mm/s   ", end="\r", flush=True)

                # Use robust emergency check
                if distance_monitor.check_emergency_stop():
                    print()  # Newline so the emergency message is on a new line
                    print(f"!!! EMERGENCY STOP !!! Dist: {dist}mm, Vel: {vel:.2f}mm/s")
                    return True
                return False
            # -----------------------------
            
            while True:
                user_input = input("\nYou: ")
                if user_input.lower() in ["exit", "quit"]:
                    break
                
                print("Ninja is thinking...")
                result = await agent.process_command(user_input)
                
                action_plan = result["action_plan"]
                response_text = result["response"]
                
                # Execute Actions
                if action_plan.get("face"):
                    faces.play(action_plan["face"])
                
                if action_plan.get("sound"):
                    sound.play(action_plan["sound"])
                    
                if action_plan.get("movement"):
                    try:
                        movement.execute_movement(
                            action_plan["movement"], 
                            abort_check=safety_check
                        )
                    except EmergencyStop:
                        print("!!! OBSTACLE DETECTED - STOPPING !!!")
                        # Reaction: Frightened
                        faces.play("scary")  # Using 'scary' as frightened
                        sound.play("scary")
                        print("Ninja: Whoa! Too close!")

                print(f"Ninja: {response_text}")
                
                # --- Idle Status Management ---
                # Return to idle status 3 seconds after completion
                time.sleep(3.0)
                faces.play("idle", duration_s=float('inf'))
                # ------------------------------

        except Exception as e:
            print(f"\nError: {e}")
        finally:
            print("\nShutting down...")
            if faces:
                faces.stop()
            distance_monitor.stop_continuous()
            hal.shutdown()

    asyncio.run(run_chat())


@main.command("server")
@click.option("--autostart", is_flag=True, help="Run in autostart mode (non-interactive).")
def server(autostart):
    """
    Start the NinjaRobot Web Server.
    Provides a web interface for remote control and AI chat.
    """
    from .web_server import run_server
    run_server(autostart=autostart)


if __name__ == "__main__":
    main()
