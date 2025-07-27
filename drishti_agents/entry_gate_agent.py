"""
Entry Gate Congestion Agent for DrishtiAI
=========================================

Analyzes entry gate congestion patterns, crowd flow dynamics,
and bottleneck situations to predict stampede risks.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .config import DEFAULT_MODEL
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
import math


def analyze_entry_gate_patterns(location: str, venue_capacity: int = 50000, num_gates: int = 4) -> Dict[str, Any]:
    """
    Analyze entry gate patterns and congestion risks.
    
    Args:
        location: The venue/location
        venue_capacity: Total venue capacity
        num_gates: Number of entry gates
        
    Returns:
        Dictionary with entry gate analysis results
    """
    
    gate_analysis = {
        "total_gates": num_gates,
        "gate_capacity_per_hour": [],
        "bottleneck_gates": [],
        "crowd_flow_rate": 0.0,
        "estimated_entry_time": "unknown",
        "congestion_risk_score": 0.0,
        "peak_entry_periods": [],
        "security_checkpoint_delays": [],
        "accessibility_considerations": []
    }
    
    # Calculate theoretical gate capacity
    # Typical gate can process 600-1200 people per hour depending on security level
    base_capacity_per_gate = 800  # people per hour
    
    # Adjust based on venue type
    location_lower = location.lower()
    if any(term in location_lower for term in ["airport", "stadium"]):
        base_capacity_per_gate = 600  # Higher security = slower processing
    elif any(term in location_lower for term in ["park", "square"]):
        base_capacity_per_gate = 1200  # Lower security = faster processing
    elif any(term in location_lower for term in ["arena", "theater"]):
        base_capacity_per_gate = 900  # Medium security
    
    # Calculate per-gate capacity
    for i in range(num_gates):
        # Simulate some variation in gate efficiency
        variation = 0.8 + (i * 0.1)  # Gates vary from 80% to 110% efficiency
        gate_capacity = int(base_capacity_per_gate * variation)
        gate_analysis["gate_capacity_per_hour"].append(gate_capacity)
    
    # Calculate total processing capacity
    total_hourly_capacity = sum(gate_analysis["gate_capacity_per_hour"])
    gate_analysis["crowd_flow_rate"] = total_hourly_capacity
    
    # Estimate entry time for full capacity
    if total_hourly_capacity > 0:
        hours_needed = venue_capacity / total_hourly_capacity
        gate_analysis["estimated_entry_time"] = f"{hours_needed:.1f} hours for full capacity"
    
    # Identify bottleneck gates (gates with significantly lower capacity)
    avg_capacity = sum(gate_analysis["gate_capacity_per_hour"]) / len(gate_analysis["gate_capacity_per_hour"])
    for i, capacity in enumerate(gate_analysis["gate_capacity_per_hour"]):
        if capacity < avg_capacity * 0.8:
            gate_analysis["bottleneck_gates"].append(f"Gate {i+1} (capacity: {capacity}/hour)")
    
    # Calculate congestion risk
    # Risk increases when demand approaches or exceeds capacity
    if venue_capacity > total_hourly_capacity * 2:  # More than 2 hours to fill
        gate_analysis["congestion_risk_score"] = 0.8
    elif venue_capacity > total_hourly_capacity * 1.5:
        gate_analysis["congestion_risk_score"] = 0.6
    elif venue_capacity > total_hourly_capacity:
        gate_analysis["congestion_risk_score"] = 0.4
    else:
        gate_analysis["congestion_risk_score"] = 0.2
    
    # Add risk for bottleneck gates
    if len(gate_analysis["bottleneck_gates"]) > 0:
        gate_analysis["congestion_risk_score"] += 0.2
    
    # Identify peak entry periods
    gate_analysis["peak_entry_periods"] = [
        "30-60 minutes before event start",
        "15-30 minutes before event start (highest risk)"
    ]
    
    # Security checkpoint considerations
    gate_analysis["security_checkpoint_delays"] = [
        "Metal detector processing: 10-15 seconds per person",
        "Bag check processing: 20-30 seconds per person",
        "Ticket verification: 5-10 seconds per person"
    ]
    
    # Accessibility considerations
    gate_analysis["accessibility_considerations"] = [
        "Wheelchair accessible entrances may have slower flow",
        "VIP/priority lane processing affects main gate capacity",
        "Age and mobility factors in crowd processing speed"
    ]
    
    return gate_analysis


def monitor_queue_dynamics(expected_arrival_pattern: str = "normal") -> Dict[str, Any]:
    """
    Monitor queue formation and dynamics at entry gates.
    
    Args:
        expected_arrival_pattern: Expected crowd arrival pattern
        
    Returns:
        Dictionary with queue dynamics analysis
    """
    
    queue_analysis = {
        "queue_formation_risk": 0.0,
        "estimated_queue_length": {},
        "queue_wait_times": {},
        "crowd_density_levels": {},
        "queue_management_recommendations": [],
        "panic_trigger_points": []
    }
    
    # Analyze different arrival patterns
    if expected_arrival_pattern == "surge":
        queue_analysis["queue_formation_risk"] = 0.9
        queue_analysis["estimated_queue_length"] = {
            "peak_time": "500-1000 people per gate",
            "normal_time": "100-200 people per gate"
        }
        queue_analysis["queue_wait_times"] = {
            "peak_time": "45-90 minutes",
            "normal_time": "10-20 minutes"
        }
        queue_analysis["panic_trigger_points"] = [
            "Queue length exceeds 1000 people",
            "Wait time exceeds 60 minutes",
            "Gates temporarily close due to overcrowding"
        ]
    
    elif expected_arrival_pattern == "early":
        queue_analysis["queue_formation_risk"] = 0.3
        queue_analysis["estimated_queue_length"] = {
            "peak_time": "200-400 people per gate",
            "early_arrival": "50-100 people per gate"
        }
        queue_analysis["queue_wait_times"] = {
            "peak_time": "20-30 minutes",
            "early_arrival": "5-10 minutes"
        }
    
    else:  # normal pattern
        queue_analysis["queue_formation_risk"] = 0.5
        queue_analysis["estimated_queue_length"] = {
            "peak_time": "300-600 people per gate",
            "normal_time": "50-150 people per gate"
        }
        queue_analysis["queue_wait_times"] = {
            "peak_time": "30-45 minutes",
            "normal_time": "5-15 minutes"
        }
    
    # Crowd density analysis
    queue_analysis["crowd_density_levels"] = {
        "low_density": "< 2 people per square meter (safe)",
        "medium_density": "2-4 people per square meter (moderate risk)",
        "high_density": "4-6 people per square meter (high risk)",
        "critical_density": "> 6 people per square meter (stampede risk)"
    }
    
    # Generate queue management recommendations
    if queue_analysis["queue_formation_risk"] > 0.7:
        queue_analysis["queue_management_recommendations"] = [
            "Implement multiple queue lanes per gate",
            "Deploy crowd control barriers to organize flow",
            "Station personnel to manage queue density",
            "Consider opening additional emergency entry points",
            "Implement real-time queue length communication"
        ]
    elif queue_analysis["queue_formation_risk"] > 0.4:
        queue_analysis["queue_management_recommendations"] = [
            "Monitor queue lengths closely",
            "Prepare additional entry points if needed",
            "Ensure clear signage and queue organization"
        ]
    
    return queue_analysis


def analyze_crowd_flow_patterns(venue_layout: str = "standard") -> Dict[str, Any]:
    """
    Analyze crowd flow patterns and potential chokepoints.
    
    Args:
        venue_layout: Type of venue layout
        
    Returns:
        Dictionary with crowd flow analysis
    """
    
    flow_analysis = {
        "entry_flow_rate": 0.0,
        "chokepoint_locations": [],
        "flow_bottlenecks": [],
        "crowd_dispersion_areas": [],
        "emergency_exit_accessibility": [],
        "flow_optimization_suggestions": []
    }
    
    # Analyze based on venue layout
    if venue_layout == "stadium":
        flow_analysis["entry_flow_rate"] = 0.8  # Multiple wide entrances
        flow_analysis["chokepoint_locations"] = [
            "Concourse entrance tunnels",
            "Escalator and stairway access points",
            "Security checkpoint areas"
        ]
        flow_analysis["crowd_dispersion_areas"] = [
            "Large concourse areas",
            "Multiple food/retail zones",
            "Seating section distribution points"
        ]
        
    elif venue_layout == "arena":
        flow_analysis["entry_flow_rate"] = 0.7  # More concentrated entry
        flow_analysis["chokepoint_locations"] = [
            "Main entrance lobby",
            "Elevator access to upper levels",
            "Concourse intersection points"
        ]
        
    elif venue_layout == "outdoor":
        flow_analysis["entry_flow_rate"] = 0.9  # More open space
        flow_analysis["chokepoint_locations"] = [
            "Entry gate areas",
            "Bridge or pathway crossings",
            "Stage/performance area approaches"
        ]
        flow_analysis["crowd_dispersion_areas"] = [
            "Open field areas",
            "Multiple viewing zones",
            "Vendor and facility areas"
        ]
    
    else:  # standard
        flow_analysis["entry_flow_rate"] = 0.6
        flow_analysis["chokepoint_locations"] = [
            "Main entrance areas",
            "Corridor intersections",
            "Stairway access points"
        ]
    
    # Identify flow bottlenecks
    flow_analysis["flow_bottlenecks"] = [
        "Single-file security checkpoints",
        "Narrow doorways and passages",
        "Elevator capacity limitations",
        "Ticket scanning delays"
    ]
    
    # Emergency exit considerations
    flow_analysis["emergency_exit_accessibility"] = [
        "Multiple emergency exits required",
        "Exit capacity must exceed entry capacity",
        "Clear emergency evacuation routes",
        "Emergency exit signage and lighting"
    ]
    
    # Flow optimization suggestions
    flow_analysis["flow_optimization_suggestions"] = [
        "Implement directional flow patterns",
        "Use barriers to guide crowd movement",
        "Create multiple dispersal routes",
        "Balance load across all entry points",
        "Provide real-time crowd density information"
    ]
    
    return flow_analysis


def calculate_entry_gate_risk_score(gate_data: Dict[str, Any], queue_data: Dict[str, Any], 
                                  flow_data: Dict[str, Any]) -> float:
    """Calculate overall entry gate risk score"""
    
    risk_score = 0.0
    
    # Base risk from gate congestion
    risk_score += gate_data.get("congestion_risk_score", 0.0) * 0.4
    
    # Queue formation risk
    risk_score += queue_data.get("queue_formation_risk", 0.0) * 0.3
    
    # Flow pattern risk (inverted - lower flow rate = higher risk)
    flow_rate = flow_data.get("entry_flow_rate", 0.5)
    flow_risk = 1.0 - flow_rate
    risk_score += flow_risk * 0.2
    
    # Additional risk factors
    if len(gate_data.get("bottleneck_gates", [])) > 1:
        risk_score += 0.1
    
    if len(flow_data.get("chokepoint_locations", [])) > 3:
        risk_score += 0.1
    
    return min(risk_score, 1.0)


def generate_entry_gate_recommendations(overall_risk: float, gate_data: Dict[str, Any], 
                                      queue_data: Dict[str, Any]) -> List[str]:
    """Generate entry gate management recommendations"""
    
    recommendations = []
    
    if overall_risk > 0.7:
        recommendations.extend([
            "CRITICAL: Implement emergency crowd control measures",
            "Open all available entry points immediately",
            "Deploy maximum security and crowd management personnel",
            "Consider limiting entry rate to prevent dangerous congestion",
            "Activate emergency protocols for crowd dispersal"
        ])
    
    if overall_risk > 0.5:
        recommendations.extend([
            "Increase personnel at all entry gates",
            "Implement queue management systems",
            "Monitor crowd density continuously",
            "Prepare to open additional entry points"
        ])
    
    if len(gate_data.get("bottleneck_gates", [])) > 0:
        recommendations.extend([
            "Address bottleneck gates with additional resources",
            "Balance crowd flow across all available gates",
            "Consider temporary gate capacity enhancements"
        ])
    
    if queue_data.get("queue_formation_risk", 0.0) > 0.6:
        recommendations.extend([
            "Implement advanced queue management",
            "Provide real-time wait time information",
            "Create multiple queue lanes to distribute load",
            "Deploy crowd psychology specialists"
        ])
    
    recommendations.extend([
        "Ensure emergency exits are clearly marked and accessible",
        "Maintain real-time communication with entry gate teams",
        "Monitor for signs of crowd agitation or panic"
    ])
    
    return recommendations


# Create the Entry Gate Analysis Agent
entry_gate_agent = LlmAgent(
    model=DEFAULT_MODEL,
    name="entry_gate_agent",
    description="""
    Specialized agent for analyzing entry gate congestion patterns, queue dynamics,
    and crowd flow to predict stampede risks at venue entrances.
    """,
    instruction="""
    You are the Entry Gate Analysis Agent for DrishtiAI, specializing in analyzing 
    entry gate patterns, queue dynamics, and crowd flow to predict stampede risks.

    Your expertise includes:
    1. Analyzing entry gate capacity and processing rates
    2. Monitoring queue formation and crowd density
    3. Identifying bottleneck gates and chokepoints
    4. Assessing crowd flow patterns and dynamics
    5. Predicting entry wait times and congestion levels
    6. Evaluating emergency exit accessibility

    When analyzing an event venue, you should:
    1. Assess total entry gate capacity vs. expected attendance
    2. Identify potential bottleneck gates and processing delays
    3. Analyze queue formation patterns and wait times
    4. Monitor crowd density levels and flow rates
    5. Evaluate venue layout for crowd flow optimization
    6. Calculate risk scores based on entry gate factors

    Key factors to monitor:
    - Gate processing capacity and efficiency
    - Queue length and formation patterns
    - Crowd density at entry points
    - Security checkpoint processing times
    - Venue layout and chokepoint locations
    - Emergency exit capacity and accessibility
    - Peak arrival time patterns

    Pay special attention to:
    - Gates with significantly lower processing capacity
    - Queue formations that exceed safe density levels
    - Chokepoints that could cause dangerous crowding
    - Peak arrival periods with highest congestion risk
    - Emergency evacuation route accessibility

    Always consider human psychology in crowds - panic can spread quickly
    when people feel trapped or unable to move forward at expected rates.
    
    Use the google_search tool to find information about venue layouts,
    capacity specifications, and any recent crowd incidents at entry points.
    """,
    tools=[
        google_search,
        analyze_entry_gate_patterns,
        monitor_queue_dynamics,
        analyze_crowd_flow_patterns,
        calculate_entry_gate_risk_score,
        generate_entry_gate_recommendations
    ]
) 