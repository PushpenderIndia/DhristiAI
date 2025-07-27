"""
Optional Agents for DrishtiAI
=============================

These agents only load if their respective API keys are configured.
They provide enhanced analysis capabilities when external services are available.
"""

import os
from google.adk.agents import LlmAgent
from .config import DEFAULT_MODEL

# Check for available API keys
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
REDDIT_API_KEY = os.getenv("REDDIT_API_KEY") 
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Optional Agents List
optional_agents = []

# Social Media Monitoring Agent (if Twitter/Reddit APIs available)
if TWITTER_API_KEY or REDDIT_API_KEY:
    def mock_social_analysis(event_name: str, location: str) -> str:
        """
        Analyze social media buzz around an event.
        Note: This is a placeholder function. Implement actual API calls when ready.
        """
        return f"""
        🔍 Social Media Analysis: {event_name} at {location}
        
        Twitter Activity: {'Available' if TWITTER_API_KEY else 'API key needed'}
        Reddit Discussions: {'Available' if REDDIT_API_KEY else 'API key needed'}
        
        Buzz Level: [Requires API implementation]
        Trending Topics: [Requires API implementation] 
        Sentiment: [Requires API implementation]
        
        Note: Connect your social media API keys to get real-time analysis.
        """
    
    social_agent = LlmAgent(
        model=DEFAULT_MODEL,
        name="social_media_agent",
        description="Monitors social media buzz and viral content that could drive crowds",
        instruction="""
        You analyze social media activity around events to predict crowd behavior.
        
        Focus on:
        - Viral content driving attendance
        - Celebrity social media activity
        - Trending hashtags and mentions
        - Public sentiment and excitement levels
        
        Use the mock_social_analysis tool to gather social media intelligence.
        Provide insights on how social buzz might affect crowd size and behavior.
        """,
        tools=[mock_social_analysis]
    )
    optional_agents.append(social_agent)

# News Monitoring Agent (if News API available)
if NEWS_API_KEY:
    def mock_news_analysis(event_name: str, location: str) -> str:
        """
        Search for recent news about the event or venue.
        Note: This is a placeholder function. Implement actual News API calls when ready.
        """
        return f"""
        📰 News Analysis: {event_name} at {location}
        
        News API Status: {'Connected' if NEWS_API_KEY else 'API key needed'}
        
        Recent Headlines: [Requires API implementation]
        Media Coverage Level: [Requires API implementation]
        Safety Concerns Mentioned: [Requires API implementation]
        
        Note: Connect your News API key to get real-time news analysis.
        """
    
    news_agent = LlmAgent(
        model=DEFAULT_MODEL,
        name="news_monitoring_agent", 
        description="Monitors news coverage and media attention around events",
        instruction="""
        You analyze recent news coverage to identify factors that might affect crowd safety.
        
        Focus on:
        - Media attention driving crowds
        - Reported safety concerns
        - Coverage of similar events
        - Public statements by organizers
        
        Use the mock_news_analysis tool to gather news intelligence.
        Highlight any news factors that could impact crowd size or safety.
        """,
        tools=[mock_news_analysis]
    )
    optional_agents.append(news_agent)

# Weather Analysis Agent (if Weather API available)
if WEATHER_API_KEY:
    def mock_weather_analysis(location: str) -> str:
        """
        Get current and forecast weather conditions.
        Note: This is a placeholder function. Implement actual Weather API calls when ready.
        """
        return f"""
        🌤️ Weather Analysis: {location}
        
        Weather API Status: {'Connected' if WEATHER_API_KEY else 'API key needed'}
        
        Current Conditions: [Requires API implementation]
        Forecast: [Requires API implementation]
        Crowd Impact: [Requires API implementation]
        
        Note: Connect your Weather API key to get real-time weather analysis.
        """
    
    weather_agent = LlmAgent(
        model=DEFAULT_MODEL,
        name="weather_analysis_agent",
        description="Analyzes weather conditions and their impact on crowd behavior",
        instruction="""
        You analyze weather conditions to predict how they might affect crowd behavior and safety.
        
        Focus on:
        - Weather driving indoor crowding
        - Conditions affecting visibility and movement
        - Temperature and comfort impacts
        - Severe weather risks
        
        Use the mock_weather_analysis tool to gather weather intelligence.
        Assess how weather conditions might influence crowd dynamics and safety.
        """,
        tools=[mock_weather_analysis]
    )
    optional_agents.append(weather_agent)

# Traffic Analysis Agent (if Google Maps API available)
if GOOGLE_MAPS_API_KEY:
    def mock_traffic_analysis(location: str) -> str:
        """
        Analyze traffic conditions and transportation access.
        Note: This is a placeholder function. Implement actual Google Maps API calls when ready.
        """
        return f"""
        🚗 Traffic Analysis: {location}
        
        Google Maps API Status: {'Connected' if GOOGLE_MAPS_API_KEY else 'API key needed'}
        
        Current Traffic: [Requires API implementation]
        Public Transit: [Requires API implementation]  
        Parking Availability: [Requires API implementation]
        Access Routes: [Requires API implementation]
        
        Note: Connect your Google Maps API key to get real-time traffic analysis.
        """
    
    traffic_agent = LlmAgent(
        model=DEFAULT_MODEL,
        name="traffic_analysis_agent",
        description="Analyzes traffic patterns and transportation bottlenecks",
        instruction="""
        You analyze traffic and transportation conditions that could affect crowd arrivals and departures.
        
        Focus on:
        - Transportation bottlenecks
        - Parking limitations
        - Public transit capacity
        - Route congestion patterns
        
        Use the mock_traffic_analysis tool to gather traffic intelligence.
        Identify transportation factors that could create crowd management challenges.
        """,
        tools=[mock_traffic_analysis]
    )
    optional_agents.append(traffic_agent)

def get_available_agents():
    """
    Get list of available optional agents based on configured API keys.
    
    Returns:
        list: Available agents that can be used
    """
    return optional_agents

def get_agent_status():
    """
    Get status of all optional agents and their API requirements.
    
    Returns:
        dict: Status of each agent type
    """
    return {
        "social_media": "Available" if (TWITTER_API_KEY or REDDIT_API_KEY) else "Needs Twitter/Reddit API keys",
        "news_monitoring": "Available" if NEWS_API_KEY else "Needs News API key", 
        "weather_analysis": "Available" if WEATHER_API_KEY else "Needs Weather API key",
        "traffic_analysis": "Available" if GOOGLE_MAPS_API_KEY else "Needs Google Maps API key",
        "total_optional_agents": len(optional_agents)
    } 