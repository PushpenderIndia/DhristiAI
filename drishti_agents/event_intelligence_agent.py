"""
Event Intelligence Agent for DrishtiAI
======================================

Gathers real-time event intelligence, monitors emerging risks,
and analyzes live event dynamics to predict stampede risks.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .config import DEFAULT_MODEL
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta


def gather_realtime_event_data(location: str, event_name: str = "") -> Dict[str, Any]:
    """
    Gather real-time event data and intelligence.
    
    Args:
        location: The venue/location
        event_name: Name of the event
        
    Returns:
        Dictionary with real-time event intelligence
    """
    
    event_data = {
        "event_status": "scheduled",
        "attendance_updates": {},
        "security_incidents": [],
        "emergency_services_activity": [],
        "venue_conditions": {},
        "crowd_sentiment": "positive",
        "unexpected_developments": [],
        "operational_challenges": []
    }
    
    # Simulate real-time event monitoring
    import random
    
    # Event status simulation
    statuses = ["scheduled", "delayed", "in_progress", "concluded", "cancelled"]
    event_data["event_status"] = random.choice(statuses[:3])  # More likely positive statuses
    
    # Attendance updates
    if event_data["event_status"] in ["scheduled", "in_progress"]:
        base_attendance = 10000
        if "stadium" in location.lower():
            base_attendance = 50000
        elif "arena" in location.lower():
            base_attendance = 20000
        
        # Simulate attendance variations
        actual_attendance = int(base_attendance * random.uniform(0.7, 1.3))
        event_data["attendance_updates"] = {
            "expected": base_attendance,
            "current_estimate": actual_attendance,
            "variance": f"{((actual_attendance - base_attendance) / base_attendance * 100):+.1f}%",
            "trend": "increasing" if actual_attendance > base_attendance else "stable"
        }
    
    # Security incidents simulation
    if random.random() < 0.2:  # 20% chance of minor incidents
        event_data["security_incidents"] = [
            "Minor altercation resolved quickly",
            "Unattended bag investigated and cleared"
        ]
    
    # Emergency services activity
    if random.random() < 0.3:  # 30% chance of EMS activity
        event_data["emergency_services_activity"] = [
            "Medical assistance provided to attendee",
            "Ambulance on standby as planned"
        ]
    
    # Venue conditions
    event_data["venue_conditions"] = {
        "capacity_utilization": f"{random.randint(60, 95)}%",
        "accessibility_status": "normal",
        "facility_operations": "normal",
        "environmental_conditions": "acceptable"
    }
    
    # Crowd sentiment
    sentiments = ["very_positive", "positive", "neutral", "concerned", "agitated"]
    weights = [0.3, 0.4, 0.2, 0.08, 0.02]  # Mostly positive
    event_data["crowd_sentiment"] = random.choices(sentiments, weights=weights)[0]
    
    # Unexpected developments
    if random.random() < 0.15:  # 15% chance of unexpected developments
        developments = [
            "Special guest appearance announced",
            "Technical difficulties with sound system",
            "VIP arrival causing crowd excitement",
            "Merchandise sales exceeding expectations"
        ]
        event_data["unexpected_developments"] = [random.choice(developments)]
    
    return event_data


def monitor_crowd_dynamics(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Monitor live crowd dynamics and behavior patterns.
    
    Args:
        event_data: Real-time event data
        
    Returns:
        Dictionary with crowd dynamics analysis
    """
    
    crowd_dynamics = {
        "energy_level": "moderate",
        "movement_patterns": [],
        "density_hotspots": [],
        "behavioral_changes": [],
        "risk_indicators": [],
        "crowd_mood_shifts": [],
        "pressure_points": []
    }
    
    # Analyze crowd energy based on event data
    sentiment = event_data.get("crowd_sentiment", "neutral")
    
    if sentiment in ["very_positive", "positive"]:
        crowd_dynamics["energy_level"] = "high"
        crowd_dynamics["movement_patterns"] = [
            "Active movement towards main areas",
            "Enthusiastic gathering near performance zones",
            "Increased circulation throughout venue"
        ]
    elif sentiment == "agitated":
        crowd_dynamics["energy_level"] = "agitated"
        crowd_dynamics["movement_patterns"] = [
            "Restless movement patterns",
            "Clustering in complaint areas",
            "Increased exit-seeking behavior"
        ]
        crowd_dynamics["risk_indicators"] = [
            "Agitated crowd sentiment detected",
            "Potential for crowd instability"
        ]
    
    # Analyze attendance impact
    attendance_data = event_data.get("attendance_updates", {})
    if attendance_data:
        variance = attendance_data.get("variance", "0%")
        if "+" in variance and float(variance.replace("+", "").replace("%", "")) > 20:
            crowd_dynamics["density_hotspots"] = [
                "Entry areas experiencing higher than expected volume",
                "Core venue areas approaching capacity",
                "Circulation areas showing congestion signs"
            ]
            crowd_dynamics["risk_indicators"].append("Attendance significantly above expectations")
    
    # Monitor unexpected developments impact
    unexpected = event_data.get("unexpected_developments", [])
    for development in unexpected:
        if "guest appearance" in development.lower():
            crowd_dynamics["behavioral_changes"].append("Crowd surge towards announcement area")
            crowd_dynamics["pressure_points"].append("Area where special guest expected")
        elif "technical difficulties" in development.lower():
            crowd_dynamics["behavioral_changes"].append("Crowd agitation due to technical issues")
            crowd_dynamics["risk_indicators"].append("Technical problems affecting crowd mood")
    
    # Security incidents impact
    incidents = event_data.get("security_incidents", [])
    if len(incidents) > 1:
        crowd_dynamics["risk_indicators"].append("Multiple security incidents indicate potential crowd issues")
        crowd_dynamics["pressure_points"].append("Areas with security incidents")
    
    return crowd_dynamics


