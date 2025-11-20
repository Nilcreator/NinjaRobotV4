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
        distance_monitor.start_continuous(interval=0.01)

        try:
            print("Initializing AI Agent...")
            agent = NinjaAgent(config)
            
            # Initialize Controllers
            faces = AnimatedFaces(hal)
            sound = RobotSoundPlayer(hal)
            movement = MovementController(hal, config)

            print("\n--- Ninja Agent Ready ---")
            print("Type 'exit' or 'quit' to stop.")
            
            # --- Safety Check Function ---
            def safety_check() -> bool:
                dist = distance_monitor.get_continuous_distance()
                
                # Display distance (flush=True to ensure immediate output)
                display_dist = dist if dist != -1 else "---"
                print(f"Distance: {display_dist}mm   ", end="\r", flush=True)

                # Check if valid reading (>=0) and within 50mm (inclusive)
                if 0 <= dist <= 50:
                    print()  # Newline so the emergency message is on a new line
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

        except Exception as e:
            print(f"\nError: {e}")
        finally:
            print("\nShutting down...")
            distance_monitor.stop_continuous()
            hal.shutdown()

    asyncio.run(run_chat())


if __name__ == "__main__":
    main()
