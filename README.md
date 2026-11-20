# ADK Replica

A minimal, dependency-free reimplementation of the core building blocks of Google's
[Agent Development Kit (ADK)](https://google.github.io/adk-docs/), written as a learning exercise
to understand how an agent framework works under the hood.

## Components

| Component | Status | Description |
|---|---|---|
| `FunctionTool` | ✅ Done | Wraps a Python function and builds a JSON-like schema from its signature and docstring. |
| `Session` | ✅ Done | Holds a conversation's events and state for a user/app. |
| `InMemorySessionService` | ✅ Done | Creates and retrieves sessions in memory. |
| `Event` | 🚧 Partial | A message authored by the user or an agent. `is_final_response()` is not implemented yet. |
| `Agent` | 🚧 Stub | Name, model, instruction and tools for an agent. |
| `Runner` | 🚧 Stub | Drives the agent loop and yields `Event`s. |

## Requirements

- Python 3.10+
- No third-party packages (standard library only)

## Getting started

```bash
git clone https://github.com/Stephnn0/adk_replica.git
cd adk_replica
python3 -m venv venv
source venv/bin/activate
python main.py
```

Expected output (abridged):

```
...testing program...
Session created: Session(app_name='test', user_id='steph', ...)
Tool schema: {'name': 'get_weather', 'description': 'Returns the weather for a city.', ...}
Tool call: {'city': 'Quito', 'forecast': 'sunny', 'temp_c': 24}
```

## Roadmap

- [ ] Implement `Event.is_final_response()`
- [ ] Implement `Agent`
- [ ] Implement `Runner` with a fake model that can call tools
