from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from .agent import agent

session_service = InMemorySessionService()
runner = Runner(agent=agent, app_name="drishti_app", session_service=session_service)
