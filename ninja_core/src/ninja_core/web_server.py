import asyncio
import os
import socket
from contextlib import asynccontextmanager
from typing import Optional

import qrcode
import uvicorn
from fastapi import FastAPI, APIRouter, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pyngrok import ngrok, conf

from .config import load_config, set_api_key
from .hal import HardwareAbstractionLayer
from .ninja_agent import NinjaAgent, MissingAPIKeyError
from .facial_expressions import AnimatedFaces
from .robot_sound import RobotSoundPlayer
from .movement_controller import MovementController, EmergencyStop
from .perception import DistanceMonitor

# --- Configuration ---
base_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# --- Pydantic Models ---
class SetApiKeyRequest(BaseModel):
    api_key: str

class AgentChatRequest(BaseModel):
    message: str

# --- Global State Wrapper ---
class AppState:
    def __init__(self):
        self.hal: Optional[HardwareAbstractionLayer] = None
        self.agent: Optional[NinjaAgent] = None
        self.faces: Optional[AnimatedFaces] = None
        self.sound: Optional[RobotSoundPlayer] = None
        self.movement: Optional[MovementController] = None
        self.distance_monitor: Optional[DistanceMonitor] = None
        self.first_interaction: bool = True
        self.has_greeted: bool = False

# --- Lifecycle ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    print("Initializing NinjaRobot V4 Web Server...")
    
    # Load Config & HAL
    config = load_config()
    app.state.ninja = AppState()
    app.state.ninja.hal = HardwareAbstractionLayer(config)
    app.state.ninja.hal.initialize()
    
    # Initialize Controllers
    app.state.ninja.faces = AnimatedFaces(app.state.ninja.hal)
    app.state.ninja.sound = RobotSoundPlayer(app.state.ninja.hal)
    app.state.ninja.movement = MovementController(app.state.ninja.hal, config)
    
    # Initialize Distance Monitor
    app.state.ninja.distance_monitor = DistanceMonitor(app.state.ninja.hal)
    app.state.ninja.distance_monitor.start_continuous(interval=0.05) # Slightly slower for web to save resources? Keep 0.05

    # Initialize Agent
    try:
        app.state.ninja.agent = NinjaAgent(config)
        print("Ninja AI Agent initialized.")
    except MissingAPIKeyError:
        print("WARNING: Gemini API Key not found. AI Agent will be disabled.")
        print("Run 'ninja_core config set-key gemini <KEY>' or use the web interface to set it.")
    except ValueError as e:
        print(f"Ninja AI Agent not initialized: {e}")

    # Network & ngrok
    asyncio.create_task(setup_network_and_display(app))

    yield

    # --- Shutdown ---
    print("Shutting down Web Server...")
    if app.state.ninja.faces:
        app.state.ninja.faces.stop()
    if app.state.ninja.distance_monitor:
        app.state.ninja.distance_monitor.stop_continuous()
    if app.state.ninja.hal:
        app.state.ninja.hal.shutdown()
    ngrok.kill()

async def setup_network_and_display(app: FastAPI):
    port = 8000
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        ip_address = "127.0.0.1"

    print(f"Local Access: http://{ip_address}:{port}")

    # ngrok
    public_url = None
    for attempt in range(3):
        try:
            public_url = ngrok.connect(port, "http").public_url
            print(f"Public Access: {public_url}")
            break
        except Exception as e:
            print(f"ngrok attempt {attempt+1} failed: {e}")
            await asyncio.sleep(2)

    # Display QR
    if public_url and app.state.ninja.hal.display:
        try:
            qr = qrcode.make(public_url)
            qr = qr.convert('RGB')
            qr = qr.resize((app.state.ninja.hal.display.width, app.state.ninja.hal.display.height))
            app.state.ninja.hal.display.display(qr)
        except Exception as e:
            print(f"Failed to display QR: {e}")
    else:
        # Idle face if no QR or no display
        if app.state.ninja.faces:
            app.state.ninja.faces.play("idle", duration_s=float('inf'))

