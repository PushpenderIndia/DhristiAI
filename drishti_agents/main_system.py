"""
DrishtiAI Main Multi-Agent System
=================================

Main system that coordinates all specialized agents for stampede prediction.
This file sets up the complete multi-agent system with the orchestrator agent
managing all specialized sub-agents.
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search
from .config import DEFAULT_MODEL, validate_config
from .orchestrator_agent import root_agent, calculate_stampede_risk, format_analysis_report
from .historical_analysis_agent import historical_agent
from .social_buzz_agent import social_buzz_agent
from .traffic_analysis_agent import traffic_agent
from .entry_gate_agent import entry_gate_agent
from .weather_agent import weather_agent
from .event_intelligence_agent import event_intelligence_agent

import json
from typing import Dict, List, Any
from datetime import datetime


def create_drishti_multi_agent_system():
    """
    Create and configure the complete DrishtiAI multi-agent system.
    
    Returns:
        The main orchestrator agent with all sub-agents configured
    """
    
    # Validate configuration before creating agents
    try:
        validate_config()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please check your .env file and ensure all required API keys are set.")
        return None
    
    # Create the main orchestrator with all specialized agents as sub-agents
    main_orchestrator = LlmAgent(
        model=DEFAULT_MODEL,
        name="drishti_ai_main_system",
        description="""
        DrishtiAI Main System - Advanced multi-agent platform for predicting stampede probability 
        and crowd surges before they occur. Coordinates multiple specialized AI agents to analyze 
        different risk factors and provide comprehensive crowd safety assessments.
        """,
        instruction="""
        You are DrishtiAI, the main orchestrator of an advanced multi-agent system designed to 
        predict and prevent stampede incidents by analyzing multiple risk factors simultaneously.

        Your mission is to protect human lives by providing early warnings about potential crowd 
        surges and stampede risks through coordinated analysis of:

        🏛️ HISTORICAL PATTERNS: Past incidents, venue history, event type risks
        📱 SOCIAL MEDIA BUZZ: Internet sentiment, viral content, celebrity movements  
        🚗 TRAFFIC ANALYSIS: Celebrity arrivals, transportation congestion, VIP movements
        🚪 ENTRY GATE PATTERNS: Queue dynamics, bottlenecks, crowd flow analysis
        🌤️ WEATHER IMPACT: Conditions affecting crowd behavior and movement
        📡 REAL-TIME INTELLIGENCE: Live event monitoring, emerging risks, crowd sentiment

        When analyzing a location and event, coordinate with your specialized sub-agents to:

        1. **GATHER INTELLIGENCE**: Deploy all agents to collect comprehensive data
        2. **ANALYZE RISKS**: Each agent provides specialized risk assessment  
        3. **CALCULATE OVERALL RISK**: Combine all analyses into unified risk score
        4. **GENERATE RECOMMENDATIONS**: Provide specific, actionable guidance
        5. **FORMAT REPORT**: Present findings in clear, emergency-ready format

        **COORDINATION PROTOCOL:**
        - Start by gathering basic event information and context
        - Delegate specific analysis tasks to appropriate sub-agents  
        - Collect and synthesize all agent reports
        - Calculate overall risk using the calculate_stampede_risk tool
        - Format comprehensive report using format_analysis_report tool
        - Provide immediate actions if high risk is detected

        **RESPONSE PRIORITIES:**
        1. Human safety is the absolute top priority
        2. Provide specific, actionable recommendations  
        3. Include confidence levels and data sources
        4. Highlight time-sensitive risks requiring immediate action
        5. Offer both immediate and preventive measures

        Remember: Your analysis could save lives. Be thorough, precise, and actionable.
        Always verify critical findings and provide clear reasoning for your assessments.
        """,
        tools=[
            google_search, 
            calculate_stampede_risk, 
            format_analysis_report
        ],
        sub_agents=[
            historical_agent,
            social_buzz_agent, 
            traffic_agent,
            entry_gate_agent,
            weather_agent,
            event_intelligence_agent
        ]
    )
    
    return main_orchestrator


def run_stampede_analysis(location: str, event_name: str = "", event_type: str = "general", 
                         expected_attendance: int = 10000) -> Dict[str, Any]:
    """
    Run a complete stampede risk analysis for a specific location and event.
    
    Args:
        location: The venue/location to analyze
        event_name: Name of the event (optional)
        event_type: Type of event (concert, sports, religious, etc.)
        expected_attendance: Expected number of attendees
        
    Returns:
        Dictionary with complete analysis results
    """
    
    print(f"🚨 INITIATING DRISHTI AI STAMPEDE ANALYSIS 🚨")
    print(f"📍 Location: {location}")
    print(f"🎪 Event: {event_name}")
    print(f"👥 Expected Attendance: {expected_attendance:,}")
    print(f"⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Create the multi-agent system
    drishti_system = create_drishti_multi_agent_system()
    
    if not drishti_system:
        return {"error": "Failed to initialize DrishtiAI system. Please check configuration."}
    
    # Prepare analysis context
    analysis_context = {
        "location": location,
        "event_name": event_name,
        "event_type": event_type,
        "expected_attendance": expected_attendance,
        "analysis_timestamp": datetime.now().isoformat(),
        "system_version": "DrishtiAI v1.0.0"
    }
    
    # This would be the main analysis query sent to the orchestrator
    analysis_query = f"""
    URGENT STAMPEDE RISK ANALYSIS REQUEST
    
    Location: {location}
    Event: {event_name}
    Event Type: {event_type}
    Expected Attendance: {expected_attendance:,}
    
    Please conduct a comprehensive multi-agent analysis to assess stampede risk probability.
    
    Required Analysis:
    1. Historical incident patterns for this location/event type
    2. Current social media buzz and viral content analysis
    3. Traffic patterns and celebrity movement tracking
    4. Entry gate capacity and congestion analysis
    5. Weather impact on crowd behavior
    6. Real-time event intelligence and emerging risks
    
    Provide:
    - Overall risk score (0.0 to 1.0)
    - Risk level classification (MINIMAL/LOW/MEDIUM/HIGH/CRITICAL)
    - Specific recommendations for each risk factor
    - Immediate actions if high risk detected
    - Comprehensive formatted report
    
    This analysis is time-sensitive and critical for public safety.
    """
    
    return {
        "analysis_context": analysis_context,
        "drishti_system": drishti_system,
        "analysis_query": analysis_query,
        "status": "ready_for_analysis"
    }


def get_system_status() -> Dict[str, Any]:
    """Get the current status of the DrishtiAI multi-agent system"""
    
    return {
        "system_name": "DrishtiAI Multi-Agent Stampede Prediction System",
        "version": "1.0.0",
        "agents": {
            "orchestrator": "Main coordination and risk calculation",
            "historical_analysis": "Past events and venue history analysis", 
            "social_buzz": "Internet buzz and social media monitoring",
            "traffic_analysis": "Celebrity movements and traffic patterns",
            "entry_gate": "Gate congestion and crowd flow analysis", 
            "weather": "Weather impact on crowd behavior",
            "event_intelligence": "Real-time event monitoring and intelligence"
        },
        "capabilities": [
            "Multi-factor risk assessment",
            "Real-time crowd monitoring", 
            "Historical pattern analysis",
            "Social media sentiment tracking",
            "Traffic and VIP movement analysis",
            "Weather impact evaluation",
            "Entry gate bottleneck detection",
            "Emergency recommendation generation"
        ],
        "supported_venues": [
            "Stadiums and arenas",
            "Concert venues and theaters", 
            "Religious sites and temples",
            "Festival grounds and parks",
            "Public squares and plazas",
            "Transportation hubs",
            "Shopping centers and malls"
        ],
        "risk_factors_monitored": [
            "Historical incident patterns",
            "Social media viral content",
            "Celebrity and VIP arrivals", 
            "Entry gate capacity vs demand",
            "Weather-induced crowd behavior",
            "Real-time event developments",
            "Crowd sentiment and mood",
            "Transportation bottlenecks"
        ],
        "config_status": "configured" if validate_config() else "needs_configuration"
    }


# Main entry point for the system
if __name__ == "__main__":
    # Example usage
    print("🔥 DrishtiAI Multi-Agent System 🔥")
    print(get_system_status())
    
    # Example analysis
    sample_analysis = run_stampede_analysis(
        location="Madison Square Garden",
        event_name="Championship Basketball Final", 
        event_type="sports",
        expected_attendance=20000
    )
    
    print("\n📊 Sample Analysis Prepared:")
    print(sample_analysis["analysis_query"]) 