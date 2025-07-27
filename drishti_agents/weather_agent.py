"""
Weather Impact Agent for DrishtiAI
==================================

Analyzes weather conditions and their impact on crowd behavior,
including how weather affects crowd density, movement patterns, and stampede risks.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .config import DEFAULT_MODEL, WEATHER_API_KEY
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
import requests


def analyze_current_weather(location: str) -> Dict[str, Any]:
    """
    Analyze current weather conditions and forecast.
    
    Args:
        location: The location to analyze weather for
        
    Returns:
        Dictionary with weather analysis results
    """
    
    # Simulate weather data (in real implementation, use actual weather API)
    weather_data = {
        "current_conditions": {
            "temperature": 72,  # Fahrenheit
            "humidity": 65,     # Percentage
            "wind_speed": 8,    # mph
            "precipitation": 0, # inches
            "visibility": 10,   # miles
            "condition": "partly_cloudy"
        },
        "forecast_next_6_hours": {
            "temperature_trend": "stable",
            "precipitation_probability": 20,
            "wind_change": "increasing",
            "severe_weather_risk": False
        },
        "weather_alerts": [],
        "crowd_behavior_impact": {}
    }
    
    # Simulate seasonal and location-based variations
    import random
    
    # Adjust for location type
    if "outdoor" in location.lower() or "park" in location.lower():
        weather_data["current_conditions"]["wind_speed"] += 5
        weather_data["forecast_next_6_hours"]["precipitation_probability"] += 10
    
    # Random weather variations
    temp_variation = random.randint(-10, 15)
    weather_data["current_conditions"]["temperature"] += temp_variation
    
    if random.random() < 0.2:  # 20% chance of precipitation
        weather_data["current_conditions"]["precipitation"] = round(random.uniform(0.1, 0.5), 1)
        weather_data["current_conditions"]["condition"] = "rainy"
    
    if random.random() < 0.1:  # 10% chance of severe weather
        weather_data["forecast_next_6_hours"]["severe_weather_risk"] = True
        weather_data["weather_alerts"] = ["Thunderstorm watch in effect"]
    
    return weather_data


def assess_weather_crowd_impact(weather_data: Dict[str, Any], event_type: str = "outdoor") -> Dict[str, Any]:
    """
    Assess how weather conditions impact crowd behavior and safety.
    
    Args:
        weather_data: Current weather conditions
        event_type: Type of event (outdoor, indoor, mixed)
        
    Returns:
        Dictionary with weather impact analysis
    """
    
    impact_analysis = {
        "crowd_comfort_level": "comfortable",
        "shelter_seeking_behavior": "none",
        "crowd_density_changes": "stable",
        "movement_pattern_changes": [],
        "safety_concerns": [],
        "weather_risk_score": 0.0,
        "crowd_behavior_predictions": []
    }
    
    current = weather_data["current_conditions"]
    forecast = weather_data["forecast_next_6_hours"]
    
    # Temperature impact analysis
    temp = current["temperature"]
    if temp > 85:  # Hot weather
        impact_analysis["crowd_comfort_level"] = "uncomfortable_hot"
        impact_analysis["shelter_seeking_behavior"] = "shade_seeking"
        impact_analysis["crowd_density_changes"] = "concentrated_in_shade"
        impact_analysis["weather_risk_score"] += 0.3
        
        impact_analysis["crowd_behavior_predictions"].extend([
            "Crowds will concentrate in shaded areas",
            "Increased risk of heat-related health issues",
            "Higher irritability and shorter tempers in crowds"
        ])
        
        if temp > 95:
            impact_analysis["weather_risk_score"] += 0.2
            impact_analysis["safety_concerns"].append("Heat exhaustion risk")
    
    elif temp < 40:  # Cold weather
        impact_analysis["crowd_comfort_level"] = "uncomfortable_cold"
        impact_analysis["shelter_seeking_behavior"] = "indoor_seeking"
        impact_analysis["crowd_density_changes"] = "concentrated_indoors"
        impact_analysis["weather_risk_score"] += 0.2
        
        impact_analysis["crowd_behavior_predictions"].extend([
            "Crowds will seek indoor areas",
            "Reduced outdoor movement",
            "Layered clothing may affect movement speed"
        ])
    
    # Precipitation impact
    if current["precipitation"] > 0:
        impact_analysis["shelter_seeking_behavior"] = "urgent_shelter_seeking"
        impact_analysis["crowd_density_changes"] = "rapid_concentration"
        impact_analysis["weather_risk_score"] += 0.4
        
        impact_analysis["movement_pattern_changes"].extend([
            "Sudden rush to covered areas",
            "Reduced visibility affecting movement",
            "Slippery surfaces increasing fall risk"
        ])
        
        if current["precipitation"] > 0.2:
            impact_analysis["weather_risk_score"] += 0.3
            impact_analysis["safety_concerns"].extend([
                "Mass shelter-seeking behavior",
                "Slippery walking surfaces",
                "Reduced visibility for crowd management"
            ])
    
    # Wind impact
    if current["wind_speed"] > 20:
        impact_analysis["weather_risk_score"] += 0.2
        impact_analysis["movement_pattern_changes"].append("Difficulty walking, seeking wind protection")
        
        if current["wind_speed"] > 35:
            impact_analysis["weather_risk_score"] += 0.3
            impact_analysis["safety_concerns"].append("High wind safety risk")
    
    # Humidity impact
    if current["humidity"] > 80:
        impact_analysis["weather_risk_score"] += 0.1
        impact_analysis["crowd_behavior_predictions"].append("Increased discomfort and fatigue")
    
    # Severe weather alerts
    if forecast["severe_weather_risk"]:
        impact_analysis["weather_risk_score"] += 0.5
        impact_analysis["safety_concerns"].extend([
            "Severe weather approaching",
            "Potential for emergency evacuation"
        ])
        impact_analysis["crowd_behavior_predictions"].append("Mass exodus if severe weather hits")
    
    # Event type considerations
    if event_type == "outdoor":
        impact_analysis["weather_risk_score"] *= 1.5  # Outdoor events more weather-sensitive
    elif event_type == "mixed":
        impact_analysis["weather_risk_score"] *= 1.2  # Partially weather-sensitive
    
    return impact_analysis


def predict_weather_crowd_scenarios(weather_impact: Dict[str, Any], attendance: int = 10000) -> Dict[str, Any]:
    """
    Predict specific crowd scenarios based on weather impact.
    
    Args:
        weather_impact: Weather impact analysis
        attendance: Expected attendance
        
    Returns:
        Dictionary with weather-based crowd scenarios
    """
    
    scenarios = {
        "most_likely_scenario": "",
        "worst_case_scenario": "",
        "crowd_distribution_changes": {},
        "timeline_predictions": [],
        "emergency_preparations_needed": []
    }
    
    risk_score = weather_impact["weather_risk_score"]
    shelter_behavior = weather_impact["shelter_seeking_behavior"]
    
    # Determine most likely scenario
    if risk_score < 0.3:
        scenarios["most_likely_scenario"] = "Weather will have minimal impact on crowd behavior"
    elif risk_score < 0.6:
        scenarios["most_likely_scenario"] = "Weather will cause moderate crowd redistribution"
    else:
        scenarios["most_likely_scenario"] = "Weather will significantly impact crowd behavior and safety"
    
    # Determine worst-case scenario
    if shelter_behavior == "urgent_shelter_seeking":
        scenarios["worst_case_scenario"] = "Mass rush to indoor areas causing dangerous overcrowding"
        scenarios["emergency_preparations_needed"].extend([
            "Prepare indoor overflow areas",
            "Deploy crowd control at shelter entrances",
            "Monitor indoor capacity limits"
        ])
    elif shelter_behavior == "shade_seeking":
        scenarios["worst_case_scenario"] = "Dangerous overcrowding in limited shaded areas"
        scenarios["emergency_preparations_needed"].extend([
            "Set up additional shade structures",
            "Provide cooling stations",
            "Monitor crowd density in shaded areas"
        ])
    
    # Predict crowd distribution changes
    if attendance > 5000:
        if shelter_behavior in ["urgent_shelter_seeking", "indoor_seeking"]:
            indoor_percentage = min(80, attendance * 0.0008)  # Up to 80% seeking indoor areas
            scenarios["crowd_distribution_changes"] = {
                "indoor_areas": f"{indoor_percentage:.0f}% of crowd",
                "outdoor_areas": f"{100-indoor_percentage:.0f}% of crowd",
                "pressure_points": "Indoor entrances and covered areas"
            }
        elif shelter_behavior == "shade_seeking":
            scenarios["crowd_distribution_changes"] = {
                "shaded_areas": "60-70% of crowd",
                "open_areas": "30-40% of crowd",
                "pressure_points": "Trees, awnings, and building overhangs"
            }
    
    # Timeline predictions
    if risk_score > 0.5:
        scenarios["timeline_predictions"] = [
            "0-15 minutes: Initial weather impact recognition",
            "15-30 minutes: Crowd begins redistributing",
            "30-60 minutes: Peak shelter-seeking behavior",
            "60+ minutes: Crowd adapts or event modifications needed"
        ]
    
    return scenarios


def generate_weather_recommendations(weather_impact: Dict[str, Any], scenarios: Dict[str, Any]) -> List[str]:
    """Generate weather-related crowd management recommendations"""
    
    recommendations = []
    risk_score = weather_impact["weather_risk_score"]
    
    if risk_score > 0.7:
        recommendations.extend([
            "HIGH WEATHER RISK: Implement emergency weather protocols",
            "Prepare for mass crowd redistribution due to weather",
            "Deploy additional personnel at shelter areas",
            "Consider weather-related event modifications or delays"
        ])
    
    if "urgent_shelter_seeking" in weather_impact["shelter_seeking_behavior"]:
        recommendations.extend([
            "Prepare emergency shelter areas with adequate capacity",
            "Monitor indoor area capacity limits closely",
            "Deploy crowd control at all shelter entrances",
            "Communicate weather updates to crowd regularly"
        ])
    
    if weather_impact["crowd_comfort_level"] == "uncomfortable_hot":
        recommendations.extend([
            "Provide additional water stations and cooling areas",
            "Monitor crowd for heat-related health issues",
            "Consider extending shade structures",
            "Advise crowd about heat safety measures"
        ])
    
    if weather_impact["crowd_comfort_level"] == "uncomfortable_cold":
        recommendations.extend([
            "Ensure adequate indoor warming areas",
            "Monitor for cold-related health issues",
            "Consider providing emergency warming supplies"
        ])
    
    if len(weather_impact["safety_concerns"]) > 0:
        recommendations.extend([
            "Address specific weather safety concerns identified",
            "Increase medical personnel availability",
            "Prepare for potential weather-related emergencies"
        ])
    
    if scenarios.get("worst_case_scenario"):
        recommendations.append(f"Prepare for worst-case scenario: {scenarios['worst_case_scenario']}")
    
    return recommendations


# Create the Weather Impact Agent
weather_agent = LlmAgent(
    model=DEFAULT_MODEL,
    name="weather_agent",
    description="""
    Specialized agent for analyzing weather conditions and their impact on crowd behavior,
    including how weather affects crowd density, movement patterns, and stampede risks.
    """,
    instruction="""
    You are the Weather Impact Agent for DrishtiAI, specializing in analyzing how weather 
    conditions affect crowd behavior and contribute to stampede risks.

    Your expertise includes:
    1. Monitoring current weather conditions and forecasts
    2. Assessing how weather impacts crowd comfort and behavior
    3. Predicting crowd redistribution due to weather changes
    4. Identifying weather-related safety concerns and risks
    5. Analyzing shelter-seeking behavior patterns
    6. Evaluating temperature, precipitation, wind, and humidity effects

    When analyzing weather impact on an event, you should:
    1. Check current weather conditions and short-term forecasts
    2. Assess crowd comfort levels and potential behavior changes
    3. Predict shelter-seeking and redistribution patterns
    4. Identify weather-related safety concerns
    5. Calculate weather risk scores for stampede probability
    6. Generate specific recommendations for weather management

    Key weather factors to monitor:
    - Temperature extremes (hot/cold) affecting crowd comfort
    - Precipitation causing sudden shelter-seeking behavior
    - Wind conditions affecting crowd movement and safety
    - Humidity levels impacting crowd endurance
    - Severe weather alerts requiring emergency response
    - Visibility conditions affecting crowd management

    Pay special attention to:
    - Sudden weather changes that cause mass crowd movement
    - Temperature extremes that concentrate crowds in specific areas
    - Precipitation events that trigger urgent shelter-seeking
    - Severe weather that requires emergency evacuation
    - Weather conditions that reduce visibility for crowd management

    Weather can rapidly transform crowd behavior patterns. A sudden rainstorm
    can cause thousands of people to simultaneously seek shelter, creating
    dangerous bottlenecks and overcrowding situations.
    
    Use the google_search tool to find current weather conditions, forecasts,
    and any weather-related alerts for the event location.
    """,
    tools=[
        google_search,
        analyze_current_weather,
        assess_weather_crowd_impact,
        predict_weather_crowd_scenarios,
        generate_weather_recommendations
    ]
) 