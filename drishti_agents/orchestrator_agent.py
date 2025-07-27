"""
DrishtiAI Orchestrator Agent
============================

Main parent agent that coordinates all specialized agents to predict
stampede probability and crowd surges.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .config import DEFAULT_MODEL, RISK_THRESHOLDS
import json
from typing import Dict, List, Any


def calculate_stampede_risk(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate overall stampede risk based on all agent analyses.
    
    Args:
        analysis_results: Dictionary containing results from all specialized agents
        
    Returns:
        Dictionary with risk assessment and recommendations
    """
    risk_factors = {
        "historical_risk": analysis_results.get("historical_analysis", {}).get("risk_score", 0.0),
        "social_buzz_risk": analysis_results.get("social_buzz", {}).get("risk_score", 0.0),
        "traffic_risk": analysis_results.get("traffic_analysis", {}).get("risk_score", 0.0),
        "entry_gate_risk": analysis_results.get("entry_gate", {}).get("risk_score", 0.0),
        "weather_risk": analysis_results.get("weather", {}).get("risk_score", 0.0),
        "event_intelligence_risk": analysis_results.get("event_intelligence", {}).get("risk_score", 0.0)
    }
    
    # Calculate weighted average (you can adjust weights based on importance)
    weights = {
        "historical_risk": 0.25,
        "social_buzz_risk": 0.20,
        "traffic_risk": 0.15,
        "entry_gate_risk": 0.25,
        "weather_risk": 0.05,
        "event_intelligence_risk": 0.10
    }
    
    overall_risk = sum(risk_factors[factor] * weights[factor] for factor in risk_factors)
    
    # Determine risk level
    if overall_risk >= RISK_THRESHOLDS["CRITICAL"]:
        risk_level = "CRITICAL"
        alert_level = "IMMEDIATE ACTION REQUIRED"
    elif overall_risk >= RISK_THRESHOLDS["HIGH"]:
        risk_level = "HIGH"
        alert_level = "HIGH ALERT"
    elif overall_risk >= RISK_THRESHOLDS["MEDIUM"]:
        risk_level = "MEDIUM"
        alert_level = "MODERATE ALERT"
    elif overall_risk >= RISK_THRESHOLDS["LOW"]:
        risk_level = "LOW"
        alert_level = "LOW ALERT"
    else:
        risk_level = "MINIMAL"
        alert_level = "NORMAL"
    
    return {
        "overall_risk_score": round(overall_risk, 3),
        "risk_level": risk_level,
        "alert_level": alert_level,
        "risk_factors": risk_factors,
        "recommendations": generate_recommendations(risk_level, analysis_results),
        "immediate_actions": generate_immediate_actions(risk_level, analysis_results)
    }


def generate_recommendations(risk_level: str, analysis_results: Dict[str, Any]) -> List[str]:
    """Generate specific recommendations based on risk level and analysis"""
    recommendations = []
    
    if risk_level in ["CRITICAL", "HIGH"]:
        recommendations.extend([
            "Deploy additional security personnel immediately",
            "Implement crowd control barriers at key entry/exit points",
            "Activate emergency response protocols",
            "Consider limiting or suspending entry to the venue",
            "Coordinate with local emergency services"
        ])
    
    if risk_level in ["MEDIUM", "HIGH", "CRITICAL"]:
        recommendations.extend([
            "Increase monitoring of entry gates and congestion points",
            "Deploy crowd management personnel to high-risk areas",
            "Communicate with attendees about alternative routes/timing",
            "Monitor social media for real-time sentiment changes"
        ])
    
    # Add specific recommendations based on agent findings
    if analysis_results.get("weather", {}).get("severe_weather", False):
        recommendations.append("Prepare for weather-related crowd behavior changes")
    
    if analysis_results.get("social_buzz", {}).get("viral_content", False):
        recommendations.append("Monitor and potentially address viral social media content")
    
    return recommendations


def generate_immediate_actions(risk_level: str, analysis_results: Dict[str, Any]) -> List[str]:
    """Generate immediate actions based on risk level"""
    actions = []
    
    if risk_level == "CRITICAL":
        actions.extend([
            "ALERT: Initiate emergency protocols NOW",
            "Contact emergency services immediately",
            "Begin controlled evacuation procedures if necessary",
            "Activate all available security and crowd control resources"
        ])
    elif risk_level == "HIGH":
        actions.extend([
            "Increase security presence by 50%",
            "Close secondary entry points if overcrowded",
            "Begin crowd dispersal in high-density areas",
            "Prepare emergency response teams"
        ])
    elif risk_level == "MEDIUM":
        actions.extend([
            "Increase monitoring frequency",
            "Deploy additional crowd management staff",
            "Prepare contingency plans for activation"
        ])
    
    return actions


