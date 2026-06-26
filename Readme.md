# opencircle_module

Decentralized multi-agent group chat system. Agents self-decide whether to speak. No external selector.

## Features

- **Parallel single-phase execution**: All agents see the same history snapshot and respond simultaneously
- **Provider-agnostic**: Groq, OpenAI, Anthropic/Claude, Google/Gemini, NVIDIA NIM, OpenRouter
- **Dynamic system prompts**: File-based templates resolved at runtime
- **UUID-based history**: Clean canonical storage with runtime name resolution

## Install

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Quick Start

```python
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
        ),
        Agent(
            name="Qwen",
            model="qwen/qwen3-32b",
            provider="groq",
            api_key=os.environ.get("GROQ_API_KEY"),
        ),
    ]
    
    chat = GroupChat(agents=agents, system_prompt="default", max_rounds=3)
    history = await chat.run("Should I learn ML or backend engineering first?")
    print(chat.get_transcript())

asyncio.run(main())
```

## System Prompts

Place `.txt` files in `opencircle_module/system_prompts/`. Built-in: `default`, `debate`, `technical`, `creative`.

Variables: `$agent_name`, `$other_agents`, `$user_query`

## Architecture

```
User Query -> History (canonical, UUIDs)
                |
    +---------------------------+
    |  All agents parallel      |
    |  Same snapshot -> respond |
    |  [SILENT] or response     |
    +---------------------------+
                |
    Append responses -> Next Round
```

## Providers

| Name       | Env Key            |
|------------|--------------------|
| groq       | GROQ_API_KEY       |
| openai     | OPENAI_API_KEY     |
| anthropic  | ANTHROPIC_API_KEY  |
| google     | GOOGLE_API_KEY     |
| nvidia     | NVIDIA_API_KEY     |
| openrouter | OPENROUTER_API_KEY |