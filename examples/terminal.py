import asyncio
import os
from dotenv import load_dotenv

from opencircle_module import Agent, GroupChat

load_dotenv()


class Colors:
    USER = "\033[92m"
    SYSTEM = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


async def terminal_gc():
    agents = [
        Agent(name="Llama", model="llama-3.3-70b-versatile", provider="groq"),
        Agent(name="Qwen", model="qwen/qwen3-32b", provider="groq"),
    ]

    chat = GroupChat(
        agents=agents,
        system_prompt="default",
        max_rounds=5,
    )

    # Real-time callback: fires as soon as any agent responds
    def on_message(msg):
        name = chat.registry.get_name(msg.sender_id)
        print(f"{Colors.BOLD}{name}:{Colors.RESET} {msg.content}\n")

    chat.on_message = on_message

    print(f"{Colors.BOLD}⭕ OpenCircle Group Chat Started{Colors.RESET}")
    print(f"{Colors.SYSTEM}Participants: {', '.join(a.name for a in agents)}{Colors.RESET}\n")

    while True:
        try:
            user_msg = input(f"{Colors.USER}{Colors.BOLD}You:{Colors.RESET} ")
            if user_msg.lower() in ("exit", "quit"):
                break
            if not user_msg.strip():
                continue

            await chat.run(user_msg)

            if chat.terminated:
                print(f"{Colors.SYSTEM}--- Topic Resolved ---{Colors.RESET}\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\n{Colors.BOLD}Error:{Colors.RESET} {e}")


if __name__ == "__main__":
    try:
        asyncio.run(terminal_gc())
    except KeyboardInterrupt:
        pass