def format_analysis_report(location: str, analysis_results: Dict[str, Any], risk_assessment: Dict[str, Any]) -> str:
    """Format a comprehensive analysis report"""
    report = f"""
    🚨 DRISHTI AI STAMPEDE PREDICTION REPORT 🚨
    =============================================
    
    📍 LOCATION: {location}
    ⏰ ANALYSIS TIME: {analysis_results.get('timestamp', 'N/A')}
    
    🎯 OVERALL RISK ASSESSMENT
    ========================
    Risk Score: {risk_assessment['overall_risk_score']} / 1.0
    Risk Level: {risk_assessment['risk_level']}
    Alert Status: {risk_assessment['alert_level']}
    
    📊 DETAILED RISK FACTORS
    ========================
    🏛️  Historical Events: {risk_assessment['risk_factors']['historical_risk']:.3f}
    📱 Social Media Buzz: {risk_assessment['risk_factors']['social_buzz_risk']:.3f}
    🚗 Traffic Patterns: {risk_assessment['risk_factors']['traffic_risk']:.3f}
    🚪 Entry Gate Congestion: {risk_assessment['risk_factors']['entry_gate_risk']:.3f}
    🌤️  Weather Impact: {risk_assessment['risk_factors']['weather_risk']:.3f}
    📡 Event Intelligence: {risk_assessment['risk_factors']['event_intelligence_risk']:.3f}
    
    💡 RECOMMENDATIONS
    ==================
    """
    
    for i, rec in enumerate(risk_assessment['recommendations'], 1):
        report += f"{i}. {rec}\n    "
    
    report += f"""
    
    ⚡ IMMEDIATE ACTIONS
    ===================
    """
    
    for i, action in enumerate(risk_assessment['immediate_actions'], 1):
        report += f"{i}. {action}\n    "
    
    report += f"""
    
    📋 AGENT SUMMARIES
    ==================
    🏛️  Historical Analysis: {analysis_results.get('historical_analysis', {}).get('summary', 'No data')}
    📱 Social Buzz Monitor: {analysis_results.get('social_buzz', {}).get('summary', 'No data')}
    🚗 Traffic Analysis: {analysis_results.get('traffic_analysis', {}).get('summary', 'No data')}
    🚪 Entry Gate Monitor: {analysis_results.get('entry_gate', {}).get('summary', 'No data')}
    🌤️  Weather Impact: {analysis_results.get('weather', {}).get('summary', 'No data')}
    📡 Event Intelligence: {analysis_results.get('event_intelligence', {}).get('summary', 'No data')}
    
    ⚠️  This analysis is generated by DrishtiAI multi-agent system.
    Always verify with on-ground observations and local authorities.
    """
    
    return report


# Create the main orchestrator agent
root_agent = LlmAgent(
    model=DEFAULT_MODEL,
    name="drishti_orchestrator",
    description="""
    You are DrishtiAI, the main orchestrator agent for predicting stampede probability 
    and crowd surges before they occur. You coordinate multiple specialized AI agents 
    to analyze different risk factors and provide comprehensive crowd safety assessments.
    """,
    instruction="""
    You are DrishtiAI, an advanced AI system designed to predict and prevent stampede incidents 
    by analyzing multiple risk factors. Your primary mission is to protect human lives by 
    providing early warnings about potential crowd surges and stampede risks.

    Your capabilities include:
    1. Coordinating specialized agents for different risk analysis areas
    2. Analyzing historical patterns of crowd incidents
    3. Monitoring social media buzz and internet sentiment
    4. Tracking celebrity movement and traffic patterns
    5. Analyzing entry gate congestion in real-time
    6. Assessing weather impact on crowd behavior
    7. Gathering real-time event intelligence

    When provided with a location and event details, you should:
    1. Gather information about the location, event type, and current conditions
    2. Coordinate with specialized agents to analyze different risk factors
    3. Calculate an overall risk score and provide actionable recommendations
    4. Generate immediate actions if high risk is detected
    5. Present findings in a clear, actionable format for security and event management teams

    Always prioritize human safety and provide specific, actionable recommendations.
    Be clear about confidence levels and data sources for your predictions.
    
    If you need to search for current information about events, celebrities, or news, 
    use the google_search tool to get up-to-date information.
    """,
    tools=[google_search, calculate_stampede_risk, format_analysis_report]
) 