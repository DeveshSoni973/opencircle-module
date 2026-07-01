"""Example usage of opencircle_module."""

import asyncio
import os
from dotenv import load_dotenv

from opencircle_module import Agent, GroupChat

load_dotenv()


async def main():
    agents = [
        Agent(
            name="Llama",
            model="llama-3.3-70b-versatile",
            provider="groq",
            api_key=os.environ.get("GROQ_API_KEY"),
            temperature=0.7,
        ),
        Agent(
            name="Qwen",
            model="qwen/qwen3-32b",
            provider="groq",
            api_key=os.environ.get("GROQ_API_KEY"),
            temperature=0.7,
        ),
    ]
    
    chat = GroupChat(
        agents=agents,
        system_prompt="default",
        max_rounds=3,
    )
    
    history = await chat.run("Just introducing you people to one another")
    
    print("\n=== FULL TRANSCRIPT ===")
    print(chat.get_transcript())


if __name__ == "__main__":
    asyncio.run(main())