# --- Helper Functions ---
async def handle_first_interaction(app_state: AppState):
    if app_state.first_interaction:
        app_state.first_interaction = False
        # Only set to idle if we haven't just greeted (to avoid overriding happy face)
        # But actually, if we are chatting, we probably want to be in a neutral state or the chat state.
        # If has_greeted is True, we might be in "happy" state or "idle" state.
        # Let's just ensure we are in a known state.
        if app_state.faces:
            app_state.faces.play("idle", duration_s=float('inf'))

async def trigger_welcome(app_state: AppState):
    """Plays greeting (happy face + sound) if not already greeted."""
    if not app_state.has_greeted:
        app_state.has_greeted = True
        print("Triggering Welcome Greeting...")
        
        # Play Happy Face
        if app_state.faces:
            app_state.faces.play("happy", duration_s=3.0)
        
        # Play Happy Sound (Non-blocking)
        if app_state.sound:
            asyncio.create_task(asyncio.to_thread(app_state.sound.play, "happy"))
        
        # Wait 3s then return to idle
        await asyncio.sleep(3.0)
        if app_state.faces:
            app_state.faces.play("idle", duration_s=float('inf'))

def safety_check(app_state: AppState) -> bool:
    """Returns True if obstacle is detected (<= 50mm)."""
    if not app_state.distance_monitor:
        return False
    dist = app_state.distance_monitor.get_continuous_distance()
    return 0 <= dist <= 50

async def execute_action_plan(app_state: AppState, action_plan: dict):
    tasks = []

    # Face
    if action_plan.get("face") and app_state.faces:
        face_name = action_plan["face"]
        # Play face for 3s then return to idle
        async def play_face():
            app_state.faces.play(face_name, duration_s=3.0)
            await asyncio.sleep(3.0)
            app_state.faces.play("idle", duration_s=float('inf'))
        tasks.append(asyncio.create_task(play_face()))

    # Sound
    if action_plan.get("sound") and app_state.sound:
        sound_name = action_plan["sound"]
        # Sound is blocking in current impl, run in thread
        tasks.append(asyncio.to_thread(app_state.sound.play, sound_name))

    # Movement
    if action_plan.get("movement") and app_state.movement:
        move_name = action_plan["movement"]
        def run_move():
            try:
                app_state.movement.execute_movement(
                    move_name, 
                    abort_check=lambda: safety_check(app_state)
                )
            except EmergencyStop:
                print("Emergency Stop triggered via Web!")
                if app_state.faces:
                    app_state.faces.play("scary")
                if app_state.sound:
                    app_state.sound.play("scary")
        tasks.append(asyncio.to_thread(run_move))

    if tasks:
        await asyncio.gather(*tasks)

# --- API Router ---
api_router = APIRouter(prefix="/api")

@api_router.get("/agent/status")
async def agent_status(request: Request):
    return {"active": request.app.state.ninja.agent is not None}

@api_router.post("/agent/set_api_key")
async def set_key_endpoint(payload: SetApiKeyRequest, request: Request):
    try:
        # Update .env
        # We need to know the service name, assuming 'gemini' for now based on V3
        set_api_key("gemini", payload.api_key)
        
        # Reload config and agent
        config = load_config()
        request.app.state.ninja.agent = NinjaAgent(config)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/agent/chat")
async def agent_chat(payload: AgentChatRequest, request: Request):
    state = request.app.state.ninja
    await handle_first_interaction(state)
    
    if not state.agent:
        raise HTTPException(status_code=400, detail="Agent not active")

    result = await state.agent.process_command(payload.message)
    
    if result.get("action_plan"):
        await execute_action_plan(state, result["action_plan"])
        
    return {"response": result.get("response"), "log": result.get("log")}

# Note: Voice chat requires saving file and passing to agent. 
# V4 agent doesn't have process_audio_command yet in the interface shown in previous turns?
# Checking ninja_agent.py in previous turns... 
# The user didn't explicitly ask for voice in V4 yet, but V3 had it. 
# I will implement the endpoint structure but might need to stub it if Agent doesn't support it yet.
# Actually, looking at V3, it used `process_audio_command`. 
# I'll omit voice for now to avoid errors if not implemented in V4 Agent, 
# or I can add it if I verify Agent has it. 
# For now, I will stick to text chat as per "Chat" requirement.

