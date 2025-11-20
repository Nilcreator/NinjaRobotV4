import asyncio
import os
from unittest.mock import MagicMock, patch

from ninja_core.config import NinjaConfig
from ninja_core.ninja_agent import MissingAPIKeyError, NinjaAgent


async def test_agent():
    print("--- Starting NinjaAgent Verification ---")

    # 1. Test Missing API Key
    print("\n[Test 1] Missing API Key Check")
    config_no_key = NinjaConfig()
    try:
        NinjaAgent(config_no_key)
        print("FAIL: Did not raise MissingAPIKeyError")
    except MissingAPIKeyError:
        print("PASS: Raised MissingAPIKeyError as expected")

    # 2. Test Initialization with Key
    print("\n[Test 2] Initialization with Key")
    config_with_key = NinjaConfig(api_keys={"gemini": "fake_key"})
    
    # Mock genai to avoid real API calls
    with patch("google.generativeai.GenerativeModel") as MockModel, \
         patch("google.generativeai.configure"):
        
        agent = NinjaAgent(config_with_key)
        print("PASS: Agent initialized successfully")

        # 3. Test Process Command (Text) - Auto Emotion
        print("\n[Test 3] Auto-Emotion Logic (Text)")
        
        # Mock the chat session and response
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Hello! How can I help?"
        mock_response.candidates[0].content.parts[0].function_call = None
        
        # Async mock for send_message_async
        async def async_return_response(*args, **kwargs):
            return mock_response
        
        mock_chat.send_message_async.side_effect = async_return_response
        agent.model.start_chat.return_value = mock_chat

        result = await agent.process_command("Hello")
        
        action_plan = result["action_plan"]
        if (
            action_plan.get("face") == "speaking" 
            and action_plan.get("sound") == "speaking"
            and action_plan.get("response") == "Hello! How can I help?"
        ):
            print(f"PASS: Auto-emotion applied correctly. Plan: {action_plan}")
        else:
            print(f"FAIL: Auto-emotion failed. Plan: {action_plan}")

        # 4. Test Process Command (Text) - Explicit JSON
        print("\n[Test 4] Explicit JSON Response")
        mock_response.text = '{"face": "happy", "sound": "happy", "response": "I am happy!"}'
        
        result = await agent.process_command("Be happy")
        action_plan = result["action_plan"]
        
        if action_plan.get("face") == "happy":
             print(f"PASS: Explicit JSON parsed correctly. Plan: {action_plan}")
        else:
             print(f"FAIL: JSON parsing failed. Plan: {action_plan}")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    asyncio.run(test_agent())
