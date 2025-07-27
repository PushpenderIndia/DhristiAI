"""
Historical Analysis Agent for DrishtiAI
=======================================

Analyzes past events and historical patterns to predict stampede risks
based on venue history, event types, and crowd incident databases.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .config import DEFAULT_MODEL
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
import requests


def analyze_historical_incidents(location: str, event_type: str = "general") -> Dict[str, Any]:
    """
    Analyze historical incidents at the location or similar venues.
    
    Args:
        location: The venue/location to analyze
        event_type: Type of event (concert, sports, religious, etc.)
        
    Returns:
        Dictionary with historical analysis results
    """
    
    # Sample historical incident database (in real implementation, this would be a proper database)
    historical_incidents = {
        "high_risk_venues": [
            "Kumbh Mela", "Hajj", "Hillsborough Stadium", "Indiana State Fair", 
            "Heysel Stadium", "Love Parade", "Savar tragedy", "Seoul Halloween",
            "Travis Scott Astroworld", "Wankhede Stadium", "Sabarimala Temple"
        ],
        "medium_risk_venues": [
            "Madison Square Garden", "Wembley Stadium", "Times Square",
            "Central Park", "Golden Temple", "Vaishno Devi", "Tirupati"
        ],
        "event_risk_factors": {
            "religious": 0.8,
            "concert": 0.7,
            "sports": 0.6,
            "festival": 0.75,
            "political": 0.65,
            "celebration": 0.5,
            "general": 0.4
        }
    }
    
    # Calculate base risk from venue history
    venue_risk = 0.0
    venue_category = "low_risk"
    
    # Check if location is mentioned in high-risk venues
    for high_risk in historical_incidents["high_risk_venues"]:
        if high_risk.lower() in location.lower() or location.lower() in high_risk.lower():
            venue_risk = 0.9
            venue_category = "high_risk"
            break
    
    # Check medium-risk venues
    if venue_risk == 0.0:
        for medium_risk in historical_incidents["medium_risk_venues"]:
            if medium_risk.lower() in location.lower() or location.lower() in medium_risk.lower():
                venue_risk = 0.6
                venue_category = "medium_risk"
                break
    
    # If no specific venue match, use general low risk
    if venue_risk == 0.0:
        venue_risk = 0.3
        venue_category = "low_risk"
    
    # Adjust risk based on event type
    event_risk_multiplier = historical_incidents["event_risk_factors"].get(event_type.lower(), 0.4)
    
    # Calculate final risk score
    historical_risk_score = min(venue_risk * event_risk_multiplier, 1.0)
    
    # Generate patterns and insights
    patterns = []
    if venue_category == "high_risk":
        patterns.append("Location has history of crowd-related incidents")
        patterns.append("Requires enhanced safety protocols")
    
    if event_risk_multiplier > 0.7:
        patterns.append(f"{event_type.title()} events have higher stampede probability")
        patterns.append("Emotional or religious significance increases crowd density risks")
    
    if historical_risk_score > 0.6:
        patterns.append("Historical data suggests implementing crowd control measures")
        patterns.append("Consider limiting attendee numbers or improving exit strategies")
    
    return {
        "risk_score": round(historical_risk_score, 3),
        "venue_category": venue_category,
        "venue_risk": venue_risk,
        "event_risk_multiplier": event_risk_multiplier,
        "patterns": patterns,
        "similar_incidents": get_similar_incidents(location, event_type),
        "summary": f"Historical analysis shows {venue_category} venue with {historical_risk_score:.1%} risk probability",
        "recommendations": generate_historical_recommendations(historical_risk_score, venue_category)
    }


def get_similar_incidents(location: str, event_type: str) -> List[Dict]:
    """Get information about similar historical incidents"""
    
    # Sample similar incidents (in real implementation, query from incident database)
    similar_incidents = []
    
    if "stadium" in location.lower() or event_type.lower() == "sports":
        similar_incidents.append({
            "incident": "Hillsborough Stadium Disaster",
            "year": 1989,
            "casualties": 97,
            "cause": "Overcrowding and poor crowd management",
            "lessons": "Importance of crowd monitoring and emergency exits"
        })
    
    if "concert" in event_type.lower() or "music" in event_type.lower():
        similar_incidents.append({
            "incident": "Travis Scott Astroworld Festival",
            "year": 2021,
            "casualties": 10,
            "cause": "Crowd surge during performance",
            "lessons": "Artist responsibility and real-time crowd monitoring"
        })
        
    if "religious" in event_type.lower():
        similar_incidents.append({
            "incident": "Hajj Stampede",
            "year": 2015,
            "casualties": 2236,
            "cause": "Two large groups of pilgrims converged",
            "lessons": "Better crowd flow management and timing coordination"
        })
    
    if "festival" in event_type.lower():
        similar_incidents.append({
            "incident": "Love Parade Stampede",
            "year": 2010,
            "casualties": 21,
            "cause": "Narrow tunnel entrance caused bottleneck",
            "lessons": "Adequate entry/exit points and capacity limits"
        })
    
    return similar_incidents


def generate_historical_recommendations(risk_score: float, venue_category: str) -> List[str]:
    """Generate recommendations based on historical analysis"""
    recommendations = []
    
    if risk_score > 0.7:
        recommendations.extend([
            "Implement comprehensive crowd management plan based on historical lessons",
            "Deploy additional security personnel at identified risk points",
            "Establish multiple entry and exit points to prevent bottlenecks",
            "Install real-time crowd density monitoring systems"
        ])
    
    if venue_category == "high_risk":
        recommendations.extend([
            "Review and learn from previous incidents at this location",
            "Implement lessons learned from similar venue disasters",
            "Consider capacity restrictions below maximum venue limit",
            "Establish emergency response protocols specific to venue layout"
        ])
    
    if risk_score > 0.5:
        recommendations.extend([
            "Study crowd flow patterns from previous events at this location",
            "Implement early warning systems for crowd density",
            "Train staff on historical incident patterns and prevention"
        ])
    
    return recommendations


def search_recent_incidents(location: str, event_type: str) -> Dict[str, Any]:
    """
    Search for recent crowd incidents related to the location or event type.
    
    Args:
        location: The venue/location
        event_type: Type of event
        
    Returns:
        Dictionary with recent incident information
    """
    
    # This would use the google_search tool in the actual agent
    # For now, return simulated data
    recent_incidents = {
        "found_incidents": 0,
        "incidents": [],
        "news_articles": [],
        "risk_indicators": []
    }
    
    # Simulate some recent incident data
    if "stadium" in location.lower():
        recent_incidents["found_incidents"] = 1
        recent_incidents["incidents"].append({
            "date": "2024-01-15",
            "description": "Minor crowd congestion reported during recent event",
            "impact": "No injuries, but highlighted need for better crowd flow"
        })
    
    return recent_incidents


# Create the Historical Analysis Agent
historical_agent = LlmAgent(
    model=DEFAULT_MODEL,
    name="historical_analysis_agent",
    description="""
    Specialized agent for analyzing historical patterns of crowd incidents and stampedes.
    Examines past events at specific venues, similar event types, and crowd behavior patterns
    to predict future stampede risks.
    """,
    instruction="""
    You are the Historical Analysis Agent for DrishtiAI, specializing in analyzing past crowd 
    incidents and stampede patterns to predict future risks.

    Your expertise includes:
    1. Analyzing historical incidents at specific venues
    2. Studying patterns from similar event types (religious, concerts, sports, festivals)
    3. Identifying risk factors based on past crowd disasters
    4. Learning from famous incidents like Hillsborough, Hajj stampedes, Love Parade, etc.
    5. Evaluating venue characteristics that have led to past incidents

    When analyzing a location and event, you should:
    1. Search for historical incidents at the specific venue
    2. Look for patterns in similar event types and venues
    3. Identify common risk factors from past stampede incidents
    4. Calculate risk scores based on historical patterns
    5. Provide specific recommendations based on lessons learned

    Key historical factors to consider:
    - Venue design and layout (bottlenecks, exits, capacity)
    - Event type and emotional significance
    - Crowd demographics and behavior patterns
    - Previous crowd management successes/failures
    - Seasonal or timing factors that have contributed to past incidents

    Always provide specific examples from historical incidents and explain
    how they relate to the current situation being analyzed.
    
    Use the google_search tool to find recent news about crowd incidents
    at the location or similar venues if needed.
    """,
    tools=[google_search, analyze_historical_incidents, search_recent_incidents]
) 