@api_router.get("/servos/movements")
def get_movements(request: Request):
    # MovementController doesn't expose list directly? 
    # It loads from config. Let's check MovementController.
    # It has `self.movements`.
    if request.app.state.ninja.movement:
        return {"movements": list(request.app.state.ninja.movement.movements.keys())}
    return {"movements": []}

@api_router.post("/servos/movements/{name}/execute")
async def execute_movement(name: str, request: Request):
    state = request.app.state.ninja
    if not state.movement:
        raise HTTPException(status_code=500, detail="Movement controller not ready")
    
    if name not in state.movement.movements:
        raise HTTPException(status_code=404, detail="Movement not found")

    def run():
        try:
            state.movement.execute_movement(name, abort_check=lambda: safety_check(state))
            return "executed"
        except EmergencyStop:
            print("Emergency Stop triggered via Web!")
            if state.faces:
                state.faces.play("scary")
            if state.sound:
                state.sound.play("scary")
            raise HTTPException(status_code=409, detail="Emergency Stop: Obstacle Detected")

    await asyncio.to_thread(run)
    return {"status": "executed"}

@api_router.get("/display/expressions")
def get_expressions(request: Request):
    if request.app.state.ninja.faces:
        return {"expressions": list(request.app.state.ninja.faces.animations.keys())}
    return {"expressions": []}

@api_router.post("/display/expressions/{name}")
def show_expression(name: str, request: Request):
    if request.app.state.ninja.faces:
        request.app.state.ninja.faces.play(name, duration_s=3.0)
    return {"status": "displayed"}

@api_router.get("/sound/emotions")
def get_sounds(request: Request):
    if request.app.state.ninja.sound:
        return {"emotions": list(request.app.state.ninja.sound.SOUNDS.keys())}
    return {"emotions": []}

@api_router.post("/sound/emotions/{name}")
async def play_sound(name: str, request: Request):
    if request.app.state.ninja.sound:
        await asyncio.to_thread(request.app.state.ninja.sound.play, name)
    return {"status": "played"}

@api_router.get("/sensor/distance")
def get_distance_api(request: Request):
    if request.app.state.ninja.distance_monitor:
        return {"distance_mm": request.app.state.ninja.distance_monitor.get_continuous_distance()}
    return {"distance_mm": -1}

# --- App ---
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Trigger welcome greeting on page load
    asyncio.create_task(trigger_welcome(request.app.state.ninja))
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/distance")
async def websocket_distance(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            if websocket.app.state.ninja.distance_monitor:
                dist = websocket.app.state.ninja.distance_monitor.get_continuous_distance()
                await websocket.send_json({"distance_mm": dist})
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass

def run_server():
    print("--- NinjaRobot Web Server Setup ---")
    
    # Check for existing token
    token_exists = False
    if conf.get_default().auth_token:
        token_exists = True
    else:
        # Check common config paths
        paths = [
            os.path.join(os.path.expanduser("~"), ".ngrok2", "ngrok.yml"),
            os.path.join(os.path.expanduser("~"), "Library", "Application Support", "ngrok", "ngrok.yml"),
            os.path.join(os.path.expanduser("~"), ".config", "ngrok", "ngrok.yml")
        ]
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p, 'r') as f:
                        if "authtoken" in f.read():
                            token_exists = True
                            break
                except Exception:
                    pass

    print("Checking ngrok configuration...")
    
    if token_exists:
        token = input("Proceed with existing ngrok account by pressing ENTER or input new ngrok authtoken to proceed: ").strip()
    else:
        token = input("Please input your ngrok authtoken to proceed: ").strip()

    if token:
        print("Setting ngrok authtoken...")
        ngrok.set_auth_token(token)
    
    uvicorn.run("ninja_core.web_server:app", host="0.0.0.0", port=8000, reload=False)
