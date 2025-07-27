"""
DrishtiAI Stampede Prediction System
===================================

Simplified multi-agent system for predicting stampede probability and crowd surges.

Core Architecture:
- Main Agent: Gemini-powered stampede risk analysis
- Wikipedia Agent: Historical research using Wikipedia
- Optional Agents: Additional analysis if API keys are provided

Available Agents:
🧠 Main DrishtiAI Agent: Core stampede prediction using Gemini
🏛️ Wikipedia Agent: Historical incident research (always available)
📱 Social Media Agent: Buzz monitoring (if Twitter/Reddit APIs provided)
📰 News Agent: Media coverage analysis (if News API provided)
🌤️ Weather Agent: Weather impact analysis (if Weather API provided)
🚗 Traffic Agent: Transportation analysis (if Google Maps API provided)
"""

# Import for ADK web interface discovery
from . import agent

# Import core agents
from . import wikipedia_agent
from . import optional_agents

# Import the main agent
from .agent import root_agent

__version__ = "2.0.0" 
__author__ = "DrishtiAI Team"

def get_system_status():
    """Get the current status of available agents"""
    try:
        from .optional_agents import get_agent_status
        optional_status = get_agent_status()
    except ImportError:
        optional_status = {"error": "Optional agents module not available"}
    
    return {
        "main_agent": "Available (Gemini-powered)",
        "wikipedia_agent": "Available (Historical research)",
        "optional_agents": optional_status,
        "version": __version__
    } 