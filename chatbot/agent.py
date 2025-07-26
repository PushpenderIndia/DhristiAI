from google.adk.agents import Agent
from .tools import run_find_person

agent = Agent(
    name="drishti_chatbot",
    model="gemini-2.0-flash",
    description="Assistant to help find missing persons or chat casually.",
    instruction=(
        "You are DrishtiAI assistant. "
        "If the user requests a missing person search, call run_find_person(name, image_path_local). "
        "Otherwise, converse naturally, while maintaining multi-turn context."
    ),
    tools=[run_find_person]
)
