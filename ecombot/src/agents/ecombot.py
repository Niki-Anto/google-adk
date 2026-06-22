import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import uuid
from google.adk.runners import Runner
from google.genai import types
from adk_extra_services.sessions import RedisSessionService
from google.adk.sessions import InMemorySessionService
from routing import enable_routing_callbacks, routing_log, classify_query
from agent import root_agent

APP_NAME = "ecombot"
REDIS_URL = "redis://localhost:6379"


def create_session_service(redis_url: str):
    try:
        service = RedisSessionService(redis_url=redis_url)
        print(f"Session backend: Redis ({redis_url})")
        return service
    except Exception as e:
        print(f"Redis unavailable ({e}), falling back to InMemorySessionService")
        service = InMemorySessionService()
        print("Session backend: InMemorySessionService")
        return service


async def list_existing_sessions(session_service, user_id: str):
    response = await session_service.list_sessions(app_name=APP_NAME, user_id=user_id)
    return response.sessions if response and response.sessions else []


async def resume_session_menu(session_service, user_id: str):
    sessions = await list_existing_sessions(session_service, user_id)
    if not sessions:
        print("\nNo existing sessions found. Starting a new conversation.\n")
        return None

    print("\n--- Existing Sessions ---")
    for i, s in enumerate(sessions, 1):
        print(f"  {i}. Session ID: {s.id}")
    print(f"  0. Back to main menu")

    while True:
        choice = input("\nSelect a session number: ").strip()
        if choice == "0":
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(sessions):
                return sessions[idx].id
        except ValueError:
            pass
        print("Invalid choice. Try again.")


async def chat_loop(runner: Runner, user_id: str, session_id: str):
    print(f"\n{'='*50}")
    print(f"  Session ID : {session_id}")
    print(f"  User ID    : {user_id}")
    print(f"{'='*50}")
    print("Type your message (or 'quit' to exit, 'new' for new session)\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if user_input.lower() == "new":
            return "new"

        message = types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )

        response_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                response_text = event.content.parts[0].text or ""

        print(f"\nBot: {response_text}\n")

    return "quit"


async def main():
    enable_routing_callbacks()
    session_service = create_session_service(REDIS_URL)
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    user_id = input("Enter your user ID (or press Enter for 'default-user'): ").strip()
    if not user_id:
        user_id = "default-user"

    print("\n" + "="*50)
    print(f"  Welcome to EcomBot CLI (user: {user_id})")
    print("="*50)

    while True:
        print("\n--- Main Menu ---")
        print("  1. New conversation")
        print("  2. Resume existing conversation")
        print("  3. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            session_id = str(uuid.uuid4())
            await session_service.create_session(
                app_name=APP_NAME, user_id=user_id, session_id=session_id
            )
            result = await chat_loop(runner, user_id, session_id)
            if result == "quit":
                break

        elif choice == "2":
            session_id = await resume_session_menu(session_service, user_id)
            if session_id:
                result = await chat_loop(runner, user_id, session_id)
                if result == "quit":
                    break

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    asyncio.run(main())



    