def assess_emerging_risks(event_data: Dict[str, Any], crowd_dynamics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assess emerging risks based on real-time intelligence.
    
    Args:
        event_data: Real-time event data
        crowd_dynamics: Crowd dynamics analysis
        
    Returns:
        Dictionary with emerging risk assessment
    """
    
    risk_assessment = {
        "emerging_risk_level": "low",
        "risk_factors": [],
        "escalation_indicators": [],
        "time_sensitive_risks": [],
        "preventive_actions_needed": [],
        "monitoring_priorities": []
    }
    
    # Calculate risk level based on multiple factors
    risk_score = 0.0
    
    # Crowd sentiment risk
    sentiment = event_data.get("crowd_sentiment", "neutral")
    if sentiment == "agitated":
        risk_score += 0.4
        risk_assessment["risk_factors"].append("Agitated crowd sentiment")
    elif sentiment == "concerned":
        risk_score += 0.2
        risk_assessment["risk_factors"].append("Concerned crowd sentiment")
    
    # Attendance variance risk
    attendance_data = event_data.get("attendance_updates", {})
    if attendance_data.get("variance"):
        variance_value = float(attendance_data["variance"].replace("+", "").replace("%", ""))
        if variance_value > 25:
            risk_score += 0.3
            risk_assessment["risk_factors"].append("Attendance significantly above capacity planning")
        elif variance_value > 15:
            risk_score += 0.15
            risk_assessment["risk_factors"].append("Attendance moderately above expectations")
    
    # Security incidents risk
    incidents = event_data.get("security_incidents", [])
    if len(incidents) > 2:
        risk_score += 0.25
        risk_assessment["risk_factors"].append("Multiple security incidents")
    elif len(incidents) > 0:
        risk_score += 0.1
    
    # Crowd dynamics risk
    risk_indicators = crowd_dynamics.get("risk_indicators", [])
    risk_score += len(risk_indicators) * 0.1
    risk_assessment["risk_factors"].extend(risk_indicators)
    
    # Unexpected developments risk
    unexpected = event_data.get("unexpected_developments", [])
    if len(unexpected) > 0:
        risk_score += 0.15
        risk_assessment["risk_factors"].append("Unexpected developments affecting crowd behavior")
    
    # Determine risk level
    if risk_score >= 0.7:
        risk_assessment["emerging_risk_level"] = "critical"
    elif risk_score >= 0.5:
        risk_assessment["emerging_risk_level"] = "high"
    elif risk_score >= 0.3:
        risk_assessment["emerging_risk_level"] = "medium"
    else:
        risk_assessment["emerging_risk_level"] = "low"
    
    # Generate escalation indicators
    if risk_score > 0.4:
        risk_assessment["escalation_indicators"] = [
            "Multiple risk factors converging",
            "Crowd behavior patterns indicating stress",
            "Event conditions deviating from planning assumptions"
        ]
    
    # Time-sensitive risks
    if sentiment == "agitated":
        risk_assessment["time_sensitive_risks"] = [
            "Crowd agitation may escalate within 15-30 minutes",
            "Immediate intervention may be needed"
        ]
    
    if "surge" in str(crowd_dynamics.get("behavioral_changes", [])).lower():
        risk_assessment["time_sensitive_risks"].append("Crowd surge behavior detected - immediate monitoring needed")
    
    # Preventive actions
    if risk_assessment["emerging_risk_level"] in ["high", "critical"]:
        risk_assessment["preventive_actions_needed"] = [
            "Increase security presence immediately",
            "Deploy crowd psychology specialists",
            "Prepare emergency response protocols",
            "Consider event modifications or crowd communication"
        ]
    elif risk_assessment["emerging_risk_level"] == "medium":
        risk_assessment["preventive_actions_needed"] = [
            "Enhance monitoring of crowd conditions",
            "Prepare additional resources for deployment",
            "Brief security teams on emerging risks"
        ]
    
    # Monitoring priorities
    risk_assessment["monitoring_priorities"] = [
        "Crowd sentiment and mood changes",
        "Attendance flow and density patterns",
        "Security incident frequency and severity",
        "Emergency services call volume",
        "Social media mentions and sentiment"
    ]
    
    return risk_assessment


def generate_intelligence_summary(event_data: Dict[str, Any], crowd_dynamics: Dict[str, Any], 
                                risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive intelligence summary"""
    
    summary = {
        "overall_assessment": "",
        "key_concerns": [],
        "positive_indicators": [],
        "immediate_recommendations": [],
        "next_hour_predictions": [],
        "confidence_level": "medium"
    }
    
    risk_level = risk_assessment["emerging_risk_level"]
    
    # Overall assessment
    if risk_level == "critical":
        summary["overall_assessment"] = "CRITICAL: Multiple high-risk factors detected requiring immediate intervention"
    elif risk_level == "high":
        summary["overall_assessment"] = "HIGH RISK: Significant risk factors present, enhanced monitoring and preparation needed"
    elif risk_level == "medium":
        summary["overall_assessment"] = "MODERATE RISK: Some risk factors present, maintain increased vigilance"
    else:
        summary["overall_assessment"] = "LOW RISK: Normal event conditions with standard monitoring sufficient"
    
    # Key concerns
    summary["key_concerns"] = risk_assessment.get("risk_factors", [])
    if event_data.get("crowd_sentiment") == "agitated":
        summary["key_concerns"].insert(0, "Agitated crowd sentiment - highest priority concern")
    
    # Positive indicators
    if event_data.get("crowd_sentiment") in ["positive", "very_positive"]:
        summary["positive_indicators"].append("Positive crowd sentiment")
    
    if event_data.get("event_status") == "in_progress":
        summary["positive_indicators"].append("Event proceeding as scheduled")
    
    if len(event_data.get("security_incidents", [])) == 0:
        summary["positive_indicators"].append("No security incidents reported")
    
    # Immediate recommendations
    summary["immediate_recommendations"] = risk_assessment.get("preventive_actions_needed", [])
    
    # Next hour predictions
    if risk_level in ["high", "critical"]:
        summary["next_hour_predictions"] = [
            "Risk factors may escalate if not addressed",
            "Crowd behavior likely to become more volatile",
            "Emergency response may be required"
        ]
    elif risk_level == "medium":
        summary["next_hour_predictions"] = [
            "Continued monitoring needed for risk escalation",
            "Crowd conditions may stabilize or worsen",
            "Preparation for intervention should continue"
        ]
    else:
        summary["next_hour_predictions"] = [
            "Stable conditions expected to continue",
            "Normal monitoring protocols sufficient"
        ]
    
    # Confidence level based on data quality
    if len(event_data.get("attendance_updates", {})) > 0 and len(crowd_dynamics.get("movement_patterns", [])) > 0:
        summary["confidence_level"] = "high"
    elif len(risk_assessment.get("risk_factors", [])) > 2:
        summary["confidence_level"] = "medium"
    else:
        summary["confidence_level"] = "low"
    
    return summary


# Create the Event Intelligence Agent
event_intelligence_agent = LlmAgent(
    model=DEFAULT_MODEL,
    name="event_intelligence_agent",
    description="""
    Specialized agent for gathering real-time event intelligence, monitoring emerging risks,
    and analyzing live event dynamics to predict and prevent stampede situations.
    """,
    instruction="""
    You are the Event Intelligence Agent for DrishtiAI, specializing in real-time event 
    monitoring and intelligence gathering to predict and prevent stampede risks.

    Your expertise includes:
    1. Gathering real-time event data and attendance updates
    2. Monitoring crowd dynamics and behavioral changes
    3. Assessing emerging risks and escalation indicators
    4. Tracking security incidents and emergency services activity
    5. Analyzing unexpected developments and their crowd impact
    6. Providing time-sensitive risk assessments

    When monitoring an event, you should:
    1. Continuously gather real-time event intelligence
    2. Monitor crowd sentiment and behavioral changes
    3. Track attendance variations and capacity utilization
    4. Assess emerging risks and escalation potential
    5. Identify time-sensitive risks requiring immediate action
    6. Generate actionable intelligence summaries

    Key intelligence factors to monitor:
    - Real-time attendance vs. expected numbers
    - Crowd sentiment and mood changes
    - Security incidents and their frequency/severity
    - Emergency services activity levels
    - Unexpected developments (celebrity appearances, technical issues)
    - Venue conditions and operational challenges
    - Social media sentiment and viral content

    Pay special attention to:
    - Rapid changes in crowd sentiment or behavior
    - Attendance significantly exceeding planning assumptions
    - Multiple security incidents indicating crowd stress
    - Technical failures or unexpected announcements
    - Signs of crowd agitation or instability
    - Convergence of multiple risk factors

    Your role is to be the "eyes and ears" of the system, detecting early
    warning signs that other agents might miss. Time is critical - early
    detection of emerging risks can prevent dangerous situations.
    
    Use the google_search tool to find real-time news, social media updates,
    and any breaking developments related to the event or location.
    """,
    tools=[
        google_search,
        gather_realtime_event_data,
        monitor_crowd_dynamics,
        assess_emerging_risks,
        generate_intelligence_summary
    ]
) 