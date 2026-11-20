"""A minimal, from-scratch replica of the core Google ADK (Agent Development Kit) objects.

Implemented so far: FunctionTool, Session, InMemorySessionService.
Still stubbed: Event.is_final_response, Agent, Runner.
"""

from __future__ import annotations

import inspect
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator


# =========================================================
#  Core objects
# =========================================================


class FunctionTool:
    def __init__(self, func: Callable):
        self.func = func
        self.name = func.__name__
        self.description = inspect.getdoc(func) or ""
        self.schema = self._build_schema()

    def _build_schema(self) -> dict:

        sig = inspect.signature(self.func, eval_str=True)
        params = {}
        required = []

        for pname, p in sig.parameters.items():
            ptype = p.annotation.__name__ if p.annotation is not inspect.Parameter.empty else "any"
            params[pname] = {"type": ptype}
            if p.default is inspect.Parameter.empty:
                required.append(pname)
        return {
            "name": self.name,
            "description": self.description,
            "parameters": params,
            "required": required,
        }

    def call(self, **kwargs) -> Any:
        return self.func(**kwargs)


@dataclass
class Event:
    author: str          # "user" or the agent's name
    content: str

    def is_final_response(self) -> bool:
        return False  # TODO: implement once the Runner emits model responses


@dataclass
class Session:
    app_name: str
    user_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    events: list[Event] = field(default_factory=list)
    state: dict[str, Any] = field(default_factory=dict)


class InMemorySessionService:
    def __init__(self):
        self._sessions: dict[str, Session] = {}

    def create_session(self, app_name: str, user_id: str) -> Session:
        session = Session(app_name=app_name, user_id=user_id)
        self._sessions[session.id] = session
        return session

    def get_session(self, session_id: str) -> Session:
        if session_id not in self._sessions:
            raise KeyError(f"Session {session_id} not found")
        return self._sessions[session_id]


class Agent:
    def __init__(self, name: str, model: str, instruction: str, tools: list[Callable] | None = None):
        pass  # TODO later


class Runner:
    def __init__(self, agent: Agent, app_name: str, session_service: InMemorySessionService):
        pass  # TODO later

    def run(self, user_id: str, session_id: str, new_message: str) -> Iterator[Event]:
        yield from ()  # TODO later


def get_weather(city: str) -> dict:
    """Returns the weather for a city."""
    return {"city": city, "forecast": "sunny", "temp_c": 24}


# =========================================================
#  Demo
# =========================================================


def main() -> None:
    print("...testing program...")
    APP_NAME = "test"
    USER_ID = "steph"

    agent = Agent(
        name="weather_agent",
        model="fake-gemini",
        instruction="You are a helpful weather assistant.",
        tools=[get_weather],
    )

    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    print("Session created:", session)   # step 1 check

    # step 2 checks
    assert session_service.get_session(session.id) is session
    tool = FunctionTool(get_weather)
    print("Tool schema:", tool.schema)
    print("Tool call:", tool.call(city="Quito"))

    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

    for event in runner.run(user_id=USER_ID, session_id=session.id,
                            new_message="What's the weather in Quito?"):
        print(f"[{event.author}] {event.content}")
        if event.is_final_response():
            print("Final answer:", event.content)


if __name__ == "__main__":
    main()
